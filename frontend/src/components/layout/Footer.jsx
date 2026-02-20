export default function Footer() {
  return (
    <footer>
      <div className="row4">
        <div className="container" style={{ padding: '20px 2%', textAlign: 'center' }}>
          <h4 style={{
            color: '#fff',
            fontFamily: "'Jura', sans-serif",
            fontSize: '20px',
            borderBottom: '1px solid #444',
            paddingBottom: '10px',
            marginBottom: '10px',
          }}>
            יעל אנגלנדר — מפקיעין עם אהבה
          </h4>
          <p style={{ color: '#999', fontSize: '12px', margin: '5px 0' }}>
            נבנה באהבה על ידי המשפחה &copy; {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </footer>
  )
}
