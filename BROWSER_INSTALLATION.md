# Foxess V2 Browser-Based Installation

## This integration uses browser automation (Playwright) instead of API

Since Foxess V2 doesn't have a public username/password API, this integration uses **real browser automation** to log in and extract data, just like a real person would.

## Prerequisites

**IMPORTANT**: You must install Playwright browser binaries in your Home Assistant environment.

### Installation Steps

1. **Install the Integration via HACS** (as normal)

2. **Install Playwright Browser**
   
   SSH into your Home Assistant or use the Terminal add-on and run:
   
   ```bash
   # For Home Assistant OS/Supervised
   docker exec homeassistant pip install playwright
   docker exec homeassistant playwright install chromium
   
   # For Home Assistant Container
   docker exec <container-name> pip install playwright
   docker exec <container-name> playwright install chromium
   
   # For Home Assistant Core (venv)
   source /srv/homeassistant/bin/activate
   pip install playwright
   playwright install chromium
   ```

3. **Restart Home Assistant**

4. **Add Integration**
   - Settings → Devices & Services → Add Integration
   - Search "Foxess V2"
   - Enter your username and password

## How It Works

1. The integration starts a headless Chrome browser
2. Navigates to https://www.foxesscloud.com/v2/
3. Logs in with your credentials
4. Extracts real-time data from the dashboard
5. Closes the browser
6. Repeats every 5 minutes

## Advantages

✅ **No API key needed** - Uses your regular login  
✅ **Works with V2** - No dependency on deprecated V1 API  
✅ **Real browser** - Handles JavaScript, sessions, cookies automatically  
✅ **Reliable** - Mimics human interaction  

## Disadvantages

⚠️ **Requires Playwright** - Extra installation step  
⚠️ **Slower** - Browser takes ~10 seconds to load and login  
⚠️ **More resources** - Uses more CPU/memory than API calls  

## Troubleshooting

### Playwright Install Fails

If `playwright install chromium` fails, try:

```bash
# Install system dependencies first
apt-get update
apt-get install -y libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2

# Then retry
playwright install chromium
```

### Login Fails

- Check your username and password are correct
- Try logging in manually at https://www.foxesscloud.com/v2/
- Check Home Assistant logs for specific errors

### Browser Not Starting

- Ensure you have enough memory (at least 512MB free)
- Check if chromium is properly installed: `playwright install --dry-run chromium`

### Sensors Show "Unavailable"

- Wait 5 minutes for first update
- Check logs: Settings → System → Logs
- Look for "foxess_v2" errors

## Alternative: API Key Method

If you can generate an API key from Foxess V2:

1. Go to foxesscloud.com/v2/ → Personal Center → API Management
2. Generate an API key
3. Use that instead (faster, no browser needed)

But if V2 doesn't offer API key generation, this browser method is the solution!

## Performance

- **First load**: ~15 seconds (browser startup + login)
- **Subsequent updates**: ~10 seconds
- **Memory usage**: ~150MB per update (browser closes after)
- **CPU usage**: Low (only during 10-second update window)

## Security

- Credentials are stored encrypted in Home Assistant
- Browser runs in headless mode (no GUI)
- All traffic goes directly to Foxess servers
- No data stored or sent elsewhere

## Support

If you encounter issues:
1. Check logs in Settings → System → Logs
2. Enable debug logging (see main README)
3. Create an issue with logs and Home Assistant version
