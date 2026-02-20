import { useState, useRef } from 'react'
import { uploadPhoto, updatePhotoTags } from '../../api/client'

export default function UploadForm() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [caption, setCaption] = useState('')
  const [status, setStatus] = useState('idle') // idle | uploading | tagging | done | error
  const [result, setResult] = useState(null)
  const [editedTags, setEditedTags] = useState([])
  const [newTag, setNewTag] = useState('')
  const [error, setError] = useState('')
  const fileRef = useRef()

  function handleFileSelect(e) {
    const f = e.target.files?.[0]
    if (!f) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setStatus('idle')
    setResult(null)
    setError('')
  }

  function handleDrop(e) {
    e.preventDefault()
    const f = e.dataTransfer.files?.[0]
    if (!f || !f.type.startsWith('image/')) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setStatus('idle')
    setResult(null)
    setError('')
  }

  async function handleUpload() {
    if (!file) return
    setStatus('uploading')
    setError('')
    try {
      setStatus('tagging')
      const data = await uploadPhoto(file, caption)
      setResult(data)
      setEditedTags([...data.tags])
      setStatus('done')
    } catch (err) {
      setError(err.message)
      setStatus('error')
    }
  }

  function removeTag(idx) {
    setEditedTags(prev => prev.filter((_, i) => i !== idx))
  }

  function addTag() {
    const tag = newTag.trim()
    if (!tag || editedTags.includes(tag)) return
    if (editedTags.length >= 20) return
    setEditedTags(prev => [...prev, tag])
    setNewTag('')
  }

  async function saveTags() {
    if (!result) return
    try {
      await updatePhotoTags(result.id, editedTags)
      setResult(prev => ({ ...prev, tags: editedTags }))
    } catch (err) {
      setError(err.message)
    }
  }

  function reset() {
    setFile(null)
    setPreview(null)
    setCaption('')
    setStatus('idle')
    setResult(null)
    setEditedTags([])
    setNewTag('')
    setError('')
  }

  const statusText = {
    uploading: 'מעלה תמונה...',
    tagging: 'מנתח תמונה עם AI — מזהה תגיות...',
  }

  return (
    <div>
      {/* Drop zone / File select */}
      {!preview && (
        <div
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          onClick={() => fileRef.current?.click()}
          style={{
            border: '2px dashed #b5913f',
            borderRadius: '8px',
            padding: '60px 20px',
            textAlign: 'center',
            cursor: 'pointer',
            background: '#faf8f3',
            transition: 'background 0.2s',
          }}
          onMouseEnter={(e) => e.currentTarget.style.background = '#f5f0e6'}
          onMouseLeave={(e) => e.currentTarget.style.background = '#faf8f3'}
        >
          <div style={{ fontSize: '3em', marginBottom: '12px', color: '#b5913f' }}>+</div>
          <p style={{ fontSize: '16px', color: '#555' }}>
            גררו תמונה לכאן או לחצו לבחירה
          </p>
          <p style={{ fontSize: '13px', color: '#999', marginTop: '8px' }}>
            JPG, PNG, WebP — עד 20MB
          </p>
          <input
            ref={fileRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </div>
      )}

      {/* Preview + Caption */}
      {preview && status !== 'done' && (
        <div>
          <div style={{ marginBottom: '16px', textAlign: 'center' }}>
            <img
              src={preview}
              alt="תצוגה מקדימה"
              style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '8px', border: '2px solid #ddd' }}
            />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', marginBottom: '6px', fontWeight: 600, color: '#1f3442' }}>
              תיאור (אופציונלי)
            </label>
            <input
              type="text"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              placeholder="למשל: סבתא יעל עם הנכדים בחצר"
              style={{
                width: '100%', padding: '10px 12px', border: '1px solid #ccc',
                borderRadius: '4px', fontSize: '15px',
              }}
            />
          </div>

          {/* Status / Loading */}
          {(status === 'uploading' || status === 'tagging') && (
            <div style={{
              background: '#f0f7ff', padding: '16px', borderRadius: '8px',
              textAlign: 'center', color: '#1f3442', marginBottom: '16px',
            }}>
              <div style={{ fontSize: '24px', marginBottom: '8px', animation: 'spin 1s linear infinite' }}>
                {status === 'tagging' ? '🔍' : '⬆️'}
              </div>
              <p>{statusText[status]}</p>
            </div>
          )}

          {error && (
            <div style={{ color: '#c0392b', marginBottom: '16px' }}>{error}</div>
          )}

          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              className="btn-main"
              onClick={handleUpload}
              disabled={status === 'uploading' || status === 'tagging'}
              style={{ padding: '12px 28px', fontSize: '15px' }}
            >
              {status === 'uploading' || status === 'tagging' ? 'מעבד...' : 'העלאה + תיוג אוטומטי'}
            </button>
            <button
              onClick={reset}
              style={{
                padding: '12px 20px', border: '1px solid #ccc', borderRadius: '4px',
                background: '#fff', cursor: 'pointer', fontSize: '14px',
              }}
            >
              ביטול
            </button>
          </div>
        </div>
      )}

      {/* Result — tags display + edit */}
      {status === 'done' && result && (
        <div>
          <div style={{
            background: '#eaf7ea', padding: '16px', borderRadius: '8px',
            marginBottom: '20px', textAlign: 'center', color: '#27ae60',
          }}>
            התמונה הועלתה בהצלחה!
          </div>

          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <div style={{ flex: '0 0 200px' }}>
              <img
                src={preview}
                alt="uploaded"
                style={{ width: '100%', borderRadius: '8px', border: '2px solid #ddd' }}
              />
              {result.caption && (
                <p style={{ fontSize: '13px', color: '#555', marginTop: '8px' }}>{result.caption}</p>
              )}
            </div>

            <div style={{ flex: 1, minWidth: '250px' }}>
              <h4 style={{ color: '#1f3442', marginBottom: '12px' }}>
                תגיות ({editedTags.length}/20)
              </h4>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
                {editedTags.map((tag, i) => (
                  <span key={i} className="tag" style={{
                    display: 'inline-flex', alignItems: 'center', gap: '6px',
                    padding: '4px 10px', fontSize: '13px',
                  }}>
                    {tag}
                    <button
                      onClick={() => removeTag(i)}
                      style={{
                        border: 'none', background: 'none', cursor: 'pointer',
                        color: '#999', fontSize: '14px', padding: 0, lineHeight: 1,
                      }}
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>

              {editedTags.length < 20 && (
                <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
                  <input
                    type="text"
                    value={newTag}
                    onChange={(e) => setNewTag(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                    placeholder="הוסף תגית..."
                    style={{
                      flex: 1, padding: '8px 12px', border: '1px solid #ccc',
                      borderRadius: '4px', fontSize: '14px',
                    }}
                  />
                  <button onClick={addTag} className="btn-main" style={{ padding: '8px 16px' }}>
                    +
                  </button>
                </div>
              )}

              {JSON.stringify(editedTags) !== JSON.stringify(result.tags) && (
                <button onClick={saveTags} className="btn-main" style={{ padding: '10px 20px', marginBottom: '12px' }}>
                  שמור שינויים בתגיות
                </button>
              )}

              <button
                onClick={reset}
                className="btn-main"
                style={{ padding: '10px 20px', background: '#b5913f' }}
              >
                העלאת תמונה נוספת
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
