"""USGS API client for fetching river and lake data."""

import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class USGSClient:
    """Client for USGS Water Services API."""
    
    BASE_URL_IV = "https://waterservices.usgs.gov/nwis/iv"
    BASE_URL_DV = "https://nwis.waterservices.usgs.gov/nwis/dv"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def get_current_data(self, site_codes: List[str]) -> Dict:
        """
        Get current instantaneous data for river sites.
        
        Args:
            site_codes: List of USGS site codes
            
        Returns:
            Dictionary containing the API response
        """
        params = {
            "format": "json",
            "sites": ",".join(site_codes),
            "parameterCd": "00060,00010",  # Flow and temperature
            "siteStatus": "active"
        }
        
        response = await self.client.get(self.BASE_URL_IV, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_daily_data(
        self, 
        site_codes: List[str], 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None
    ) -> Dict:
        """
        Get daily historical data for river sites.
        
        Args:
            site_codes: List of USGS site codes
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            period: Period code (e.g., P30D for 30 days, P1Y for 1 year)
            
        Returns:
            Dictionary containing the API response
        """
        params = {
            "format": "json",
            "sites": ",".join(site_codes),
            "parameterCd": "00060,00010",
            "siteStatus": "active"
        }
        
        if period:
            params["period"] = period
        else:
            if start_date:
                params["startDT"] = start_date
            if end_date:
                params["endDT"] = end_date
        
        response = await self.client.get(self.BASE_URL_DV, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_site_data(self, site_code: str) -> Dict:
        """Get current data for a single site."""
        return await self.get_current_data([site_code])
    
    async def get_historical_periods(self, site_codes: List[str]) -> Dict:
        """Get historical data for common periods used in the frontend."""
        periods = {
            "last_year": "P365D",
            "last_month": "P30D", 
            "last_5_years": "P1825D"
        }
        
        results = {}
        for period_name, period_code in periods.items():
            try:
                data = await self.get_daily_data(site_codes, period=period_code)
                results[period_name] = data
            except Exception as e:
                results[period_name] = {"error": str(e)}
        
        return results