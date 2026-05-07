import { useState, useEffect } from 'react';
import {
  Users,
  Phone,
  Mail,
  FileText,
  Search,
  Ticket,
  CreditCard,
  TrendingUp,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { getAllClients } from '@/services/api';
import { reservations } from '@/data/mockData';

export default function AdminClients() {
  const [searchTerm, setSearchTerm] = useState('');
  const [clientsWithStats, setClientsWithStats] = useState<{
    id_client: number; nom: string; prenom: string; telephone: string;
    email: string; cin: string; reservation_count: number; total_spent: number;
  }[]>([]);

  useEffect(() => {
    getAllClients().then((data: typeof clientsWithStats) => setClientsWithStats(data));
  }, []);

  const filtered = clientsWithStats.filter(c => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    return (
      c.nom.toLowerCase().includes(term) ||
      c.prenom.toLowerCase().includes(term) ||
      c.cin.toLowerCase().includes(term) ||
      c.email.toLowerCase().includes(term) ||
      c.telephone.toLowerCase().includes(term)
    );
  });

  const totalSpent = clientsWithStats.reduce((sum, c) => sum + Number(c.total_spent), 0);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Gestion des clients</h1>
        <p className="text-sm text-gray-500 mt-1">Tous les clients et leurs activités</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-[#0891b2]/10 rounded-xl flex items-center justify-center">
              <Users className="w-6 h-6 text-[#0891b2]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{clientsWithStats.length}</div>
              <div className="text-sm text-gray-500">Clients enregistrés</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center">
              <CreditCard className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{totalSpent.toFixed(0)} MRU</div>
              <div className="text-sm text-gray-500">Revenus clients</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center">
              <Ticket className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{reservations.length}</div>
              <div className="text-sm text-gray-500">Réservations totales</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-amber-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {clientsWithStats.length > 0 ? Math.round(totalSpent / clientsWithStats.length) : 0} MRU
              </div>
              <div className="text-sm text-gray-500">Panier moyen</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Search */}
      <div className="relative w-full md:w-96 mb-6">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <Input
          placeholder="Rechercher par nom, CIN, email..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Clients Table */}
      <Card className="border border-gray-200 shadow-sm">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50/80">
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Client</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Contact</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">CIN</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Réservations</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Dépenses totales</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Status</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((c, idx) => (
                  <tr key={c.id_client} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-[#0c4a6e] to-[#0891b2] rounded-xl flex items-center justify-center">
                          <span className="text-white font-bold text-sm">{c.prenom[0]}{c.nom[0]}</span>
                        </div>
                        <div>
                          <div className="font-medium text-gray-900">{c.prenom} {c.nom}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-1 text-gray-600">
                          <Phone className="w-3 h-3 text-gray-400" />
                          {c.telephone}
                        </div>
                        <div className="flex items-center gap-1 text-gray-600">
                          <Mail className="w-3 h-3 text-gray-400" />
                          {c.email}
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-1 text-gray-700">
                        <FileText className="w-3 h-3 text-gray-400" />
                        {c.cin}
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-1">
                        <Ticket className="w-4 h-4 text-[#0891b2]" />
                        <span className="font-medium">{c.reservation_count}</span>
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="font-bold text-[#0c4a6e]">{Number(c.total_spent).toFixed(2)} MRU</div>
                    </td>
                    <td className="px-4 py-4">
                      <Badge className={c.reservation_count > 0 ? 'bg-green-100 text-green-700 hover:bg-green-100' : 'bg-gray-100 text-gray-600 hover:bg-gray-100'}>
                        {c.reservation_count > 0 ? 'Actif' : 'Inactif'}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
