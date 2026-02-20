import { useState } from 'react'
import { Link } from 'react-router-dom'

const categories = ['הכל', 'ילדות בפקיעין', 'צבא', 'משפחה', 'חיי יום יום']

const stories = [
  { id: 1, title: 'הלילה שבו ירד השלג בפקיעין', category: 'ילדות בפקיעין', period: 'שנות ה-50', excerpt: 'באותו חורף קר במיוחד, כל הכפר התעורר לנוף לבן. הילדים רצו החוצה בלי נעליים...' },
  { id: 2, title: 'המתכון הסודי של סבתא', category: 'משפחה', period: 'שנות ה-70', excerpt: 'סבתא מעולם לא כתבה את המתכון. היא מדדה הכל ביד, בעין, בלב. יום אחד ניסיתי להקליט אותה...' },
  { id: 3, title: 'היום הראשון בבסיס', category: 'צבא', period: 'שנות ה-60', excerpt: 'כשהגעתי לבסיס עם המזוודה הקטנה, כולם הסתכלו על הבחורה מפקיעין שלא הכירה אף אחד...' },
  { id: 4, title: 'שישי של כיפורים', category: 'חיי יום יום', period: 'שנות ה-80', excerpt: 'כל שישי היה אותו דבר — ריח של חלה מהתנור, שירים ברדיו, וכל הילדים יושבים סביב השולחן...' },
  { id: 5, title: 'עץ התאנה בחצר', category: 'ילדות בפקיעין', period: 'שנות ה-50', excerpt: 'עץ התאנה היה הכי גבוה בכפר. אנחנו היינו מטפסים עליו כל קיץ ואוכלים תאנים ישר מהענף...' },
]

export default function StoriesPage() {
  const [activeCategory, setActiveCategory] = useState('הכל')

  const filtered = activeCategory === 'הכל'
    ? stories
    : stories.filter((s) => s.category === activeCategory)

  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      {/* Main Content */}
      <div className="contentLeft">
        <div className="content-block">
          <h3>הסיפורים של יעל</h3>
          <p style={{ color: '#555', marginBottom: '20px' }}>
            כי כל חיים הם אוסף של רגעים שצריך לספר. הסיפורים האלה הם יעל — בקולה, בסגנונה, באהבה שלה.
          </p>

          {filtered.map((story, index) => (
            <div key={story.id}>
              {index > 0 && <hr className="divider" />}
              <div style={{ padding: '10px 0' }}>
                <span className="tag">{story.category}</span>
                <span style={{ fontSize: '12px', color: '#999', marginRight: '10px' }}>{story.period}</span>
                <h5 style={{ margin: '8px 0 6px' }}>
                  <a href="#">{story.title}</a>
                </h5>
                <p style={{ color: '#555', fontSize: '13px' }}>{story.excerpt}</p>
                <a href="#" style={{ fontSize: '12px', fontWeight: 600 }}>
                  קראו את הסיפור המלא ◂
                </a>
              </div>
            </div>
          ))}

          {filtered.length === 0 && (
            <p style={{ color: '#999', textAlign: 'center', padding: '30px 0' }}>
              עוד אין סיפורים בקטגוריה הזו. בקרוב יתווספו!
            </p>
          )}
        </div>
      </div>

      {/* Sidebar */}
      <div className="sidebarLeft">
        <div className="sidebar-block">
          <h4>קטגוריות</h4>
          <div className="sidebar-content">
            <ul className="list1">
              {categories.map((cat) => (
                <li key={cat}>
                  <a
                    href="#"
                    onClick={(e) => { e.preventDefault(); setActiveCategory(cat) }}
                    style={{ fontWeight: activeCategory === cat ? 700 : 400 }}
                  >
                    {cat}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="sidebar-block">
          <h4>ציטוט</h4>
          <div className="sidebar-content">
            <blockquote>
              "כל סיפור שלא מספרים — נעלם לנצח"
            </blockquote>
            <p style={{ color: '#b5913f', fontSize: '13px', marginTop: '8px' }}>— יעל אנגלנדר</p>
          </div>
        </div>
      </div>
    </div>
    </div></div>
  )
}
