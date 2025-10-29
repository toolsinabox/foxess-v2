# Foxess V2 Integration - Installation & Setup Guide

## ⚠️ Important Information

This integration attempts to connect to Foxess Cloud V2 using username/password authentication. However, **Foxess V2 uses a JavaScript-heavy single-page application (SPA)** which may require browser-based authentication.

### Current Status

✅ **Completed:**
- Full HACS-compatible integration structure
- Configuration flow through Home Assistant UI
- All sensor definitions for solar/battery/grid data
- Complete documentation

⚠️ **Requires Testing:**
- The login mechanism needs to be tested with actual Foxess V2 credentials
- API endpoints may need adjustment based on actual Foxess V2 responses
- Alternative authentication methods may be needed

## Installation Options

### Option 1: HACS Installation (Recommended once published)

1. Open HACS in your Home Assistant
2. Click "Integrations"
3. Click the menu (three dots) in the top right
4. Select "Custom repositories"
5. Add this repository URL
6. Select category: "Integration"
7. Install the "Foxess V2" integration
8. Restart Home Assistant

### Option 2: Manual Installation

1. Copy the `custom_components/foxess_v2` folder to your Home Assistant's `config/custom_components/` directory

   ```bash
   # On your Home Assistant machine
   cd /config/custom_components/
   git clone [your-repo-url] foxess_v2_temp
   mv foxess_v2_temp/custom_components/foxess_v2 ./
   rm -rf foxess_v2_temp
   ```

2. Restart Home Assistant

3. Go to Settings → Devices & Services → Add Integration

4. Search for "Foxess V2"

5. Enter your credentials:
   - **Username**: `eddie@toolsinabox.com.au` (your Foxess Cloud email)
   - **Password**: Your Foxess Cloud password

## Testing the Integration

After installation, the integration will attempt to:

1. **Login** to Foxess Cloud using your credentials
2. **Discover** your inverter/device
3. **Fetch** real-time and historical data
4. **Create** sensors in Home Assistant

### If Login Fails

If the integration cannot log in, you may see errors like:
- "Invalid authentication"
- "Unable to connect"
- "No JSON response"

This likely means Foxess V2 requires browser-based authentication. In this case, we have **two solutions**:

#### Solution A: Use Selenium-based Scraping

Update the `foxess_api.py` to use Selenium WebDriver:

```python
# This requires:
pip install selenium undetected-chromedriver
```

I can help implement this if the current method doesn't work.

#### Solution B: Investigate Actual API Endpoints

If you can access your browser's Developer Tools while logged into Foxess V2:

1. Open https://www.foxesscloud.com/v2/
2. Log in with your credentials
3. Open DevTools (F12) → Network tab
4. Click around the dashboard
5. Look for API calls (usually to endpoints like `/op/v0/...` or `/api/...`)
6. Share the endpoints, headers, and request/response formats

I can then update the integration to use the correct API calls.

## Available Sensors

Once working, the integration provides these sensors:

| Sensor ID | Description | Unit |
|-----------|-------------|------|
| `sensor.foxess_pv_power` | Solar power generation | kW |
| `sensor.foxess_battery_state_of_charge` | Battery charge level | % |
| `sensor.foxess_battery_power` | Battery charge/discharge | kW |
| `sensor.foxess_grid_power` | Grid import/export | kW |
| `sensor.foxess_load_power` | Home consumption | kW |
| `sensor.foxess_inverter_power` | Inverter output | kW |
| `sensor.foxess_energy_today` | Solar energy today | kWh |
| `sensor.foxess_energy_total` | Total solar energy | kWh |
| `sensor.foxess_feed_in_energy_today` | Grid export today | kWh |
| `sensor.foxess_grid_consumption_today` | Grid import today | kWh |
| `sensor.foxess_battery_charge_today` | Battery charged today | kWh |
| `sensor.foxess_battery_discharge_today` | Battery discharged today | kWh |

## Troubleshooting

### Enable Debug Logging

Add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.foxess_v2: debug
```

Then check the logs in Settings → System → Logs

### Check Integration Status

Go to Settings → Devices & Services → Foxess V2 and check for any error messages.

### Manual API Testing

You can test the login manually:

```python
import asyncio
import aiohttp
import json

async def test():
    session = aiohttp.ClientSession()
    
    login_data = {
        "user": "eddie@toolsinabox.com.au",
        "password": "Asc221210%",
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    async with session.post(
        "https://www.foxesscloud.com/c/v0/user/login",
        json=login_data,
        headers=headers,
    ) as response:
        print(f"Status: {response.status}")
        print(f"Response: {await response.text()}")
    
    await session.close()

asyncio.run(test())
```

## Next Steps

1. **Install the integration** in Home Assistant
2. **Try to add it** with your credentials
3. **Check the logs** for any errors
4. **Report back** with:
   - Success or failure
   - Any error messages
   - Home Assistant version

If it doesn't work immediately, I can help debug and fix the API calls!

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## License

MIT License - See LICENSE file
