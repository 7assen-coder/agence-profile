import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="flex w-full flex-1 items-center justify-center px-6 py-28 text-xl text-slate-500 sm:px-10">
        Chargement…
      </div>
    )
  }

  if (!token) {
    return <Navigate to="/connexion" state={{ from: location }} replace />
  }

  return <>{children}</>
}
