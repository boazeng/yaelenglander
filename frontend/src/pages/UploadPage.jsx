import UploadForm from '../components/photos/UploadForm'
import { useAuth } from '../context/AuthContext'

export default function UploadPage() {
  const { user } = useAuth()

  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      <div className="contentLeft">
        <div className="content-block">
          <h3>העלאת תמונה</h3>
          <p style={{ color: '#555', marginBottom: '20px' }}>
            שלום {user?.name}! העלו תמונות משפחתיות — המערכת תזהה ותתייג אותן אוטומטית.
          </p>
          <UploadForm />
        </div>
      </div>

      <div className="sidebarLeft">
        <div className="sidebar-block">
          <h4>טיפים להעלאה</h4>
          <div className="sidebar-content">
            <ul className="list1">
              <li>העלו תמונות באיכות טובה</li>
              <li>הוסיפו תיאור קצר — זה עוזר לזכור</li>
              <li>המערכת מזהה אוטומטית: אנשים, מקומות, אירועים ועוד</li>
              <li>אפשר לערוך תגיות אחרי ההעלאה</li>
              <li>תמונות ישנות בשחור-לבן? מצוין!</li>
            </ul>
          </div>
        </div>

        <div className="sidebar-block">
          <h4>ציטוט</h4>
          <div className="sidebar-content">
            <blockquote>
              "כל תמונה מספרת סיפור — שמרו את הסיפורים שלנו"
            </blockquote>
            <p style={{ color: '#b5913f', fontSize: '13px', marginTop: '8px' }}>— יעל אנגלנדר</p>
          </div>
        </div>
      </div>
    </div>
    </div></div>
  )
}
