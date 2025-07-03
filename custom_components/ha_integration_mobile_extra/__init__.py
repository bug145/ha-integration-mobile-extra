"""The HA Integration Mobile Extra integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform

DOMAIN = "ha_integration_mobile_extra"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Integration Mobile Extra from a config entry."""
    # Store config entry in hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Load sensor platform for each selected device
    selected_devices = entry.data.get("selected_devices", [])
    for device_id in selected_devices:
        await async_load_platform(
            hass,
            Platform.SENSOR,
            DOMAIN,
            {"device_id": device_id, "config_entry": entry},
            entry,
        )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove config entry from hass data
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    
    # Unload all platforms for this entry
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SENSOR])
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry) 