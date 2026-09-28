"""📧 Produkte per E-Mail auf die Liste.

Home Assistant bringt die Integration „IMAP“ mit: Sie schaut in ein Postfach und meldet jede neue Mail
als Ereignis („imap_content“). Hier hören wir darauf: Kommt eine Mail von einem erlaubten Absender in
das gewählte Postfach, wird jede Zeile ein Artikel – genau wie beim „Text einfügen“.
"""

from __future__ import annotations

import html
import logging
import re
from email.utils import parseaddr
from typing import Any

from homeassistant.core import Event, HomeAssistant, callback

_LOGGER = logging.getLogger(__name__)

EVENT_IMAP = "imap_content"
_TAG = re.compile(r"<[^>]+>")
_BR = re.compile(r"<\s*(br|/p|/div|/li|/tr)\b[^>]*>", re.I)
# ab hier kommt nur noch Zitat / Signatur / Werbung
_STOP = re.compile(
    r"^(--\s*$|_{5,}|-{5,}|am .+ schrieb|on .+ wrote:|von:\s|from:\s|gesendet von|sent from|diese e-mail wurde)",
    re.I,
)


def mail_sources(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Alle eingerichteten IMAP-Postfächer."""
    return [
        {"entry_id": e.entry_id, "name": e.title or e.data.get("username") or "IMAP"}
        for e in hass.config_entries.async_entries("imap")
    ]


def mail_text(text: str | None, subject: str | None = None) -> str:
    """Nur die Einkaufszeilen: ohne HTML, Zitate, Signatur und „Gesendet von meinem iPhone“."""
    raw = text or ""
    if "<" in raw and ">" in raw and re.search(r"<(html|body|div|p|br|span|table)\b", raw, re.I):
        raw = _BR.sub("\n", raw)
        raw = re.sub(r"<(style|script)[^>]*>.*?</\1>", "", raw, flags=re.I | re.S)
        raw = html.unescape(_TAG.sub("", raw))
    lines: list[str] = []
    for line in raw.replace("\r", "").split("\n"):
        stripped = line.strip()
        if _STOP.match(stripped):
            break
        if not stripped or stripped.startswith(">"):
            continue
        lines.append(stripped)
    if not lines and subject:  # nur der Betreff? Dann eben der
        lines = [s.strip() for s in re.split(r"[,;]", subject) if s.strip()]
    return "\n".join(lines[:60])


class MailImport:
    """Hört auf neue Mails aus der IMAP-Integration."""

    def __init__(self, hass: HomeAssistant, manager: Any) -> None:
        self.hass = hass
        self.manager = manager
        self._unsub = None
        self._seen: list[str] = []

    @callback
    def start(self) -> None:
        self.stop()
        if self.manager.mail_import:
            self._unsub = self.hass.bus.async_listen(EVENT_IMAP, self._on_mail)

    @callback
    def stop(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None

    @callback
    def _on_mail(self, event: Event) -> None:
        cfg = self.manager.mail_import
        data = event.data
        if not cfg or data.get("entry_id") != cfg.get("entry_id") or data.get("initial") is False:
            return
        key = f"{data.get('uid')}|{data.get('date')}"
        if key in self._seen:
            return
        self._seen = (self._seen + [key])[-50:]
        name, address = parseaddr(str(data.get("sender") or ""))
        address = address.lower()
        allowed = [s.lower() for s in cfg.get("senders", [])]
        if address not in allowed:
            _LOGGER.info("📧 Mail von %s ignoriert – steht nicht bei den erlaubten Absendern", address or "?")
            return
        text = mail_text(data.get("text"), data.get("subject"))
        if not text:
            return
        from .transfer import import_text  # noqa: PLC0415 – erst hier, sonst Kreis-Import

        store_id = cfg.get("store_id") if self.manager.store_by_id(cfg.get("store_id")) else None
        with self.manager.acting(f"📧 {name or address}", None, "mail"):
            res = import_text(self.manager, text, store_id)
        if res.get("added"):
            cfg["count"] = int(cfg.get("count", 0)) + res["added"]
            self.manager._changed()
