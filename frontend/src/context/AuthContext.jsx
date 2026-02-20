import { createContext, useContext, useState, useEffect } from 'react'
import { login as apiLogin, googleLogin as apiGoogleLogin, getMe } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      getMe()
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('auth_token')
          setUser(null)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  async function login(email, password) {
    const data = await apiLogin(email, password)
    localStorage.setItem('auth_token', data.token)
    setUser({ name: data.name, role: data.role })
    return data
  }

  async function googleLogin(credential) {
    const data = await apiGoogleLogin(credential)
    localStorage.setItem('auth_token', data.token)
    setUser({ name: data.name, role: data.role })
    return data
  }

  function logout() {
    localStorage.removeItem('auth_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, googleLogin, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be inside AuthProvider')
  return ctx
}
