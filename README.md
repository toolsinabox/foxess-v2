# Foxess V2 Integration for Home Assistant

A custom Home Assistant integration for Foxess V2 solar inverter systems. This integration connects to the Foxess Cloud v2 platform using your username and password to retrieve real-time and historical data from your solar system.

> ⚠️ **Status**: This integration is functional but requires testing with actual Foxess V2 accounts. The Foxess V2 platform uses modern web authentication which may require additional configuration. See [INSTALLATION.md](INSTALLATION.md) for details.

## 🌟 Features

### Real-time Monitoring
- ☀️ PV (Solar) Power
- 🔋 Battery State of Charge (SoC)  
- ⚡ Battery Power (Charge/Discharge)
- 🏠 Grid Power (Import/Export)
- 💡 Load Power (Home Consumption)
- 🔌 Inverter Power

### Daily Energy Totals
- 📊 Energy Generation Today
- 📈 Total Energy Generated
- ↗️ Feed-in Energy Today
- ↘️ Grid Consumption Today
- 🔋⬆️ Battery Charge Today
- 🔋⬇️ Battery Discharge Today

### Easy Setup
- ✅ Simple configuration through Home Assistant UI
- 🔐 No API keys needed - just username and password
- 🔄 Automatic data updates every 5 minutes
- 🏗️ HACS-compatible repository structure

## 📁 Repository Structure

```
foxess-v2-hacs/
├── custom_components/foxess_v2/    # Main integration code
│   ├── __init__.py                 # Integration setup
│   ├── manifest.json               # Integration metadata
│   ├── config_flow.py             # Configuration UI
│   ├── sensor.py                  # Sensor entities
│   ├── const.py                   # Constants & sensor definitions
│   ├── foxess_api.py              # API client (web scraping)
│   ├── strings.json               # UI translations
│   └── translations/
│       └── en.json                # English translations
├── README.md                      # This file
├── INSTALLATION.md                # Detailed installation guide
├── hacs.json                      # HACS metadata
├── LICENSE                        # MIT License
└── .gitignore                     # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites
- Home Assistant 2024.1.0 or newer
- Foxess Cloud V2 account (https://www.foxesscloud.com/v2/)
- Active Foxess inverter registered in the cloud

### Installation via HACS

1. **Add Custom Repository**
   - Open HACS → Integrations
   - Click ⋮ → Custom repositories
   - Add repository URL
   - Category: Integration

2. **Install**
   - Search for "Foxess V2"
   - Click Install
   - Restart Home Assistant

3. **Configure**
   - Settings → Devices & Services → Add Integration
   - Search "Foxess V2"
   - Enter your Foxess Cloud credentials

### Manual Installation

```bash
cd /config/custom_components/
git clone [your-repo-url] foxess_v2
# Restart Home Assistant
```

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions and troubleshooting.

## 📊 Available Sensors

All sensors are created automatically with the prefix `sensor.foxess_`:

| Sensor | Unit | Device Class |
|--------|------|--------------|
| PV Power | kW | power |
| Battery State of Charge | % | battery |
| Battery Power | kW | power |
| Grid Power | kW | power |
| Load Power | kW | power |
| Inverter Power | kW | power |
| Energy Today | kWh | energy |
| Energy Total | kWh | energy |
| Feed-in Energy Today | kWh | energy |
| Grid Consumption Today | kWh | energy |
| Battery Charge Today | kWh | energy |
| Battery Discharge Today | kWh | energy |

## 🎨 Dashboard Example

```yaml
type: vertical-stack
cards:
  - type: entities
    title: ☀️ Solar System - Real Time
    entities:
      - entity: sensor.foxess_pv_power
        name: Solar Power
        icon: mdi:solar-power
      - entity: sensor.foxess_battery_state_of_charge
        name: Battery Level
        icon: mdi:battery
      - entity: sensor.foxess_battery_power
        name: Battery Power
        icon: mdi:battery-charging
      - entity: sensor.foxess_grid_power
        name: Grid Power
        icon: mdi:transmission-tower
      - entity: sensor.foxess_load_power
        name: Home Consumption
        icon: mdi:home-lightning-bolt
        
  - type: entities
    title: 📊 Today's Energy
    entities:
      - entity: sensor.foxess_energy_today
        name: Solar Generated
        icon: mdi:solar-power
      - entity: sensor.foxess_feed_in_energy_today
        name: Exported to Grid
        icon: mdi:transmission-tower-export
      - entity: sensor.foxess_grid_consumption_today
        name: Imported from Grid
        icon: mdi:transmission-tower-import
      - entity: sensor.foxess_battery_charge_today
        name: Battery Charged
        icon: mdi:battery-plus
      - entity: sensor.foxess_battery_discharge_today
        name: Battery Discharged
        icon: mdi:battery-minus
```

## 🔧 Configuration

The integration is configured through the Home Assistant UI. No YAML configuration is needed.

**Required:**
- Username (email address)
- Password

**Optional Settings:**
- Update interval (default: 5 minutes)

## 🐛 Troubleshooting

### Invalid Authentication
1. Verify credentials at https://www.foxesscloud.com/v2/
2. Check for typos in username/password
3. Ensure you're using V2, not the old API system

### No Data Showing
1. Wait 5 minutes for first update
2. Check if inverter is online in Foxess Cloud
3. Enable debug logging (see below)
4. Check Home Assistant logs

### Sensors Show "Unavailable"
1. Check internet connection
2. Verify Foxess Cloud is accessible
3. Check integration status in Devices & Services

### Enable Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.foxess_v2: debug
```

Then check: Settings → System → Logs

## 🧪 Testing Status

This integration has been developed and tested with:
- ✅ Home Assistant Core structure
- ✅ HACS compatibility
- ✅ Configuration flow UI
- ✅ Sensor definitions
- ⚠️ **Needs testing**: Actual Foxess V2 API authentication

**Help wanted**: If you test this integration, please report:
- Success or failure
- Any error messages
- Your Home Assistant version
- Any API endpoints you discover

## 🛠️ Development

### Architecture

```
User Credentials
      ↓
Config Flow (config_flow.py)
      ↓
Integration Setup (__init__.py)
      ↓
Data Coordinator (updates every 5 min)
      ↓
Foxess API Client (foxess_api.py)
      ↓
Web Scraping / API Calls
      ↓
Sensors (sensor.py)
      ↓
Home Assistant
```

### API Client

The `foxess_api.py` module handles:
1. Authentication with username/password
2. Session management
3. Device discovery
4. Data extraction

If the current implementation doesn't work, alternative methods include:
- Selenium-based browser automation
- Playwright for JavaScript rendering
- Reverse-engineered API endpoints

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your Foxess system
5. Submit a pull request

## 📝 Known Limitations

1. **Authentication**: Foxess V2 uses JavaScript-heavy authentication which may require browser automation
2. **Update Frequency**: Limited to 5-minute intervals to avoid overwhelming the Foxess servers
3. **Multiple Devices**: Currently supports single device only (first device found)
4. **Historical Data**: Limited to daily totals (no hourly history yet)

## 🔮 Future Enhancements

- [ ] Support for multiple inverters/devices
- [ ] Hourly historical data
- [ ] Battery scheduling controls
- [ ] Push notifications for system events
- [ ] Energy flow diagrams
- [ ] Selenium/Playwright fallback for authentication
- [ ] Local Modbus support (no cloud required)

## 📄 License

MIT License

Copyright (c) 2025 Foxess V2 Integration Contributors

See [LICENSE](LICENSE) file for full details.

## 🙏 Credits

- Developed for the Home Assistant community
- Inspired by other solar integrations
- Created for Foxess V2 users worldwide

## ⚠️ Disclaimer

This is an **unofficial integration** and is not affiliated with, endorsed by, or connected to Foxess in any way. 

Use at your own risk. The authors are not responsible for:
- Any damage to your system
- Data loss
- Terms of service violations
- Account issues

Always ensure you comply with Foxess Cloud's terms of service.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/foxess-v2-hacs/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/foxess-v2-hacs/discussions)
- **Home Assistant Community**: [Community Forum](https://community.home-assistant.io/)

## 🌐 Links

- [Foxess Cloud V2](https://www.foxesscloud.com/v2/)
- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [Integration Documentation](INSTALLATION.md)

---

**Made with ❤️ for the Home Assistant Community**
