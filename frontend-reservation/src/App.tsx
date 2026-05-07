import { Routes, Route } from 'react-router'
import Home from './pages/Home'
import AdminLayout from './layouts/AdminLayout'
import AdminDashboard from './pages/AdminDashboard'
import AdminReservations from './pages/AdminReservations'
import AdminTrajets from './pages/AdminTrajets'
import AdminStatistiques from './pages/AdminStatistiques'
import AdminClients from './pages/AdminClients'
import AdminParametres from './pages/AdminParametres'
import AdminDatabase from './pages/AdminDatabase'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/admin" element={<AdminLayout><AdminDashboard /></AdminLayout>} />
      <Route path="/admin/reservations" element={<AdminLayout><AdminReservations /></AdminLayout>} />
      <Route path="/admin/trajets" element={<AdminLayout><AdminTrajets /></AdminLayout>} />
      <Route path="/admin/statistiques" element={<AdminLayout><AdminStatistiques /></AdminLayout>} />
      <Route path="/admin/clients" element={<AdminLayout><AdminClients /></AdminLayout>} />
      <Route path="/admin/parametres" element={<AdminLayout><AdminParametres /></AdminLayout>} />
      <Route path="/admin/database" element={<AdminLayout><AdminDatabase /></AdminLayout>} />
    </Routes>
  )
}
