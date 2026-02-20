import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Layout from './components/layout/Layout'
import ProtectedRoute from './components/auth/ProtectedRoute'
import HomePage from './pages/HomePage'
import PekiinPage from './pages/PekiinPage'
import StoriesPage from './pages/StoriesPage'
import RecipesPage from './pages/RecipesPage'
import PhotosPage from './pages/PhotosPage'
import LoginPage from './pages/LoginPage'
import UploadPage from './pages/UploadPage'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/pekiin" element={<PekiinPage />} />
            <Route path="/stories" element={<StoriesPage />} />
            <Route path="/recipes" element={<RecipesPage />} />
            <Route path="/photos" element={<PhotosPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/upload" element={
              <ProtectedRoute><UploadPage /></ProtectedRoute>
            } />
          </Routes>
        </Layout>
      </AuthProvider>
    </BrowserRouter>
  )
}
