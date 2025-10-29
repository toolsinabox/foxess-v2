"""Foxess V2 Browser-based scraper using Playwright."""
import logging
import asyncio
import json
import re
from typing import Dict, Any

_LOGGER = logging.getLogger(__name__)

# Playwright will be installed as optional dependency
try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    _LOGGER.warning("Playwright not available. Install with: pip install playwright && playwright install chromium")


class FoxessV2Browser:
    """Browser automation for Foxess V2."""

    def __init__(self, username: str, password: str):
        """Initialize browser scraper."""
        self.username = username
        self.password = password
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    async def start_browser(self):
        """Start headless browser."""
        if not PLAYWRIGHT_AVAILABLE:
            raise Exception("Playwright not installed. Run: pip install playwright && playwright install chromium")

        self.playwright = await async_playwright().start()
        
        # Launch browser in headless mode
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        # Create context with realistic browser settings
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        self.page = await self.context.new_page()
        _LOGGER.debug("Browser started successfully")

    async def login(self) -> bool:
        """Login to Foxess V2 using browser automation."""
        try:
            if not self.page:
                await self.start_browser()

            _LOGGER.debug("Navigating to Foxess V2 login page...")
            await self.page.goto('https://www.foxesscloud.com/v2/', wait_until='networkidle')
            
            # Wait for page to load
            await asyncio.sleep(3)

            # Find and fill username field
            _LOGGER.debug("Entering username...")
            await self.page.fill('input[type="text"], input[type="email"], input[placeholder*="mail"], input[placeholder*="user"]', self.username)
            
            # Find and fill password field
            _LOGGER.debug("Entering password...")
            await self.page.fill('input[type="password"]', self.password)
            
            # Wait a bit
            await asyncio.sleep(1)

            # Click login button
            _LOGGER.debug("Clicking login button...")
            await self.page.click('button:has-text("Log In"), button:has-text("Login"), button[type="submit"]')
            
            # Wait for navigation after login
            await asyncio.sleep(5)
            
            # Check if login successful by checking URL or page content
            current_url = self.page.url
            _LOGGER.debug(f"After login URL: {current_url}")
            
            if 'login' not in current_url.lower():
                _LOGGER.info("Login successful!")
                return True
            else:
                _LOGGER.error("Login appears to have failed")
                return False

        except Exception as err:
            _LOGGER.error(f"Error during browser login: {err}")
            raise

    async def get_data(self) -> Dict[str, Any]:
        """Get data by scraping the dashboard."""
        try:
            if not self.page:
                raise Exception("Browser not initialized")

            _LOGGER.debug("Extracting data from dashboard...")
            
            # Wait for dashboard to load
            await asyncio.sleep(3)
            
            # Execute JavaScript to extract data from the page
            data = await self.page.evaluate("""
                () => {
                    const result = {};
                    
                    // Extract all text data from the dashboard
                    const textData = {};
                    document.querySelectorAll('[class*="value"], [class*="data"], [class*="power"]').forEach((el, i) => {
                        const text = el.textContent.trim();
                        if (text && text.length < 50) {
                            textData[text] = text;
                        }
                    });
                    
                    // Parse known patterns
                    for (const [key, value] of Object.entries(textData)) {
                        // PV Power
                        if (key.includes('kW') && !key.includes('Today') && !key.includes('Total')) {
                            const match = key.match(/([0-9.]+)kW/);
                            if (match) result.pv_power = parseFloat(match[1]);
                        }
                        
                        // Battery SOC
                        if (key.includes('SOC:')) {
                            const match = key.match(/SOC:([0-9]+)%/);
                            if (match) result.battery_soc = parseFloat(match[1]);
                        }
                        
                        // Today/Total patterns
                        if (key.includes('PV Yield') && key.includes('/')) {
                            const match = key.match(/([0-9.]+)\/ ([0-9.]+)/);
                            if (match) {
                                result.energy_today = parseFloat(match[1]);
                                result.energy_total = parseFloat(match[2]);
                            }
                        }
                        
                        if (key.includes('Feed-in') && key.includes('/')) {
                            const match = key.match(/([0-9.]+)\/ ([0-9.]+)/);
                            if (match) {
                                result.feed_in_energy_today = parseFloat(match[1]);
                            }
                        }
                        
                        if (key.includes('Consumption') && key.includes('/')) {
                            const match = key.match(/([0-9.]+)\/ ([0-9.]+)/);
                            if (match) {
                                result.grid_consumption_today = parseFloat(match[1]);
                            }
                        }
                    }
                    
                    return result;
                }
            """)
            
            _LOGGER.debug(f"Extracted data: {data}")
            
            # Ensure we have at least some data
            if not data:
                # Fallback: get any visible numbers
                data = await self._extract_fallback_data()
            
            return data

        except Exception as err:
            _LOGGER.error(f"Error getting data: {err}")
            raise

    async def _extract_fallback_data(self) -> Dict[str, Any]:
        """Fallback method to extract data."""
        try:
            page_text = await self.page.content()
            
            # Simple regex patterns to find data
            import re
            
            data = {}
            
            # Find SOC
            soc_match = re.search(r'SOC:(\d+)%', page_text)
            if soc_match:
                data['battery_soc'] = float(soc_match.group(1))
            
            # Find power values
            power_matches = re.findall(r'(\d+\.?\d*)kW', page_text)
            if power_matches:
                data['pv_power'] = float(power_matches[0])
            
            return data
        except:
            return {}

    def _normalize_data(self, raw_data: Dict) -> Dict[str, Any]:
        """Normalize scraped data to match our sensor format."""
        normalized = {}
        
        # Map common field names to our format
        field_mapping = {
            'pvpower': 'pv_power',
            'pv_power': 'pv_power',
            'soc': 'battery_soc',
            'battery_soc': 'battery_soc',
            'batpower': 'battery_power',
            'battery_power': 'battery_power',
            'gridpower': 'grid_power',
            'grid_power': 'grid_power',
            'loadpower': 'load_power',
            'load_power': 'load_power',
            'invpower': 'inverter_power',
            'inverter_power': 'inverter_power',
        }
        
        for key, value in raw_data.items():
            # Convert key to lowercase and remove spaces
            clean_key = key.lower().replace(' ', '_').replace('-', '_')
            
            # Map to our field names
            our_key = field_mapping.get(clean_key, clean_key)
            
            # Try to convert to float
            try:
                if isinstance(value, str):
                    # Remove units (kW, %, etc.)
                    value_clean = value.replace('kW', '').replace('kWh', '').replace('%', '').strip()
                    normalized[our_key] = float(value_clean)
                else:
                    normalized[our_key] = float(value)
            except (ValueError, TypeError):
                normalized[our_key] = value
        
        return normalized

    async def close(self):
        """Close browser."""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            _LOGGER.debug("Browser closed")
        except Exception as err:
            _LOGGER.error(f"Error closing browser: {err}")
