"""Sensor platform for Foxess V2."""
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Foxess V2 sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []
    for sensor_type, sensor_config in SENSOR_TYPES.items():
        entities.append(FoxessV2Sensor(coordinator, sensor_type, sensor_config))

    async_add_entities(entities)


class FoxessV2Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a Foxess V2 sensor."""

    def __init__(self, coordinator, sensor_type: str, sensor_config: dict):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        self._attr_name = f"Foxess {sensor_config['name']}"
        self._attr_unique_id = f"foxess_v2_{sensor_type}"
        self._attr_icon = sensor_config.get("icon")
        self._attr_native_unit_of_measurement = sensor_config.get("unit")
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_state_class = sensor_config.get("state_class")

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, "foxess_v2")},
            "name": "Foxess V2 Inverter",
            "manufacturer": "Foxess",
            "model": "V2",
        }
