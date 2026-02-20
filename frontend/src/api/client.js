/**
 * API client — fetch wrapper with JWT token handling.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5003'

function getToken() {
  return localStorage.getItem('auth_token')
}

async function request(path, options = {}) {
  const token = getToken()
  const headers = { ...options.headers }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  // Don't set Content-Type for FormData (browser sets it with boundary)
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'שגיאת שרת' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }

  return res.json()
}

// Auth
export function login(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function googleLogin(credential) {
  return request('/auth/google', {
    method: 'POST',
    body: JSON.stringify({ credential }),
  })
}

export function getMe() {
  return request('/auth/me')
}

// Photos
export function getPhotos({ tags, limit = 50, offset = 0 } = {}) {
  const params = new URLSearchParams()
  if (tags) params.set('tags', tags)
  if (limit) params.set('limit', limit)
  if (offset) params.set('offset', offset)
  return request(`/photos?${params}`)
}

export function getPhoto(id) {
  return request(`/photos/${id}`)
}

export function uploadPhoto(file, caption) {
  const formData = new FormData()
  formData.append('file', file)
  if (caption) formData.append('caption', caption)
  return request('/photos/upload', { method: 'POST', body: formData })
}

export function updatePhotoTags(photoId, tags) {
  return request(`/photos/${photoId}/tags`, {
    method: 'PATCH',
    body: JSON.stringify(tags),
  })
}

export function deletePhoto(id) {
  return request(`/photos/${id}`, { method: 'DELETE' })
}

export function getTags() {
  return request('/photos/tags')
}

export { API_BASE }
