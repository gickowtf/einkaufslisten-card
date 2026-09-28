"""Ja/Nein-Sensor: steht überhaupt etwas auf der Liste?"""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SIGNAL_UPDATED
from .manager import EinkaufslisteManager
from .sensor import _device


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    manager: EinkaufslisteManager = hass.data[DOMAIN]["manager"]
    async_add_entities([EtwasZuKaufenSensor(manager, entry)])


class EtwasZuKaufenSensor(BinarySensorEntity):
    """binary_sensor.einkaufsliste_etwas_zu_kaufen – an, sobald mindestens ein Artikel offen ist"""

    _attr_has_entity_name = True
    _attr_translation_key = "etwas_zu_kaufen"
    _attr_should_poll = False

    def __init__(self, manager: EinkaufslisteManager, entry: ConfigEntry) -> None:
        self._m = manager
        self._attr_unique_id = f"{entry.entry_id}_etwas_zu_kaufen"
        self._attr_device_info = _device(entry)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(async_dispatcher_connect(self.hass, SIGNAL_UPDATED, self._refresh))

    @callback
    def _refresh(self) -> None:
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        return any(not i["checked"] for i in self._m.items)

    @property
    def icon(self) -> str:
        return "mdi:cart-arrow-down" if self.is_on else "mdi:cart-check"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        stores = {}
        for i in self._m.items:
            if not i["checked"]:
                st = self._m.store_by_id(i.get("store_id"))
                name = st["name"] if st else "Egal wo"
                stores[name] = stores.get(name, 0) + 1
        return {"anzahl": sum(stores.values()), "geschaefte": sorted(stores)}
