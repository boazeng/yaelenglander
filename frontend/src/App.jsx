import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import PekiinPage from './pages/PekiinPage'
import StoriesPage from './pages/StoriesPage'
import RecipesPage from './pages/RecipesPage'
import PhotosPage from './pages/PhotosPage'

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/pekiin" element={<PekiinPage />} />
          <Route path="/stories" element={<StoriesPage />} />
          <Route path="/recipes" element={<RecipesPage />} />
          <Route path="/photos" element={<PhotosPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
