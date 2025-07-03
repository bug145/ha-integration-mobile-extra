"""Options flow for HA Integration Mobile Extra."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DEFAULT_NAME, CONF_SELECTED_DEVICES, CONF_DEVICE_NAMES


class HaIntegrationMobileExtraOptionsFlow(config_entries.OptionsFlow):
    """Options flow for HA Integration Mobile Extra."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self.mobile_devices: dict[str, str] = {}

    async def async_step_init(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Manage the options."""
        # Get mobile devices from mobile_app integration
        self.mobile_devices = await self._get_mobile_devices(self.hass)
        
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_NAME: user_input.get(CONF_NAME, DEFAULT_NAME),
                    CONF_SELECTED_DEVICES: user_input.get(CONF_SELECTED_DEVICES, []),
                    CONF_DEVICE_NAMES: self.mobile_devices,
                },
            )

        # Create schema with checkboxes for mobile devices
        schema_dict = {
            vol.Optional(
                CONF_NAME, 
                default=self.config_entry.data.get(CONF_NAME, DEFAULT_NAME)
            ): str,
        }
        
        if self.mobile_devices:
            current_selected = self.config_entry.data.get(CONF_SELECTED_DEVICES, [])
            schema_dict[vol.Optional(CONF_SELECTED_DEVICES, default=current_selected)] = cv.multi_select(
                self.mobile_devices
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
            description_placeholders={"name": DEFAULT_NAME},
        )

    async def _get_mobile_devices(self, hass: HomeAssistant) -> dict[str, str]:
        """Get list of mobile devices from mobile_app integration."""
        devices = {}
        
        try:
            # Get all mobile_app config entries
            mobile_app_entries = [
                entry for entry in hass.config_entries.async_entries("mobile_app")
            ]
            
            for entry in mobile_app_entries:
                device_name = entry.data.get("device_name", entry.title)
                devices[entry.entry_id] = device_name
                
        except Exception:
            # If mobile_app is not available, return empty dict
            pass
            
        return devices 