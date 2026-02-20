import { useState } from 'react'

const categories = ['הכל', 'עיקריות', 'קינוחים', 'שבת וחגים', 'סלטים ומזות']

const recipes = [
  { id: 1, title: 'קובה בורגול של יעל', category: 'עיקריות', time: '90 דקות', story: 'את הקובה הזו יעל למדה מאימה, שלמדה מאימה שלה. שלושה דורות של אותו טעם.', ingredients: ['בורגול דק', 'בשר טחון', 'בצל', 'שמן זית', 'תבלינים'] },
  { id: 2, title: "מג'דרה של הסבתות", category: 'עיקריות', time: '60 דקות', story: "כל שישי, כשהריח של המג'דרה התפשט בבית, ידעת שהשבת בדרך.", ingredients: ['עדשים', 'אורז', 'בצל מטוגן', 'שמן זית', 'כמון'] },
  { id: 3, title: 'עוגת תאנים מפקיעין', category: 'קינוחים', time: '45 דקות', story: 'התאנים היו מעץ התאנה בחצר. יעל תמיד אמרה שהטעם הכי טוב הוא מהעץ שלך.', ingredients: ['תאנים טריות', 'קמח', 'סוכר', 'ביצים', 'שמן'] },
  { id: 4, title: 'סלט ירוק עם זעתר ולימון', category: 'סלטים ומזות', time: '15 דקות', story: 'הזעתר הגיע מהגבעה שמעל הבית. יעל הייתה קוטפת אותו טרי כל בוקר.', ingredients: ['עלים ירוקים', 'זעתר טרי', 'לימון', 'שמן זית', 'מלח'] },
  { id: 5, title: 'חלה של שבת', category: 'שבת וחגים', time: '3 שעות', story: 'הריח של החלה מהתנור היה הסימן הרשמי שהשבת נכנסת.', ingredients: ['קמח', 'שמרים', 'סוכר', 'ביצים', 'שמן', 'מלח'] },
]

export default function RecipesPage() {
  const [activeCategory, setActiveCategory] = useState('הכל')

  const filtered = activeCategory === 'הכל'
    ? recipes
    : recipes.filter((r) => r.category === activeCategory)

  return (
    <div className="row3"><div className="container">
    <div className="content-area">
      {/* Main Content */}
      <div className="contentLeft">
        <div className="content-block">
          <h3>המתכונים של יעל</h3>
          <p style={{ color: '#555', marginBottom: '20px' }}>
            כי אוכל זה אהבה, וכל מתכון הוא סיפור. הטעמים של יעל — מפקיעין לשולחן.
          </p>

          {filtered.map((recipe, index) => (
            <div key={recipe.id}>
              {index > 0 && <hr className="divider" />}
              <div style={{ padding: '10px 0' }}>
                <span className="tag">{recipe.category}</span>
                <span style={{ fontSize: '12px', color: '#999', marginRight: '10px' }}>⏱ {recipe.time}</span>
                <h5 style={{ margin: '8px 0 6px', color: '#1f3442' }}>
                  <a href="#">{recipe.title}</a>
                </h5>
                <p style={{ color: '#555', fontSize: '13px', fontStyle: 'italic' }}>
                  "{recipe.story}"
                </p>
                <div style={{ marginTop: '8px' }}>
                  {recipe.ingredients.map((ing, i) => (
                    <span key={i} style={{
                      display: 'inline-block',
                      background: '#f1f1f1',
                      border: '1px solid #ddd',
                      padding: '2px 8px',
                      fontSize: '11px',
                      color: '#555',
                      marginLeft: '5px',
                      marginBottom: '4px',
                    }}>
                      {ing}
                    </span>
                  ))}
                </div>
                <a href="#" style={{ fontSize: '12px', fontWeight: 600, display: 'inline-block', marginTop: '8px' }}>
                  למתכון המלא ◂
                </a>
              </div>
            </div>
          ))}
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
              "הטעם הכי טוב הוא כשמבשלים עם אהבה"
            </blockquote>
            <p style={{ color: '#b5913f', fontSize: '13px', marginTop: '8px' }}>— יעל אנגלנדר</p>
          </div>
        </div>

        <div className="sidebar-block">
          <h4>טיפ של יעל</h4>
          <div className="sidebar-content">
            <p style={{ fontSize: '13px', color: '#555' }}>
              "תמיד תטעמו תוך כדי בישול.
              המתכון הוא רק הבסיס —
              היד שלכם היא הסוד."
            </p>
          </div>
        </div>
      </div>
    </div>
    </div></div>
  )
}
