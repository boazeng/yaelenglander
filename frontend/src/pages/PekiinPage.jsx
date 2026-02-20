const timelineEvents = [
  { year: 'תקופת בית שני', title: 'ראשית הקהילה', text: 'משפחות יהודיות מתיישבות בפקיעין. לפי המסורת, יהודי פקיעין מעולם לא עזבו את ארץ ישראל.' },
  { year: 'המאה ה-2', title: 'רבי שמעון בר יוחאי', text: 'רשב"י ובנו רבי אלעזר מתחבאים במערה בפקיעין במשך 13 שנה מפני הרומאים.' },
  { year: 'המאה ה-16', title: 'בית הכנסת העתיק', text: 'בית הכנסת של פקיעין, אחד העתיקים בעולם, ממשיך לשמש את הקהילה.' },
  { year: 'המאה ה-20', title: 'משפחת אנגלנדר', text: 'יעל נולדת בפקיעין, גדלה בין השורשים העמוקים של הקהילה היהודית העתיקה.' },
]

export default function PekiinPage() {
  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      {/* Main Content */}
      <div className="contentLeft">

        <div className="content-block">
          <h3>פקיעין — הכפר שמעולם לא נעזב</h3>

          <div className="img-frame" style={{ marginBottom: '20px', textAlign: 'center' }}>
            <div style={{
              padding: '60px 20px',
              background: 'linear-gradient(to bottom, #33556b, #172331)',
              color: '#b7a782',
              fontFamily: "'Frank Ruhl Libre', serif",
            }}>
              תמונה של פקיעין תתווסף כאן
            </div>
          </div>

          <p>
            פקיעין היא כפר עתיק בגליל העליון, ידוע כמקום שבו שרדה קהילה יהודית
            רצופה מתקופת בית שני ועד ימינו. זהו אחד המקומות היחידים בארץ ישראל
            שבו יהודים חיו ברציפות לאורך כל הדורות — גם בתקופות של גלות וחורבן.
          </p>
          <p>
            הכפר ידוע במערת רשב"י, בית הכנסת העתיק שלו, ובמסורות שעוברות
            ממשפחה למשפחה. יעל אנגלנדר נולדה וגדלה כאן, ונשאה איתה את
            הסיפורים, הטעמים והמסורות של פקיעין לכל מקום שהלכה.
          </p>
        </div>

        <div className="content-block">
          <h3>ציר הזמן של פקיעין</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <tbody>
              {timelineEvents.map((event, index) => (
                <tr key={index} style={{ borderBottom: '1px dashed #aaa' }}>
                  <td style={{
                    padding: '15px 15px 15px 0',
                    width: '130px',
                    verticalAlign: 'top',
                    color: '#b5913f',
                    fontWeight: 600,
                    fontSize: '13px',
                    fontFamily: "'Frank Ruhl Libre', serif",
                  }}>
                    {event.year}
                  </td>
                  <td style={{ padding: '15px 0' }}>
                    <strong style={{ color: '#1f3442', fontSize: '15px' }}>{event.title}</strong>
                    <br />
                    <span style={{ color: '#555', fontSize: '13px' }}>{event.text}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Sidebar */}
      <div className="sidebarLeft">

        <div className="sidebar-block">
          <h4>ציטוט</h4>
          <div className="sidebar-content">
            <blockquote>
              "בפקיעין השורשים עמוקים כמו ההרים"
            </blockquote>
            <p style={{ color: '#b5913f', fontSize: '13px', marginTop: '8px' }}>— יעל אנגלנדר</p>
          </div>
        </div>

        <div className="sidebar-block">
          <h4>מקומות חשובים</h4>
          <div className="sidebar-content">
            <ul className="list1">
              {['מערת רשב"י', 'בית הכנסת העתיק', 'עין הכפר', 'עץ התאנה העתיק', 'בית משפחת זינאתי'].map((place) => (
                <li key={place}><a href="#">{place}</a></li>
              ))}
            </ul>
          </div>
        </div>

        <div className="sidebar-block">
          <h4>הידעתם?</h4>
          <div className="sidebar-content">
            <p style={{ fontSize: '13px', color: '#555' }}>
              פקיעין הוא אחד המקומות היחידים בעולם
              שבו נשמרה נוכחות יהודית רצופה במשך
              יותר מ-2,000 שנה.
            </p>
          </div>
        </div>
      </div>
    </div>
    </div></div>
  )
}
