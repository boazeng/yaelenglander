import { API_BASE } from '../../api/client'

export default function Lightbox({ photo, onClose }) {
  if (!photo) return null

  return (
    <div
      onClick={onClose}
      style={{
        position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)',
        zIndex: 1000, display: 'flex', alignItems: 'center',
        justifyContent: 'center', padding: '20px',
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: '#fff', maxWidth: '700px', width: '100%',
          borderRadius: '8px', overflow: 'hidden',
        }}
      >
        <img
          src={`${API_BASE}${photo.file_url}`}
          alt={photo.caption || ''}
          style={{ width: '100%', maxHeight: '500px', objectFit: 'contain', background: '#f5f5f5' }}
        />

        <div style={{ padding: '20px' }}>
          {photo.caption && (
            <h5 style={{ color: '#1f3442', marginBottom: '10px', fontSize: '16px' }}>
              {photo.caption}
            </h5>
          )}

          {/* Tags */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
            {photo.tags.map((tag, i) => (
              <span key={i} className="tag" style={{ padding: '3px 10px', fontSize: '12px' }}>
                {tag}
              </span>
            ))}
          </div>

          {/* Meta info */}
          <div style={{ fontSize: '12px', color: '#999', display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            {photo.uploaded_by && <span>העלה: {photo.uploaded_by}</span>}
            {photo.uploaded_at && (
              <span>{new Date(photo.uploaded_at).toLocaleDateString('he-IL')}</span>
            )}
            {photo.width && photo.height && (
              <span>{photo.width}×{photo.height}</span>
            )}
          </div>

          <button
            onClick={onClose}
            className="btn-main"
            style={{ marginTop: '16px' }}
          >
            סגור
          </button>
        </div>
      </div>
    </div>
  )
}
