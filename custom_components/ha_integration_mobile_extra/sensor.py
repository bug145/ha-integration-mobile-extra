"""Sensor platform for HA Integration Mobile Extra."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.const import CONF_NAME

from .const import DOMAIN, DEFAULT_NAME, CONF_SELECTED_DEVICES, CONF_DEVICE_NAMES


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    selected_devices = config_entry.data.get(CONF_SELECTED_DEVICES, [])
    device_names = config_entry.data.get(CONF_DEVICE_NAMES, {})
    
    entities = []
    
    # Create a sensor for each selected device
    for device_id in selected_devices:
        device_name = device_names.get(device_id, f"Device {device_id}")
        entities.append(MobileExtraSensor(config_entry, device_id, device_name))
    
    # If no devices selected, create a default sensor
    if not entities:
        entities.append(MobileExtraSensor(config_entry, None, DEFAULT_NAME))
    
    async_add_entities(entities)


class MobileExtraSensor(SensorEntity):
    """Representation of a Mobile Extra Sensor."""

    def __init__(self, config_entry: ConfigEntry, device_id: str | None, device_name: str) -> None:
        """Initialize the sensor."""
        self.config_entry = config_entry
        self.device_id = device_id
        self.device_name = device_name
        
        # Set entity attributes
        if device_id:
            self._attr_name = f"{device_name} Extra"
            self._attr_unique_id = f"{config_entry.entry_id}_{device_id}_mobile_extra"
        else:
            self._attr_name = device_name
            self._attr_unique_id = f"{config_entry.entry_id}_mobile_extra"
        
        self._attr_native_value = "Ready"
        self._attr_icon = "mdi:cellphone"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return entity specific state attributes."""
        attrs = {
            "device_name": self.device_name,
        }
        
        if self.device_id:
            attrs["device_id"] = self.device_id
            
        return attrs 