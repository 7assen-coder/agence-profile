import { Link, useLocation } from 'react-router';
import {
  Bus,
  LayoutDashboard,
  CalendarDays,
  BarChart3,
  Users,
  Settings,
  LogOut,
  ChevronRight,
  Bell,
  Search,
  Armchair,
  Ticket,
  Shield,
  Database,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import type { ReactNode } from 'react';

interface AdminLayoutProps {
  children: ReactNode;
}

const menuItems = [
  { path: '/admin', label: 'Tableau de bord', icon: LayoutDashboard },
  { path: '/admin/reservations', label: 'Réservations', icon: Ticket },
  { path: '/admin/trajets', label: 'Trajets', icon: CalendarDays },
  { path: '/admin/statistiques', label: 'Statistiques', icon: BarChart3 },
  { path: '/admin/clients', label: 'Clients', icon: Users },
  { path: '/admin/database', label: 'Base de données', icon: Database },
  { path: '/admin/parametres', label: 'Paramètres', icon: Settings },
];

export default function AdminLayout({ children }: AdminLayoutProps) {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <div className="min-h-screen bg-[#f0f4f8] flex">
      {/* Sidebar - Fixed */}
      <aside className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-gray-200 z-50 flex flex-col shadow-sm">
        {/* Logo */}
        <div className="p-6 border-b border-gray-100">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-[#0c4a6e] to-[#0891b2] rounded-xl flex items-center justify-center shadow-md shadow-[#0891b2]/20">
              <Bus className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="font-bold text-gray-900 text-sm leading-tight">TransportReserve</div>
              <div className="text-[10px] text-gray-400 uppercase tracking-wider font-medium">Admin Panel</div>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          <div className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider px-3 mb-2 mt-2">Menu Principal</div>
          {menuItems.map((item) => {
            const isActive = currentPath === item.path || (item.path !== '/admin' && currentPath.startsWith(item.path));
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] text-white shadow-md shadow-[#0891b2]/20'
                    : 'text-gray-500 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-gray-400'}`} />
                {item.label}
                {isActive && <ChevronRight className="w-4 h-4 ml-auto text-white/70" />}
              </Link>
            );
          })}
        </nav>

        {/* Bottom Section */}
        <div className="p-4 border-t border-gray-100">
          <div className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] rounded-xl p-4 text-white mb-4 shadow-md shadow-[#0891b2]/10">
            <div className="flex items-center gap-2 mb-2">
              <Armchair className="w-4 h-4 text-cyan-300" />
              <span className="text-xs font-medium text-cyan-100">Places aujourd'hui</span>
            </div>
            <div className="text-2xl font-bold">47 / 96</div>
            <div className="text-xs text-cyan-200">49 places disponibles</div>
          </div>

          <div className="flex items-center gap-2 px-3 py-2 text-xs text-gray-400">
            <Shield className="w-3 h-3" />
            <span>Système sécurisé</span>
          </div>

          <Link to="/">
            <Button variant="ghost" className="w-full justify-start text-gray-500 hover:text-gray-900 hover:bg-gray-50 mt-2">
              <LogOut className="w-4 h-4 mr-2" /> Retour au site
            </Button>
          </Link>
        </div>
      </aside>

      {/* Main Content */}
      <div className="ml-64 flex-1 flex flex-col min-h-screen">
        {/* Top Header */}
        <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-gray-200 px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 flex-1">
              <div className="relative w-80">
                <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <Input placeholder="Rechercher dans l'admin..." className="pl-10 bg-gray-50 border-gray-200 rounded-xl" />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative w-10 h-10 rounded-xl bg-gray-50 hover:bg-gray-100 flex items-center justify-center transition-colors">
                <Bell className="w-5 h-5 text-gray-500" />
                <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <div className="flex items-center gap-3 pl-4 border-l border-gray-200">
                <div className="w-10 h-10 bg-gradient-to-br from-[#0c4a6e] to-[#0891b2] rounded-xl flex items-center justify-center">
                  <span className="text-white font-bold text-sm">AD</span>
                </div>
                <div className="hidden md:block">
                  <div className="text-sm font-medium text-gray-900">Administrateur</div>
                  <div className="text-xs text-gray-500">admin@transport.ma</div>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content - fills remaining height */}
        <main className="flex-1 p-8">
          {children}
        </main>

        {/* Footer */}
        <footer className="px-8 py-4 border-t border-gray-200 bg-white/50">
          <div className="flex items-center justify-between text-xs text-gray-400">
            <div className="flex items-center gap-2">
              <Bus className="w-4 h-4" />
              <span>Transport Reservation SaaS — Module Réservation</span>
            </div>
            <div className="flex items-center gap-4">
              <span>v1.0.0</span>
              <span>Flask + MySQL + React</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
