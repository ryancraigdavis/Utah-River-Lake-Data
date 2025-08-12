<script>
  import RiverData from './lib/RiverData.svelte'
  import LakeData from './lib/LakeData.svelte'
  import { onMount } from 'svelte'
  
  let apiStatus = 'checking...'
  
  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      const data = await response.json()
      apiStatus = data.status === 'healthy' ? 'connected' : 'error'
    } catch (error) {
      apiStatus = 'disconnected'
    }
  })
</script>

<main>
  <h1>Utah River & Lake Data</h1>
  
  <div class="status">
    Backend API: <span class="status-{apiStatus}">{apiStatus}</span>
  </div>
  
  <div class="tabs">
    <RiverData />
    <LakeData />
  </div>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 1200px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
    margin-bottom: 0.5em;
  }

  .status {
    margin: 1em 0;
    font-size: 1.2em;
  }

  .status-connected {
    color: #4ade80;
  }

  .status-disconnected {
    color: #ef4444;
  }

  .status-checking {
    color: #fbbf24;
  }

  .tabs {
    margin-top: 2em;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>