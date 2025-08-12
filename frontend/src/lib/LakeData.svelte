<script>
  import { onMount } from 'svelte'
  import { fetchLakeSites, fetchGreatSaltLake, fetchBearLake } from './api.js'
  
  let sites = {}
  let lakeData = null
  let loading = false
  let error = null
  let selectedLake = 'great_salt_lake'
  
  onMount(async () => {
    try {
      const sitesResponse = await fetchLakeSites()
      sites = sitesResponse.lakes
    } catch (err) {
      error = err.message
    }
  })
  
  async function loadLakeData() {
    loading = true
    error = null
    
    try {
      if (selectedLake === 'great_salt_lake') {
        lakeData = await fetchGreatSaltLake()
      } else if (selectedLake === 'bear_lake') {
        lakeData = await fetchBearLake()
      }
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }
  
  function extractLakeInfo(timeSeries) {
    if (!timeSeries || timeSeries.length === 0) return null
    
    const series = timeSeries[0]
    const siteName = series.sourceInfo?.siteName || 'Unknown Site'
    const siteCode = series.sourceInfo?.siteCode?.[0]?.value || 'Unknown'
    
    const values = series.values?.[0]?.value
    const latestValue = values && values.length > 0 ? values[values.length - 1] : null
    
    return {
      siteName,
      siteCode,
      value: latestValue?.value || 'No data',
      dateTime: latestValue?.dateTime || 'No timestamp',
      parameter: series.variable?.variableName || 'Unknown parameter',
      unit: series.variable?.unit?.unitCode || ''
    }
  }
</script>

<div class="section">
  <h2>Utah Lakes & Reservoirs</h2>
  
  <div class="info">
    <p>Total sites: {Object.values(sites).flat().length}</p>
    
    <div class="lake-selector">
      <label>
        <input type="radio" bind:group={selectedLake} value="great_salt_lake" />
        Great Salt Lake ({sites.great_salt_lake?.length || 0} sites)
      </label>
      <label>
        <input type="radio" bind:group={selectedLake} value="bear_lake" />
        Bear Lake ({sites.bear_lake?.length || 0} sites)
      </label>
    </div>
    
    <button on:click={loadLakeData} disabled={loading}>
      {loading ? 'Loading...' : `Load ${selectedLake.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())} Data`}
    </button>
  </div>
  
  {#if error}
    <div class="error">Error: {error}</div>
  {/if}
  
  {#if lakeData}
    <div class="data-grid">
      {#each lakeData.value?.timeSeries || [] as series}
        {@const info = extractLakeInfo([series])}
        {#if info}
          <div class="data-card">
            <h3>{info.siteName}</h3>
            <p class="site-code">Site: {info.siteCode}</p>
            <p class="parameter">{info.parameter}</p>
            <p class="value">{info.value} {info.unit}</p>
            <p class="timestamp">{new Date(info.dateTime).toLocaleString()}</p>
          </div>
        {/if}
      {/each}
      
      {#if (!lakeData.value?.timeSeries || lakeData.value.timeSeries.length === 0)}
        <div class="no-data">
          No current data available for {selectedLake.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .section {
    margin: 2em 0;
    padding: 1em;
    border: 1px solid #333;
    border-radius: 8px;
    background-color: #1a1a1a;
  }

  .info {
    margin: 1em 0;
  }

  .lake-selector {
    margin: 1em 0;
    display: flex;
    gap: 1em;
    flex-wrap: wrap;
  }

  .lake-selector label {
    display: flex;
    align-items: center;
    gap: 0.5em;
    cursor: pointer;
  }

  .data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin-top: 1em;
  }

  .data-card {
    padding: 1em;
    border: 1px solid #444;
    border-radius: 6px;
    background-color: #2a2a2a;
  }

  .data-card h3 {
    margin: 0 0 0.5em 0;
    color: #3b82f6;
    font-size: 1.1em;
  }

  .site-code {
    color: #888;
    font-size: 0.9em;
    margin: 0.25em 0;
  }

  .parameter {
    color: #ccc;
    font-weight: bold;
    margin: 0.5em 0;
  }

  .value {
    font-size: 1.5em;
    font-weight: bold;
    color: #3b82f6;
    margin: 0.5em 0;
  }

  .timestamp {
    color: #888;
    font-size: 0.8em;
    margin: 0.25em 0;
  }

  .no-data {
    color: #fbbf24;
    padding: 2em;
    text-align: center;
    background-color: #2a2a1a;
    border-radius: 6px;
    border: 1px dashed #444;
  }

  .error {
    color: #ef4444;
    padding: 1em;
    background-color: #2a1a1a;
    border-radius: 4px;
    margin: 1em 0;
  }

  button {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 0.8em 1.5em;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
  }

  button:hover {
    background-color: #2563eb;
  }

  button:disabled {
    background-color: #666;
    cursor: not-allowed;
  }
</style>