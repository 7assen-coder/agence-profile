import { Navigate, Route, Routes } from 'react-router-dom'
import { Shell } from './components/Shell'
import { ProtectedRoute } from './components/ProtectedRoute'
import { HomePage } from './pages/HomePage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { DashboardPage } from './pages/DashboardPage'
import { AgenciesPage } from './pages/AgenciesPage'
import { AgencyDetailPage } from './pages/AgencyDetailPage'

export default function App() {
  return (
    <div className="flex min-h-dvh w-full flex-col">
      <Routes>
        <Route path="/" element={<Shell />}>
          <Route index element={<HomePage />} />
          <Route path="connexion" element={<LoginPage />} />
          <Route path="inscription" element={<RegisterPage />} />
          <Route path="agences" element={<AgenciesPage />} />
          <Route path="agences/:id" element={<AgencyDetailPage />} />
          <Route
            path="compte"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </div>
  )
}
