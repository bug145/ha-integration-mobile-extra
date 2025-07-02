from homeassistant.config_entries import ConfigFlow
from .const import DOMAIN

class HaIntegrationMobileExtraConfigFlow(ConfigFlow):
    """Config flow for HA Integration Mobile Extra."""
    VERSION = 1
    DOMAIN = DOMAIN

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="HA Integration Mobile Extra", data={})
        return self.async_show_form(step_id="user") 