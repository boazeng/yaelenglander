import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/', label: 'ראשי' },
  { path: '/pekiin', label: 'פקיעין', children: [
    { path: '/pekiin?section=history', label: 'ההיסטוריה של פקיעין' },
    { path: '/pekiin?section=places', label: 'מקומות חשובים' },
    { path: '/pekiin?section=timeline', label: 'ציר הזמן' },
  ]},
  { path: '/stories', label: 'סיפורים', children: [
    { path: '/stories?cat=childhood', label: 'ילדות בפקיעין' },
    { path: '/stories?cat=army', label: 'צבא' },
    { path: '/stories?cat=family', label: 'משפחה' },
    { path: '/stories?cat=daily', label: 'חיי יום יום' },
  ]},
  { path: '/recipes', label: 'מתכונים', children: [
    { path: '/recipes?cat=main', label: 'עיקריות' },
    { path: '/recipes?cat=desserts', label: 'קינוחים' },
    { path: '/recipes?cat=shabbat', label: 'שבת וחגים' },
    { path: '/recipes?cat=salads', label: 'סלטים ומזות' },
  ]},
  { path: '/photos', label: 'תמונות', children: [
    { path: '/photos?album=childhood', label: 'ילדות' },
    { path: '/photos?album=army', label: 'צבא' },
    { path: '/photos?album=family', label: 'משפחה' },
    { path: '/photos?album=pekiin', label: 'פקיעין' },
    { path: '/photos?album=holidays', label: 'חגים' },
  ]},
]

export default function Header() {
  const location = useLocation()

  return (
    <header className="site-header">
      <div className="container" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 2%',
      }}>
        {/* Tree Logo + Title */}
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '12px', textDecoration: 'none', padding: '15px 0' }}>
          <img
            src="/images/tree-only.png"
            alt="עץ שורשים"
            style={{ height: '100px', width: 'auto' }}
          />
          <div>
            <div style={{
              fontFamily: "'Frank Ruhl Libre', 'Cormorant Garamond', serif",
              color: '#d2a01a',
              fontSize: '44px',
              fontWeight: 700,
              lineHeight: 1.1,
              letterSpacing: '-1px',
            }}>
              יעל אנגלנדר
            </div>
            <div style={{
              fontFamily: "'Frank Ruhl Libre', 'Cormorant Garamond', serif",
              color: '#ffffff',
              fontSize: '22px',
              fontWeight: 400,
              lineHeight: 1.3,
            }}>
              כי האדם עץ השדה
            </div>
          </div>
        </Link>

        {/* Navigation */}
        <nav>
          <ul className="slimmenu">
            {navItems.map((item) => (
              <li key={item.path} className={item.children ? 'has-dropdown' : ''}>
                <Link
                  to={item.path}
                  className={location.pathname === item.path ? 'active' : ''}
                >
                  {item.label}
                  {item.children && <span className="dropdown-arrow">&#9662;</span>}
                </Link>
                {item.children && (
                  <ul className="dropdown-menu">
                    {item.children.map((child) => (
                      <li key={child.path}>
                        <Link to={child.path}>{child.label}</Link>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  )
}
