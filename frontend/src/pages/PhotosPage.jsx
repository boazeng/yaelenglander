import { useState } from 'react'

const albums = ['הכל', 'ילדות', 'צבא', 'משפחה', 'פקיעין', 'חגים']

const photos = [
  { id: 1, album: 'ילדות', year: '1955', desc: 'יעל בת 5 עם אחיה בחצר בפקיעין' },
  { id: 2, album: 'פקיעין', year: '1950', desc: 'בית הכנסת העתיק בפקיעין' },
  { id: 3, album: 'צבא', year: '1967', desc: 'יעל במדים, היום הראשון בבסיס' },
  { id: 4, album: 'משפחה', year: '1975', desc: 'החתונה — יעל ואבא ביום המאושר' },
  { id: 5, album: 'משפחה', year: '1980', desc: 'עם הילד הראשון' },
  { id: 6, album: 'חגים', year: '1985', desc: 'ליל הסדר — כל המשפחה סביב השולחן' },
  { id: 7, album: 'פקיעין', year: '1960', desc: 'עץ התאנה המפורסם בחצר הבית' },
  { id: 8, album: 'משפחה', year: '1995', desc: 'יעל עם הנכד הראשון' },
  { id: 9, album: 'ילדות', year: '1958', desc: 'שיעור בבית הספר בפקיעין' },
]

export default function PhotosPage() {
  const [activeAlbum, setActiveAlbum] = useState('הכל')
  const [selectedPhoto, setSelectedPhoto] = useState(null)

  const filtered = activeAlbum === 'הכל'
    ? photos
    : photos.filter((p) => p.album === activeAlbum)

  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      {/* Main Content */}
      <div className="contentLeft">
        <div className="content-block">
          <h3>גלריית תמונות</h3>
          <p style={{ color: '#555', marginBottom: '20px' }}>
            רגעים שנשמרו לנצח — כי כל תמונה היא חלון לזמן אחר.
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '12px',
          }}>
            {filtered.map((photo) => (
              <div
                key={photo.id}
                className="img-frame"
                onClick={() => setSelectedPhoto(photo)}
                style={{ cursor: 'pointer', transition: 'box-shadow 0.3s' }}
                onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)'}
                onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
              >
                <div style={{
                  aspectRatio: '1',
                  background: 'linear-gradient(135deg, #f1f1f1, #e0dbd4)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2em',
                  color: '#b7a782',
                }}>
                  📷
                </div>
                <div style={{ padding: '6px 2px' }}>
                  <p style={{ fontSize: '11px', color: '#333', margin: 0, lineHeight: 1.4 }}>
                    {photo.desc}
                  </p>
                  <span style={{ fontSize: '10px', color: '#b5913f' }}>{photo.album} • {photo.year}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Sidebar */}
      <div className="sidebarLeft">
        <div className="sidebar-block">
          <h4>אלבומים</h4>
          <div className="sidebar-content">
            <ul className="list1">
              {albums.map((album) => (
                <li key={album}>
                  <a
                    href="#"
                    onClick={(e) => { e.preventDefault(); setActiveAlbum(album) }}
                    style={{ fontWeight: activeAlbum === album ? 700 : 400 }}
                  >
                    {album} ({photos.filter(p => album === 'הכל' || p.album === album).length})
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="sidebar-block">
          <h4>ציטוט</h4>
          <div className="sidebar-content">
            <blockquote>
              "תמונה אחת שווה אלף מילים, אבל הזיכרון שווה יותר"
            </blockquote>
            <p style={{ color: '#b5913f', fontSize: '13px', marginTop: '8px' }}>— יעל אנגלנדר</p>
          </div>
        </div>
      </div>

      {/* Lightbox */}
      {selectedPhoto && (
        <div
          onClick={() => setSelectedPhoto(null)}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.8)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px',
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{ background: '#fff', maxWidth: '600px', width: '100%', border: '4px solid #ddd' }}
          >
            <div style={{
              aspectRatio: '4/3',
              background: 'linear-gradient(135deg, #f1f1f1, #e0dbd4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '4em',
              color: '#b7a782',
            }}>
              📷
            </div>
            <div style={{ padding: '20px' }}>
              <h5 style={{ color: '#1f3442', marginBottom: '8px' }}>{selectedPhoto.desc}</h5>
              <span className="tag">{selectedPhoto.album}</span>
              <span style={{ fontSize: '12px', color: '#999', marginRight: '10px' }}>{selectedPhoto.year}</span>
              <br />
              <button
                onClick={() => setSelectedPhoto(null)}
                className="btn-main"
                style={{ marginTop: '15px' }}
              >
                סגור
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
    </div></div>
  )
}
