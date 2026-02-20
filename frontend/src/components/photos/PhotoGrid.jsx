import PhotoCard from './PhotoCard'

export default function PhotoGrid({ photos, onPhotoClick }) {
  if (!photos.length) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
        <div style={{ fontSize: '3em', marginBottom: '12px' }}>📷</div>
        <p>אין תמונות עדיין</p>
      </div>
    )
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: '12px',
    }}>
      {photos.map((photo) => (
        <PhotoCard key={photo.id} photo={photo} onClick={onPhotoClick} />
      ))}
    </div>
  )
}
