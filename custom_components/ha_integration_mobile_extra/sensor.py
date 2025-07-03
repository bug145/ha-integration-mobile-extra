"""Sensor platform for HA Integration Mobile Extra."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.const import CONF_NAME, ATTR_DEVICE_ID

from .const import DOMAIN, DEFAULT_NAME, CONF_SELECTED_DEVICES, CONF_DEVICE_NAMES


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info: dict | None = None,
) -> None:
    """Set up the sensor platform."""
    if discovery_info is None:
        return

    device_id = discovery_info.get("device_id")
    config_entry = discovery_info.get("config_entry")
    
    if not device_id or not config_entry:
        return

    # Get device name from config
    device_names = config_entry.data.get(CONF_DEVICE_NAMES, {})
    device_name = device_names.get(device_id, f"Device {device_id}")
    
    # Create sensor for this device
    async_add_entities([MobileExtraSensor(device_id, device_name, config_entry)])


class MobileExtraSensor(SensorEntity):
    """Representation of a Mobile Extra Sensor."""

    def __init__(self, device_id: str, device_name: str, config_entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.device_id = device_id
        self.device_name = device_name
        self.config_entry = config_entry
        
        # Set entity attributes to associate with mobile_app device
        self._attr_name = f"{device_name} Extra Sensor"
        self._attr_unique_id = f"{device_id}_mobile_extra_sensor"
        self._attr_device_id = device_id  # Associate with mobile_app device
        self._attr_native_value = "Ready"
        self._attr_icon = "mdi:cellphone-cog"
        self._attr_should_poll = False
        self._attr_entity_category = None

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return entity specific state attributes."""
        return {
            "device_name": self.device_name,
            "device_id": self.device_id,
            "integration": "mobile_extra",
        }

    async def async_added_to_hass(self) -> None:
        """Call when entity is added to hass."""
        # Update state when added to hass
        self._attr_native_value = "Active"
        self.async_write_ha_state() 