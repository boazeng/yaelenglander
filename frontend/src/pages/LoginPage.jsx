import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/upload')
    } catch (err) {
      setError(err.message || 'שגיאה בכניסה')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      <div className="contentLeft">
        <div className="content-block">
          <h3>כניסה לאזור המשפחה</h3>
          <p style={{ color: '#555', marginBottom: '24px' }}>
            רק בני משפחה מאושרים יכולים להעלות תמונות ותוכן.
          </p>

          <form onSubmit={handleSubmit} style={{ maxWidth: '400px' }}>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 600, color: '#1f3442' }}>
                אימייל
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{
                  width: '100%', padding: '10px 12px', border: '1px solid #ccc',
                  borderRadius: '4px', fontSize: '15px', direction: 'ltr',
                }}
              />
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', marginBottom: '6px', fontWeight: 600, color: '#1f3442' }}>
                סיסמה
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{
                  width: '100%', padding: '10px 12px', border: '1px solid #ccc',
                  borderRadius: '4px', fontSize: '15px', direction: 'ltr',
                }}
              />
            </div>

            {error && (
              <div style={{ color: '#c0392b', marginBottom: '16px', fontSize: '14px' }}>
                {error}
              </div>
            )}

            <button
              type="submit"
              className="btn-main"
              disabled={loading}
              style={{ width: '100%', padding: '12px', fontSize: '16px' }}
            >
              {loading ? 'מתחבר...' : 'כניסה'}
            </button>
          </form>
        </div>
      </div>

      <div className="sidebarLeft">
        <div className="sidebar-block">
          <h4>למה נדרשת כניסה?</h4>
          <div className="sidebar-content">
            <p>
              כדי לשמור על פרטיות המשפחה, רק בני משפחה מאושרים יכולים להעלות תמונות וסיפורים.
              צפייה בתוכן פתוחה לכולם.
            </p>
          </div>
        </div>
      </div>
    </div>
    </div></div>
  )
}
