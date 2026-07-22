import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// Attach JWT token to every request if present
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ── Auth ──────────────────────────────────────────────────────────────────────
export const register = (data) => api.post('/auth/register', data)
export const login    = (data) => api.post('/auth/login', data)

// ── Vehicles ──────────────────────────────────────────────────────────────────
export const getVehicles    = ()         => api.get('/vehicles')
export const searchVehicles = (params)   => api.get('/vehicles/search', { params })
export const addVehicle     = (data)     => api.post('/vehicles', data)
export const updateVehicle  = (id, data) => api.put(`/vehicles/${id}`, data)
export const deleteVehicle  = (id)       => api.delete(`/vehicles/${id}`)

// ── Inventory ─────────────────────────────────────────────────────────────────
export const purchaseVehicle = (id)              => api.post(`/vehicles/${id}/purchase`)
export const restockVehicle  = (id, quantity)    => api.post(`/vehicles/${id}/restock`, { quantity })

// ── Admin ─────────────────────────────────────────────────────────────────────
export const promoteUser = (email) => api.post('/admin/promote-user', { email })
export const getUsers    = ()      => api.get('/admin/users')

