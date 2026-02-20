import { API_BASE } from '../../api/client'

export default function PhotoCard({ photo, onClick }) {
  return (
    <div
      className="img-frame"
      onClick={() => onClick?.(photo)}
      style={{ cursor: 'pointer', transition: 'box-shadow 0.3s' }}
      onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)'}
      onMouseLeave={(e) => e.currentTarget.style.boxShadow = 'none'}
    >
      <div style={{ aspectRatio: '1', overflow: 'hidden', background: '#f1f1f1' }}>
        <img
          src={`${API_BASE}${photo.thumb_url}`}
          alt={photo.caption || ''}
          loading="lazy"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          onError={(e) => {
            e.target.style.display = 'none'
            e.target.parentElement.innerHTML = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:2em;color:#b7a782">📷</div>'
          }}
        />
      </div>
      <div style={{ padding: '6px 2px' }}>
        {photo.caption && (
          <p style={{ fontSize: '11px', color: '#333', margin: 0, lineHeight: 1.4 }}>
            {photo.caption}
          </p>
        )}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '3px', marginTop: '4px' }}>
          {photo.tags.slice(0, 3).map((tag, i) => (
            <span key={i} style={{
              fontSize: '10px', background: '#f0ebe0', color: '#8a7340',
              padding: '1px 6px', borderRadius: '3px',
            }}>
              {tag}
            </span>
          ))}
          {photo.tags.length > 3 && (
            <span style={{ fontSize: '10px', color: '#999' }}>
              +{photo.tags.length - 3}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
