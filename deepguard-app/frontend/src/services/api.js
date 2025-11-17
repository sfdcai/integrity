import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
})

export const fetchWells = () => api.get('/wells').then(res => res.data)
export const fetchWell = (id) => api.get(`/wells/${id}`).then(res => res.data)
export const fetchTasks = () => api.get('/tasks').then(res => res.data)
export const createMeasurement = (annulusId, payload) => api.post(`/annuli/${annulusId}/measurements`, payload).then(res => res.data)
export const createWell = (payload) => api.post('/wells', payload).then(res => res.data)
export const fetchSchematic = (wellId) => api.get(`/wells/${wellId}/schematic`).then(res => res.data)

export default api
