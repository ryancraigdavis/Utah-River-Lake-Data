<script>
  import { onMount } from 'svelte'
  import { fetchRiverSites, fetchRiverCurrent } from './api.js'
  
  let sites = []
  let riverData = null
  let loading = false
  let error = null
  
  onMount(async () => {
    try {
      const sitesResponse = await fetchRiverSites()
      sites = sitesResponse.sites
    } catch (err) {
      error = err.message
    }
  })
  
  async function loadRiverData() {
    loading = true
    error = null
    
    try {
      riverData = await fetchRiverCurrent()
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }
  
  function extractRiverInfo(timeSeries) {
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
      parameter: series.variable?.variableName || 'Unknown parameter'
    }
  }
</script>

<div class="section">
  <h2>Utah Rivers</h2>
  
  <div class="info">
    <p>Monitoring {sites.length} river sites</p>
    <button on:click={loadRiverData} disabled={loading}>
      {loading ? 'Loading...' : 'Load Current River Data'}
    </button>
  </div>
  
  {#if error}
    <div class="error">Error: {error}</div>
  {/if}
  
  {#if riverData}
    <div class="data-grid">
      {#each riverData.value?.timeSeries || [] as series}
        {@const info = extractRiverInfo([series])}
        {#if info}
          <div class="data-card">
            <h3>{info.siteName}</h3>
            <p class="site-code">Site: {info.siteCode}</p>
            <p class="parameter">{info.parameter}</p>
            <p class="value">{info.value}</p>
            <p class="timestamp">{new Date(info.dateTime).toLocaleString()}</p>
          </div>
        {/if}
      {/each}
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
    color: #ff3e00;
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
    color: #4ade80;
    margin: 0.5em 0;
  }

  .timestamp {
    color: #888;
    font-size: 0.8em;
    margin: 0.25em 0;
  }

  .error {
    color: #ef4444;
    padding: 1em;
    background-color: #2a1a1a;
    border-radius: 4px;
    margin: 1em 0;
  }

  button {
    background-color: #ff3e00;
    color: white;
    border: none;
    padding: 0.8em 1.5em;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
  }

  button:hover {
    background-color: #cc3200;
  }

  button:disabled {
    background-color: #666;
    cursor: not-allowed;
  }
</style>