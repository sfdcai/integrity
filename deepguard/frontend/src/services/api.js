import axios from 'axios'

const fallbackHost = typeof window !== 'undefined'
  ? `${window.location.protocol}//${window.location.hostname}:8000`
  : 'http://localhost:8000'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || fallbackHost
})

export const setToken = (token) => {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export const login = async (email, password) => {
  const data = new URLSearchParams({ username: email, password })
  const res = await api.post('/auth/login', data)
  const { access_token } = res.data
  setToken(access_token)
  return access_token
}

export const fetchWells = () => api.get('/api/wells').then(r => r.data)
export const fetchWell = (id) => api.get(`/api/wells/${id}`).then(r => r.data)
export const fetchSchematic = (id) => api.get(`/api/wells/${id}/schematic`).then(r => r.data)
export default api
