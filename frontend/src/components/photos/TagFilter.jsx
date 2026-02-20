export default function TagFilter({ tags, activeTags, onToggle }) {
  if (!tags.length) return null

  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '20px' }}>
      <button
        onClick={() => onToggle(null)}
        style={{
          padding: '5px 14px', borderRadius: '16px', border: '1px solid #b5913f',
          background: activeTags.length === 0 ? '#b5913f' : '#fff',
          color: activeTags.length === 0 ? '#fff' : '#b5913f',
          cursor: 'pointer', fontSize: '13px', fontWeight: 600,
        }}
      >
        הכל
      </button>
      {tags.map((tag) => {
        const active = activeTags.includes(tag.name)
        return (
          <button
            key={tag.id}
            onClick={() => onToggle(tag.name)}
            style={{
              padding: '5px 14px', borderRadius: '16px', border: '1px solid #b5913f',
              background: active ? '#b5913f' : '#fff',
              color: active ? '#fff' : '#b5913f',
              cursor: 'pointer', fontSize: '13px', transition: 'all 0.2s',
            }}
          >
            {tag.name}
          </button>
        )
      })}
    </div>
  )
}
