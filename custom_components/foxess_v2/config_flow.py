"""Config flow for Foxess V2 integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .foxess_api import FoxessV2API

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class FoxessV2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Foxess V2."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Test the credentials
                api = FoxessV2API(
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    self.hass,
                )
                await api.login()

                # Create entry
                return self.async_create_entry(
                    title=f"Foxess V2 ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )
            except Exception as err:
                _LOGGER.error("Failed to authenticate: %s", err)
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
