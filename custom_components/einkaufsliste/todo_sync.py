"""🔁 To-do-Liste automatisch herüberholen.

Man wählt in ⚙️ → Import eine To-do-Liste aus Home Assistant (z. B. die Alexa-Einkaufsliste aus der
Integration „Alexa Devices“). Alles, was dort landet („Alexa, setz Milch auf die Einkaufsliste“), wandert
sofort in die Einkaufsliste und wird in der To-do-Liste wieder gelöscht. Ganz ohne Automation.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_call_later, async_track_state_change_event

_LOGGER = logging.getLogger(__name__)

# So heißt der Eintrager im Verlauf und unter dem Artikel (nach der Integration der To-do-Liste)
_SOURCE_NAMES = {
    "alexa_devices": "Alexa",
    "google_tasks": "Google Tasks",
    "bring": "Bring!",
    "todoist": "Todoist",
    "shopping_list": "HA-Einkaufsliste",
    "local_todo": "To-do-Liste",
    "ourgroceries": "OurGroceries",
    "anylist": "AnyList",
}


def source_name(hass: HomeAssistant, entity_id: str) -> str:
    """„Alexa“ statt „todo.alexa_einkaufsliste“ – so sieht jeder, woher der Artikel kam."""
    entry = er.async_get(hass).async_get(entity_id)
    if entry and entry.platform in _SOURCE_NAMES:
        return _SOURCE_NAMES[entry.platform]
    state = hass.states.get(entity_id)
    return (state.name if state else None) or entity_id.split(".", 1)[-1]


class TodoSync:
    """Beobachtet eine To-do-Liste und holt neue Einträge in die Einkaufsliste."""

    def __init__(self, hass: HomeAssistant, manager: Any) -> None:
        self.hass = hass
        self.manager = manager
        self._unsub = None
        self._busy = False
        self._again = False
        self._retry = None

    @callback
    def start(self) -> None:
        self.stop()
        cfg = self.manager.todo_sync
        if not cfg or not cfg.get("entity_id"):
            return
        self._unsub = async_track_state_change_event(self.hass, [cfg["entity_id"]], self._on_change)
        self.hass.async_create_task(self.run())  # gleich einmal nachschauen

    @callback
    def stop(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None
        if self._retry:
            self._retry()
            self._retry = None

    @callback
    def _on_change(self, event: Event) -> None:
        new = event.data.get("new_state")
        if new is None or str(new.state) in ("0", "unavailable", "unknown"):
            return
        self.hass.async_create_task(self.run())

    async def run(self) -> int:
        """Offene Einträge holen, eintragen, dort löschen. Gibt die Anzahl zurück."""
        if self._busy:
            self._again = True
            return 0
        self._busy = True
        total = 0
        try:
            while True:
                self._again = False
                total += await self._once()
                if not self._again:
                    break
        finally:
            self._busy = False
        return total

    async def _once(self) -> int:
        cfg = self.manager.todo_sync
        if not cfg:
            return 0
        entity_id = cfg["entity_id"]
        state = self.hass.states.get(entity_id)
        if state is None or state.state in ("unavailable", "unknown"):
            return 0
        try:
            resp = await self.hass.services.async_call(
                "todo", "get_items", {"entity_id": entity_id, "status": ["needs_action"]},
                blocking=True, return_response=True,
            )
        except Exception as err:  # noqa: BLE001 – Liste gerade nicht erreichbar: später nochmal
            _LOGGER.debug("To-do-Liste %s nicht lesbar: %s", entity_id, err)
            self._later()
            return 0
        entries = (resp or {}).get(entity_id, {}).get("items", [])
        if not entries:
            return 0
        who = source_name(self.hass, entity_id)
        done: list[str] = []
        added = 0
        with self.manager.acting(who, None, "sync"):
            for entry in entries:
                text = str(entry.get("summary") or "").strip()
                if text and len(text) <= 80:
                    try:
                        store_id = cfg.get("store_id") if self.manager.store_by_id(cfg.get("store_id")) else None
                        self.manager.add_item(text, store_id=store_id, added_by=who, notify=True)
                        added += 1
                    except ValueError as err:
                        _LOGGER.debug("„%s“ nicht übernommen: %s", text, err)
                done.append(entry.get("uid") or text)
        if added:
            self.manager.todo_sync["count"] = int(self.manager.todo_sync.get("count", 0)) + added
            self.manager._changed()
        if done:
            try:  # erst eintragen, dann dort löschen – so geht nichts verloren
                await self.hass.services.async_call(
                    "todo", "remove_item", {"entity_id": entity_id, "item": done}, blocking=True
                )
            except Exception as err:  # noqa: BLE001
                _LOGGER.warning("Einträge in %s konnten nicht gelöscht werden: %s", entity_id, err)
        return added

    @callback
    def _later(self) -> None:
        if self._retry:
            return

        @callback
        def _fire(_now: Any) -> None:
            self._retry = None
            self.hass.async_create_task(self.run())

        self._retry = async_call_later(self.hass, 300, _fire)
