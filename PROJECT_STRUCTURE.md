# Foxess V2 Integration - Complete File Structure

```
/app/
│
├── custom_components/foxess_v2/      # Home Assistant Integration
│   ├── __init__.py                    # Main integration logic (async_setup_entry)
│   ├── manifest.json                  # Integration metadata for HA
│   ├── config_flow.py                 # UI configuration flow
│   ├── sensor.py                      # Sensor entities definition
│   ├── const.py                       # Constants and sensor types
│   ├── foxess_api.py                  # API client (web scraping logic)
│   ├── strings.json                   # UI strings
│   └── translations/
│       └── en.json                    # English translations
│
├── README.md                          # Main project documentation
├── INSTALLATION.md                    # Detailed installation guide
├── GITHUB_SETUP.md                    # GitHub publishing instructions
├── LICENSE                            # MIT License
├── hacs.json                          # HACS metadata
├── .gitignore                         # Git ignore patterns
│
└── test_files/                        # Development test files (not for production)
    ├── test_foxess_api.py             # API endpoint tester
    └── test_selenium_scraper.py       # Selenium-based scraper test
```

## File Descriptions

### Integration Files (custom_components/foxess_v2/)

#### `__init__.py` (265 lines)
**Purpose**: Main integration entry point
- Sets up the integration in Home Assistant
- Creates DataUpdateCoordinator for periodic updates
- Manages integration lifecycle (setup/unload)
- Coordinates between API client and sensors

**Key Functions**:
- `async_setup_entry()` - Initialize integration
- `async_unload_entry()` - Clean up on removal
- `async_update_data()` - Fetch data from Foxess Cloud

#### `manifest.json` (10 lines)
**Purpose**: Integration metadata for Home Assistant
- Domain: `foxess_v2`
- Version: `1.0.0`
- Dependencies: `aiohttp`, `beautifulsoup4`
- Enable config flow: Yes
- IoT class: Cloud polling

#### `config_flow.py` (52 lines)
**Purpose**: Configuration UI in Home Assistant
- Provides username/password input form
- Validates credentials before saving
- Creates integration entry after successful auth
- Handles error states (invalid auth, connection errors)

#### `sensor.py` (68 lines)
**Purpose**: Defines sensor entities
- Creates 12 sensor entities
- Updates from DataUpdateCoordinator
- Provides device info for grouping
- Maps data to sensor states

**Sensors Created**:
1. PV Power (kW)
2. Battery SoC (%)
3. Battery Power (kW)
4. Grid Power (kW)
5. Load Power (kW)
6. Inverter Power (kW)
7. Energy Today (kWh)
8. Energy Total (kWh)
9. Feed-in Energy Today (kWh)
10. Grid Consumption Today (kWh)
11. Battery Charge Today (kWh)
12. Battery Discharge Today (kWh)

#### `const.py` (82 lines)
**Purpose**: Constants and configuration
- Domain name and URLs
- Update interval (300 seconds)
- Sensor type definitions
- Unit of measurements
- Device classes
- State classes (measurement/total_increasing)

#### `foxess_api.py` (200 lines)
**Purpose**: Foxess Cloud API client
- Handles authentication (username/password)
- Manages session with aiohttp
- Discovers devices
- Fetches real-time data
- Fetches daily reports
- Parses responses into usable data

**Key Methods**:
- `login()` - Authenticate with Foxess Cloud
- `get_data()` - Fetch all available data
- `_parse_real_data()` - Parse real-time values
- `_parse_report_data()` - Parse daily totals
- `_parse_battery_data()` - Parse battery info

#### `strings.json` & `translations/en.json` (18 lines each)
**Purpose**: UI text translations
- Config flow titles and descriptions
- Input field labels
- Error messages
- Abort reasons

### Documentation Files

#### `README.md` (400+ lines)
**Purpose**: Main project documentation
- Feature overview with emojis
- Repository structure
- Quick start guide
- Installation instructions
- Dashboard examples
- Troubleshooting guide
- Development information
- Links and resources

#### `INSTALLATION.md` (250+ lines)
**Purpose**: Detailed setup instructions
- Current status and warnings
- Installation options (HACS/manual)
- Testing procedures
- Alternative solutions if login fails
- Available sensors list
- Troubleshooting steps
- Manual API testing code

#### `GITHUB_SETUP.md` (250+ lines)
**Purpose**: GitHub publishing guide
- Git initialization steps
- GitHub repository creation
- Repository URL updates
- Release creation
- HACS submission process
- Post-publication checklist

### Configuration Files

#### `hacs.json` (5 lines)
**Purpose**: HACS discovery metadata
- Integration name
- Render README: true
- Domains: sensor
- Minimum HA version: 2024.1.0

#### `.gitignore` (30+ lines)
**Purpose**: Git ignore patterns
- Python cache files
- Virtual environments
- IDE files
- System files
- Build artifacts

#### `LICENSE` (21 lines)
**Purpose**: MIT License
- Open source license
- Permission grants
- Warranty disclaimer

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interaction                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Config Flow (config_flow.py)                │
│  • Display username/password form                            │
│  • Validate credentials                                      │
│  • Create integration entry                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            Integration Setup (__init__.py)                   │
│  • Create API client                                         │
│  • Setup DataUpdateCoordinator                               │
│  • Schedule updates every 5 minutes                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              API Client (foxess_api.py)                      │
│  • Login to Foxess Cloud                                     │
│  • Discover devices                                          │
│  • Fetch real-time data                                      │
│  • Fetch daily reports                                       │
│  • Parse JSON responses                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│               Sensors (sensor.py)                            │
│  • Create 12 sensor entities                                 │
│  • Update from coordinator data                              │
│  • Provide to Home Assistant                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Home Assistant UI                           │
│  • Display sensors in dashboard                              │
│  • Historical data & graphs                                  │
│  • Automation triggers                                       │
└─────────────────────────────────────────────────────────────┘
```

## API Endpoints (Attempted)

The integration tries these Foxess V2 endpoints:

```
Login:
  POST https://www.foxesscloud.com/c/v0/user/login
  POST https://www.foxesscloud.com/op/v0/user/login
  
  Body: {"user": "email", "password": "password"}
  Headers: Content-Type: application/json

Device List:
  GET https://www.foxesscloud.com/op/v0/device/list
  Headers: token: <auth_token>

Real-time Data:
  GET https://www.foxesscloud.com/op/v0/device/real/query?sn=<device_sn>
  Headers: token: <auth_token>

Daily Report:
  GET https://www.foxesscloud.com/op/v0/device/report/day?sn=<device_sn>
  Headers: token: <auth_token>

Battery Info:
  GET https://www.foxesscloud.com/op/v0/device/battery/info?sn=<device_sn>
  Headers: token: <auth_token>
```

## Installation Paths

### For Users (HACS Custom Repository):
```
1. Home Assistant → HACS → Integrations
2. Menu → Custom repositories
3. Add: https://github.com/YOUR_USERNAME/foxess-v2-hacs
4. Install integration
5. Restart HA
6. Settings → Integrations → Add Integration → Foxess V2
```

### For Developers (Manual):
```
1. Copy custom_components/foxess_v2/ to:
   /config/custom_components/foxess_v2/
   
2. Restart Home Assistant

3. Integration appears in: Settings → Integrations
```

## Testing Requirements

To test this integration, you need:
- ✅ Home Assistant instance (2024.1.0+)
- ✅ Foxess V2 account credentials
- ✅ Active Foxess inverter
- ⚠️ Ability to view Home Assistant logs
- ⚠️ Browser DevTools knowledge (for debugging API)

## Known Limitations

1. **Authentication**: May not work with current endpoints
   - Foxess V2 likely uses JavaScript-heavy SPA
   - May require browser automation (Selenium/Playwright)
   - Actual API endpoints need to be discovered

2. **Single Device**: Only supports first device found

3. **Update Frequency**: 5 minute intervals only

4. **Data Types**: Limited to real-time + daily totals

## Next Steps for Testing

1. **Install** the integration in Home Assistant
2. **Enable debug logging** in configuration.yaml
3. **Try to configure** with your credentials
4. **Check logs** for errors and API responses
5. **Report findings**:
   - Success/failure
   - Error messages
   - Actual API endpoints used (from browser DevTools)

## Potential Fixes

If authentication fails, options include:

**Option A**: Update API endpoints based on actual Foxess V2 calls

**Option B**: Implement Selenium browser automation

**Option C**: Reverse-engineer the Foxess mobile app

## Total Files Created

- **7** Core integration files
- **2** Translation files  
- **4** Documentation files
- **2** Configuration files
- **2** Test files (development only)

**Total**: 17 files ready for GitHub repository

---

This integration is ready to be published and tested! 🚀
