"""River and lake data endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..usgs_client import USGSClient

router = APIRouter()

# Utah river sites from the frontend
UTAH_SITES = [
    "10109000",  # Weber River at Echo
    "10168000",  # Jordan River at 1700 South at Salt Lake City
    "10171000",  # Jordan River at 9000 South at Sandy
    "10234500",  # Sevier River near Lynndyl
    "10258500",  # Amargosa Creek near Beatty
    "09261000",  # Green River near Jensen
    "09379500",  # San Juan River at Bluff
    "10346000",  # Truckee River at Tahoe City
    "09315000",  # Green River at Green River
    "10128500"   # Bear River at Bordeaux
]


async def get_usgs_client():
    """Dependency to get USGS client."""
    client = USGSClient()
    try:
        yield client
    finally:
        await client.close()


@router.get("/sites")
async def get_sites():
    """Get list of available river sites."""
    return {
        "sites": UTAH_SITES,
        "count": len(UTAH_SITES)
    }


@router.get("/current")
async def get_current_data(
    sites: Optional[str] = None,
    client: USGSClient = Depends(get_usgs_client)
):
    """
    Get current river data for all or specified sites.
    
    Args:
        sites: Comma-separated list of site codes (optional)
    """
    try:
        site_list = sites.split(",") if sites else UTAH_SITES
        data = await client.get_current_data(site_list)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching current data: {str(e)}")


@router.get("/current/{site_code}")
async def get_site_current_data(
    site_code: str,
    client: USGSClient = Depends(get_usgs_client)
):
    """Get current data for a specific site."""
    try:
        data = await client.get_site_data(site_code)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching site data: {str(e)}")


@router.get("/historical")
async def get_historical_data(
    sites: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    client: USGSClient = Depends(get_usgs_client)
):
    """
    Get historical river data.
    
    Args:
        sites: Comma-separated list of site codes (optional)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        period: Period code (e.g., P30D, P1Y)
    """
    try:
        site_list = sites.split(",") if sites else UTAH_SITES
        data = await client.get_daily_data(
            site_list, 
            start_date=start_date,
            end_date=end_date,
            period=period
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical data: {str(e)}")


@router.get("/periods")
async def get_common_periods(
    sites: Optional[str] = None,
    client: USGSClient = Depends(get_usgs_client)
):
    """Get data for common time periods (last year, month, 5 years)."""
    try:
        site_list = sites.split(",") if sites else UTAH_SITES
        data = await client.get_historical_periods(site_list)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching period data: {str(e)}")