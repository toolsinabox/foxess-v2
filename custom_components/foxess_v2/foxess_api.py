"""Foxess V2 API Client - calls local add-on."""
import logging
import aiohttp
from typing import Dict, Any

_LOGGER = logging.getLogger(__name__)


class FoxessV2API:
    """Foxess V2 API Client using local add-on."""

    def __init__(self, username: str, password: str, hass):
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.hass = hass
        self.addon_url = "http://localhost:8099"
        self.session = None

    async def login(self) -> bool:
        """Check if add-on is running."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Check add-on health
            async with self.session.get(f"{self.addon_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    _LOGGER.info("Foxess V2 add-on is running")
                    return True
                else:
                    raise Exception("Add-on not responding")
        
        except Exception as err:
            _LOGGER.error(f"Cannot connect to Foxess V2 add-on. Make sure the add-on is installed and running: {err}")
            raise Exception("Foxess V2 add-on not found. Please install and start the 'Foxess V2 Scraper' add-on first.")

    async def get_data(self) -> Dict[str, Any]:
        """Get data from add-on."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Get data from add-on
            async with self.session.get(f"{self.addon_url}/data", timeout=aiohttp.ClientTimeout(total=30)) as response:
                result = await response.json()
                
                if result.get('status') == 'success':
                    data = result.get('data', {})
                    _LOGGER.debug(f"Retrieved data from add-on: {data}")
                    return data
                else:
                    raise Exception(f"Add-on returned error: {result.get('message')}")
        
        except Exception as err:
            _LOGGER.error(f"Error getting data from add-on: {err}")
            raise

    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()
