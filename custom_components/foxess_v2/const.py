"""Constants for the Foxess V2 integration."""

DOMAIN = "foxess_v2"
DEFAULT_NAME = "Foxess V2"

# API endpoints
BASE_URL = "https://www.foxesscloud.com"
LOGIN_URL = f"{BASE_URL}/v2/login"
API_URL = f"{BASE_URL}/v2/api"

# Update interval (5 minutes)
UPDATE_INTERVAL = 300

# Configuration
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Sensor types
SENSOR_TYPES = {
    "pv_power": {
        "name": "PV Power",
        "unit": "kW",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement",
    },
    "battery_soc": {
        "name": "Battery State of Charge",
        "unit": "%",
        "icon": "mdi:battery",
        "device_class": "battery",
        "state_class": "measurement",
    },
    "battery_power": {
        "name": "Battery Power",
        "unit": "kW",
        "icon": "mdi:battery-charging",
        "device_class": "power",
        "state_class": "measurement",
    },
    "grid_power": {
        "name": "Grid Power",
        "unit": "kW",
        "icon": "mdi:transmission-tower",
        "device_class": "power",
        "state_class": "measurement",
    },
    "load_power": {
        "name": "Load Power",
        "unit": "kW",
        "icon": "mdi:home-lightning-bolt",
        "device_class": "power",
        "state_class": "measurement",
    },
    "inverter_power": {
        "name": "Inverter Power",
        "unit": "kW",
        "icon": "mdi:solar-power-variant",
        "device_class": "power",
        "state_class": "measurement",
    },
    "energy_today": {
        "name": "Energy Today",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "energy_total": {
        "name": "Energy Total",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "feed_in_energy_today": {
        "name": "Feed-in Energy Today",
        "unit": "kWh",
        "icon": "mdi:transmission-tower-export",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "grid_consumption_today": {
        "name": "Grid Consumption Today",
        "unit": "kWh",
        "icon": "mdi:transmission-tower-import",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "battery_charge_today": {
        "name": "Battery Charge Today",
        "unit": "kWh",
        "icon": "mdi:battery-plus",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "battery_discharge_today": {
        "name": "Battery Discharge Today",
        "unit": "kWh",
        "icon": "mdi:battery-minus",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
}