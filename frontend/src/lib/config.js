// Environment configuration
const isDev = import.meta.env.DEV
const prodApiUrl = import.meta.env.VITE_API_URL || 'http://104.173.199.40:55223/api/v1'

export const API_BASE = isDev 
  ? 'http://localhost:8000/api/v1'
  : prodApiUrl