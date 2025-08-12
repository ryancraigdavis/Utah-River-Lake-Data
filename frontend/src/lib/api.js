import { API_BASE } from './config.js'

export async function fetchRiverSites() {
  const response = await fetch(`${API_BASE}/rivers/sites`)
  if (!response.ok) throw new Error('Failed to fetch river sites')
  return response.json()
}

export async function fetchRiverCurrent(sites = null) {
  const url = sites 
    ? `${API_BASE}/rivers/current?sites=${sites}`
    : `${API_BASE}/rivers/current`
  
  const response = await fetch(url)
  if (!response.ok) throw new Error('Failed to fetch river data')
  return response.json()
}

export async function fetchLakeSites() {
  const response = await fetch(`${API_BASE}/lakes/sites`)
  if (!response.ok) throw new Error('Failed to fetch lake sites')
  return response.json()
}

export async function fetchLakeCurrent(sites = null, lakeType = null) {
  let url = `${API_BASE}/lakes/current`
  const params = new URLSearchParams()
  
  if (sites) params.append('sites', sites)
  if (lakeType) params.append('lake_type', lakeType)
  
  if (params.toString()) {
    url += `?${params.toString()}`
  }
  
  const response = await fetch(url)
  if (!response.ok) throw new Error('Failed to fetch lake data')
  return response.json()
}

export async function fetchGreatSaltLake() {
  const response = await fetch(`${API_BASE}/lakes/great-salt-lake`)
  if (!response.ok) throw new Error('Failed to fetch Great Salt Lake data')
  return response.json()
}

export async function fetchBearLake() {
  const response = await fetch(`${API_BASE}/lakes/bear-lake`)
  if (!response.ok) throw new Error('Failed to fetch Bear Lake data')
  return response.json()
}