import { Link } from 'react-router-dom'

const sections = [
  { path: '/pekiin', title: 'פקיעין', desc: 'הכפר שבו יהודים מעולם לא עזבו את ארץ ישראל. כאן נולדה יעל, וכאן מתחיל הסיפור.' },
  { path: '/stories', title: 'סיפורים', desc: 'סיפורי חיים, זיכרונות וצחוקים מהמשפחה. מילדות בפקיעין ועד חיי יום יום.' },
  { path: '/recipes', title: 'מתכונים', desc: 'הטעמים של יעל — מתכונים שעוברים מדור לדור, עם הסיפור שמאחורי כל מנה.' },
  { path: '/photos', title: 'תמונות', desc: 'רגעים שנשמרו לנצח — תמונות מכל תקופות החיים.' },
]

export default function HomePage() {
  return (
    <>
      {/* Top Section - Background + Two Content Blocks */}
      <div id="topsection">
        <div className="container" style={{ display: 'flex', justifyContent: 'center', gap: '16%' }}>
          <Link to="/stories" className="top-content-block snip">
            <img src="/images/topcontent1.jpg" alt="" />
            <div className="top-content-overlay">
              <h3 className="title1">הסיפורים</h3>
              <h3 className="title2">זיכרונות ורגעים</h3>
              <h3 className="title3">מחיי יעל</h3>
            </div>
          </Link>
          <Link to="/recipes" className="top-content-block snip">
            <img src="/images/topcontent2.jpg" alt="" />
            <div className="top-content-overlay">
              <h3 className="title1">המתכונים</h3>
              <h3 className="title2">טעמים מדור לדור</h3>
              <h3 className="title3">מהמטבח של יעל</h3>
            </div>
          </Link>
        </div>
      </div>

      <div className="row3">
        <div className="container">
        <div className="content-area">
        {/* Main Content */}
        <div className="contentLeft">

          <h2>ברוכים הבאים</h2>
          <div className="content-block">
            <p>
              יעל אנגלנדר נולדה בפקיעין — הכפר העתיק שבו יהודים חיו ברציפות
              מתקופת בית שני ועד ימינו. היא חיה עם אהבה, גידלה משפחה,
              ושמרה על מסורות שעברו מדור לדור.
            </p>
            <p>
              האתר הזה לא נבנה כאתר זיכרון — הוא נבנה כדי להחיות אותה.
              כאן תמצאו את הסיפורים שלה, המתכונים שלה, התמונות,
              וגם תוכלו לדבר איתה.
            </p>
          </div>

          {/* 2-column sections */}
          <div style={{ display: 'flex', gap: '2%', flexWrap: 'wrap' }}>
            {sections.map((section) => (
              <div key={section.path} style={{ width: '48%', marginBottom: '20px' }}>
                <div className="content-block" style={{ height: '100%' }}>
                  <h5 style={{ marginBottom: '8px' }}>
                    <Link to={section.path} style={{ color: '#1f3442' }}>{section.title}</Link>
                  </h5>
                  <p style={{ fontSize: '13px', color: '#555' }}>{section.desc}</p>
                  <Link to={section.path} className="btn-main" style={{ marginTop: '10px' }}>
                    קראו עוד
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="sidebarLeft">

          <div className="sidebar-block">
            <h4>ציטוט</h4>
            <div className="sidebar-content">
              <blockquote>
                "המשפחה היא השורשים, והסיפורים הם הענפים"
              </blockquote>
              <p style={{ color: '#b5913f', fontSize: '13px', marginTop: '8px' }}>— יעל אנגלנדר</p>
            </div>
          </div>

          <div className="sidebar-block">
            <h4>ניווט מהיר</h4>
            <div className="sidebar-content">
              <ul className="list1">
                {sections.map((section) => (
                  <li key={section.path}>
                    <Link to={section.path}>{section.title}</Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="sidebar-block">
            <h4>על פקיעין</h4>
            <div className="sidebar-content">
              <p style={{ fontSize: '13px', color: '#555' }}>
                פקיעין היא כפר עתיק בגליל העליון.
                זהו אחד המקומות היחידים שבו יהודים חיו ברציפות
                לאורך כל הדורות.
              </p>
              <Link to="/pekiin" className="btn-main" style={{ marginTop: '10px' }}>
                קראו עוד
              </Link>
            </div>
          </div>
        </div>
      </div>
      </div>
      </div>
    </>
  )
}
