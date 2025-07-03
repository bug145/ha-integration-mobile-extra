"""Config flow for HA Integration Mobile Extra."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DEFAULT_NAME, CONF_SELECTED_DEVICES, CONF_DEVICE_NAMES
from .options_flow import HaIntegrationMobileExtraOptionsFlow


class HaIntegrationMobileExtraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HA Integration Mobile Extra."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.mobile_devices: dict[str, str] = {}

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Get mobile devices from mobile_app integration
        self.mobile_devices = await self._get_mobile_devices(self.hass)
        
        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data={
                    CONF_NAME: user_input.get(CONF_NAME, DEFAULT_NAME),
                    CONF_SELECTED_DEVICES: user_input.get(CONF_SELECTED_DEVICES, []),
                    CONF_DEVICE_NAMES: self.mobile_devices,
                },
            )

        # Create schema with checkboxes for mobile devices
        schema_dict = {
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        }
        
        if self.mobile_devices:
            schema_dict[vol.Optional(CONF_SELECTED_DEVICES, default=[])] = cv.multi_select(
                self.mobile_devices
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(schema_dict),
            description_placeholders={"name": DEFAULT_NAME},
        )

    @staticmethod
    async def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> HaIntegrationMobileExtraOptionsFlow:
        """Get the options flow for this handler."""
        return HaIntegrationMobileExtraOptionsFlow(config_entry)

    async def _get_mobile_devices(self, hass: HomeAssistant) -> dict[str, str]:
        """Get list of mobile devices from mobile_app integration."""
        devices = {}
        
        try:
            # Get all mobile_app config entries
            mobile_app_entries = [
                entry for entry in hass.config_entries.async_entries("mobile_app")
            ]
            
            for entry in mobile_app_entries:
                # Get the device_id from the entry data
                device_id = entry.data.get("device_id")
                if device_id:
                    device_name = entry.data.get("device_name", entry.title)
                    devices[device_id] = device_name
                
        except Exception:
            # If mobile_app is not available, return empty dict
            pass
            
        return devices 