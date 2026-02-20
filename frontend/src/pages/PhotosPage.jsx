import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getPhotos, getTags } from '../api/client'
import { useAuth } from '../context/AuthContext'
import PhotoGrid from '../components/photos/PhotoGrid'
import TagFilter from '../components/photos/TagFilter'
import Lightbox from '../components/photos/Lightbox'

export default function PhotosPage() {
  const [photos, setPhotos] = useState([])
  const [allTags, setAllTags] = useState([])
  const [activeTags, setActiveTags] = useState([])
  const [selectedPhoto, setSelectedPhoto] = useState(null)
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()

  useEffect(() => {
    loadData()
  }, [activeTags])

  async function loadData() {
    setLoading(true)
    try {
      const [photosData, tagsData] = await Promise.all([
        getPhotos({ tags: activeTags.join(',') || undefined }),
        allTags.length ? Promise.resolve(allTags) : getTags(),
      ])
      setPhotos(photosData)
      if (!allTags.length) setAllTags(tagsData)
    } catch (err) {
      console.error('Failed to load photos:', err)
    } finally {
      setLoading(false)
    }
  }

  function handleTagToggle(tagName) {
    if (!tagName) {
      setActiveTags([])
      return
    }
    setActiveTags(prev =>
      prev.includes(tagName)
        ? prev.filter(t => t !== tagName)
        : [...prev, tagName]
    )
  }

  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      <div className="contentLeft">
        <div className="content-block">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h3 style={{ margin: 0 }}>גלריית תמונות</h3>
            {user && (
              <Link to="/upload" className="btn-main" style={{ textDecoration: 'none', fontSize: '14px' }}>
                + העלאת תמונה
              </Link>
            )}
          </div>
          <p style={{ color: '#555', marginBottom: '20px' }}>
            רגעים שנשמרו לנצח — כי כל תמונה היא חלון לזמן אחר.
          </p>

          <TagFilter tags={allTags} activeTags={activeTags} onToggle={handleTagToggle} />

          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>טוען תמונות...</div>
          ) : (
            <PhotoGrid photos={photos} onPhotoClick={setSelectedPhoto} />
          )}
        </div>
      </div>

      <div className="sidebarLeft">
        <div className="sidebar-block">
          <h4>תגיות פופולריות</h4>
          <div className="sidebar-content">
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {allTags.slice(0, 15).map((tag) => (
                <button
                  key={tag.id}
                  onClick={() => handleTagToggle(tag.name)}
                  style={{
                    padding: '3px 10px', borderRadius: '12px', fontSize: '12px',
                    border: '1px solid #ddd', cursor: 'pointer',
                    background: activeTags.includes(tag.name) ? '#b5913f' : '#f9f6f0',
                    color: activeTags.includes(tag.name) ? '#fff' : '#666',
                  }}
                >
                  {tag.name}
                </button>
              ))}
            </div>
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

        {!user && (
          <div className="sidebar-block">
            <h4>בן משפחה?</h4>
            <div className="sidebar-content">
              <p>
                <Link to="/login" style={{ color: '#b5913f' }}>התחבר</Link> כדי להעלות תמונות משפחתיות.
              </p>
            </div>
          </div>
        )}
      </div>

      <Lightbox photo={selectedPhoto} onClose={() => setSelectedPhoto(null)} />
    </div>
    </div></div>
  )
}
