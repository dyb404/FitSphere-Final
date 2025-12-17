import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Simple request interceptor - no token needed
api.interceptors.request.use(
  (config) => {
    // No token required - simple authentication
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only handle 401 for non-login endpoints
    if (error.response?.status === 401 && !error.config?.url?.includes('/api/auth/login')) {
      localStorage.removeItem('user')
      if (window.location.pathname !== '/login') {
        setTimeout(() => {
          window.location.href = '/login'
        }, 100)
      }
    }
    return Promise.reject(error)
  }
)

// Auth API
export const login = async (email, password) => {
  try {
    const response = await api.post('/api/auth/login', { email, password })
    console.log('API login response:', response)
    console.log('Response data:', response.data)
    // Backend returns user object directly in response.data
    return response.data
  } catch (error) {
    console.error('API login error:', error)
    throw error
  }
}

export const register = async (name, email, password, role = 'client') => {
  const response = await api.post('/api/auth/register', { name, email, password, role })
  return response.data
}

// No need for getCurrentUser - we store user in localStorage

// Health Tips API
export const getHealthTips = async () => {
  const response = await api.get('/api/health-tips')
  return response.data
}

// Workouts API
export const getMyWorkouts = async (userId) => {
  const response = await api.get(`/api/workouts?user_id=${userId}`)
  return response.data
}

export const getMyCreatedWorkouts = async (userId) => {
  const response = await api.get(`/api/workouts?user_id=${userId}`)
  return response.data
}

export const createWorkout = async (data, trainerId) => {
  const response = await api.post(`/api/workouts?trainer_id=${trainerId}`, data)
  return response.data
}

export const updateWorkout = async (id, data, trainerId) => {
  const response = await api.put(`/api/workouts/${id}?trainer_id=${trainerId}`, data)
  return response.data
}

export const deleteWorkout = async (id, trainerId) => {
  const response = await api.delete(`/api/workouts/${id}?trainer_id=${trainerId}`)
  return response.data
}

// Progress Logs API
export const getMyProgressLogs = async (userId) => {
  const response = await api.get(`/api/progress?client_id=${userId}`)
  return response.data
}

export const addProgressLog = async (data, userId) => {
  const response = await api.post('/api/progress', { ...data, client_id: userId })
  return response.data
}

export const deleteProgressLog = async (id) => {
  const response = await api.delete(`/api/progress/${id}`)
  return response.data
}

// Clients API (Trainer)
export const getClients = async () => {
  const response = await api.get('/api/users/clients')
  return response.data
}

// Assignments API
export const getAssignments = async (userId) => {
  const response = await api.get(`/api/assignments?user_id=${userId}`)
  return response.data
}

export const assignWorkout = async (clientId, workoutId) => {
  const response = await api.post('/api/assignments', { client_id: clientId, workout_id: workoutId })
  return response.data
}

export const removeAssignment = async (id) => {
  const response = await api.delete(`/api/assignments/${id}`)
  return response.data
}

export default api

