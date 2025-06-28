"""Sensor platform for HA Integration Mobile Extra."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.const import CONF_NAME

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([MobileExtraSensor(config_entry)])


class MobileExtraSensor(SensorEntity):
    """Representation of a Mobile Extra Sensor."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.config_entry = config_entry
        self._attr_name = config_entry.data.get(CONF_NAME, "Mobile Extra Sensor")
        self._attr_unique_id = f"{config_entry.entry_id}_mobile_extra"
        self._attr_native_value = "Ready"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._attr_native_value 