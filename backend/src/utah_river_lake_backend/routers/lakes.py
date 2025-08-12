"""Lake and reservoir data endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..usgs_client import USGSClient

router = APIRouter()

# Utah lake and reservoir sites
UTAH_LAKES = {
    "great_salt_lake": [
        "10010000",  # Great Salt Lake at Saltair Boat Harbor, UT
        "10010100",  # Great Salt Lake Near Saline, UT
        "10010050",  # Great Salt Lake at Promontory Point, Utah
        "10010020"   # Gsl Breach at Lakeside, UT
    ],
    "bear_lake": [
        "415941111175401",  # Bear Lake nr east shore 0.4 mi S of UT-ID border
        "420106111225701"   # Bear Lake nr west shore 1.5 mi SE of Fish Haven ID
    ],
    "reservoirs": [
        "404641111483901",  # Red Butte Reservoir - West
        "10163000"          # Provo River at Provo (near Utah Lake)
    ]
}

# Flatten all lake sites for convenience
ALL_LAKE_SITES = []
for sites in UTAH_LAKES.values():
    ALL_LAKE_SITES.extend(sites)


async def get_usgs_client():
    """Dependency to get USGS client."""
    client = USGSClient()
    try:
        yield client
    finally:
        await client.close()


@router.get("/sites")
async def get_lake_sites():
    """Get list of available lake and reservoir sites."""
    return {
        "lakes": UTAH_LAKES,
        "all_sites": ALL_LAKE_SITES,
        "total_count": len(ALL_LAKE_SITES)
    }


@router.get("/current")
async def get_current_lake_data(
    sites: Optional[str] = None,
    lake_type: Optional[str] = None,
    client: USGSClient = Depends(get_usgs_client)
):
    """
    Get current lake/reservoir data for all or specified sites.
    
    Args:
        sites: Comma-separated list of site codes (optional)
        lake_type: Filter by lake type (great_salt_lake, bear_lake, reservoirs)
    """
    try:
        if sites:
            site_list = sites.split(",")
        elif lake_type and lake_type in UTAH_LAKES:
            site_list = UTAH_LAKES[lake_type]
        else:
            site_list = ALL_LAKE_SITES
            
        data = await client.get_lake_data(site_list)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching current lake data: {str(e)}")


@router.get("/current/{site_code}")
async def get_lake_site_current_data(
    site_code: str,
    client: USGSClient = Depends(get_usgs_client)
):
    """Get current data for a specific lake/reservoir site."""
    try:
        data = await client.get_lake_data([site_code])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lake site data: {str(e)}")


@router.get("/historical")
async def get_historical_lake_data(
    sites: Optional[str] = None,
    lake_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    client: USGSClient = Depends(get_usgs_client)
):
    """
    Get historical lake/reservoir data.
    
    Args:
        sites: Comma-separated list of site codes (optional)
        lake_type: Filter by lake type (great_salt_lake, bear_lake, reservoirs)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format  
        period: Period code (e.g., P30D, P1Y)
    """
    try:
        if sites:
            site_list = sites.split(",")
        elif lake_type and lake_type in UTAH_LAKES:
            site_list = UTAH_LAKES[lake_type]
        else:
            site_list = ALL_LAKE_SITES
            
        data = await client.get_lake_historical(
            site_list, 
            start_date=start_date,
            end_date=end_date,
            period=period
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching historical lake data: {str(e)}")


@router.get("/periods")
async def get_lake_common_periods(
    sites: Optional[str] = None,
    lake_type: Optional[str] = None,
    client: USGSClient = Depends(get_usgs_client)
):
    """Get lake data for common time periods (last year, month, 5 years)."""
    try:
        if sites:
            site_list = sites.split(",")
        elif lake_type and lake_type in UTAH_LAKES:
            site_list = UTAH_LAKES[lake_type]
        else:
            site_list = ALL_LAKE_SITES
            
        lake_params = "00065,00062,00054,00010"  # Lake-specific parameters
        data = await client.get_historical_periods(site_list, parameter_codes=lake_params)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lake period data: {str(e)}")


@router.get("/great-salt-lake")
async def get_great_salt_lake_data(
    client: USGSClient = Depends(get_usgs_client)
):
    """Get current data specifically for Great Salt Lake monitoring sites."""
    try:
        data = await client.get_lake_data(UTAH_LAKES["great_salt_lake"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Great Salt Lake data: {str(e)}")


@router.get("/bear-lake")
async def get_bear_lake_data(
    client: USGSClient = Depends(get_usgs_client)
):
    """Get current data specifically for Bear Lake monitoring sites."""
    try:
        data = await client.get_lake_data(UTAH_LAKES["bear_lake"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Bear Lake data: {str(e)}")