import { useState, useEffect } from 'react';
import {
  Bus,
  Calendar,
  User,
  CreditCard,
  MapPin,
  CheckCircle,
  Clock,
  XCircle,
  Armchair,
  Search,
  Filter,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { getAllReservations } from '@/services/api';
import type { ReservationComplet } from '@/types';

export default function AdminReservations() {
  const [reservations, setReservations] = useState<ReservationComplet[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'tous' | 'confirmee' | 'en_attente' | 'annulee'>('tous');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    getAllReservations().then((data: ReservationComplet[]) => {
      setReservations(data);
      setLoading(false);
    });
  }, []);

  const filtered = reservations
    .filter(r => filter === 'tous' || r.statut === filter)
    .filter(r => {
      if (!searchTerm) return true;
      const term = searchTerm.toLowerCase();
      return (
        r.client?.nom.toLowerCase().includes(term) ||
        r.client?.prenom.toLowerCase().includes(term) ||
        r.client?.cin.toLowerCase().includes(term) ||
        r.trajet?.ville_depart?.nom.toLowerCase().includes(term) ||
        r.trajet?.ville_arrivee?.nom.toLowerCase().includes(term) ||
        r.trajet?.agence?.nom.toLowerCase().includes(term)
      );
    });

  const stats = {
    total: reservations.length,
    confirmee: reservations.filter(r => r.statut === 'confirmee').length,
    en_attente: reservations.filter(r => r.statut === 'en_attente').length,
    annulee: reservations.filter(r => r.statut === 'annulee').length,
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Réservations</h1>
        <p className="text-sm text-gray-500 mt-1">Gestion et supervision des réservations</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card className="border border-gray-200 bg-white">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
              <Bus className="w-6 h-6 text-[#0891b2]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-sm text-gray-500">Total</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 bg-white">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.confirmee}</div>
              <div className="text-sm text-gray-500">Confirmées</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 bg-white">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-amber-50 rounded-xl flex items-center justify-center">
              <Clock className="w-6 h-6 text-amber-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.en_attente}</div>
              <div className="text-sm text-gray-500">En attente</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 bg-white">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-red-50 rounded-xl flex items-center justify-center">
              <XCircle className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{stats.annulee}</div>
              <div className="text-sm text-gray-500">Annulées</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-2 bg-white rounded-xl p-1 border border-gray-200 shadow-sm">
          <button onClick={() => setFilter('tous')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'tous' ? 'bg-[#0891b2] text-white' : 'text-gray-600 hover:bg-gray-50'}`}>Tous</button>
          <button onClick={() => setFilter('confirmee')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'confirmee' ? 'bg-green-600 text-white' : 'text-gray-600 hover:bg-gray-50'}`}>Confirmées</button>
          <button onClick={() => setFilter('en_attente')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'en_attente' ? 'bg-amber-500 text-white' : 'text-gray-600 hover:bg-gray-50'}`}>En attente</button>
          <button onClick={() => setFilter('annulee')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filter === 'annulee' ? 'bg-red-500 text-white' : 'text-gray-600 hover:bg-gray-50'}`}>Annulées</button>
        </div>

        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <Input placeholder="Rechercher par nom, CIN, ville..." value={searchTerm} onChange={e => setSearchTerm(e.target.value)} className="pl-10" />
        </div>
      </div>

      {/* Reservations Table */}
      <Card className="border border-gray-200 shadow-sm">
        <CardContent className="p-0">
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <div className="w-8 h-8 border-2 border-[#0891b2]/30 border-t-[#0891b2] rounded-full animate-spin"></div>
            </div>
          ) : filtered.length === 0 ? (
            <div className="text-center py-16">
              <Filter className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">Aucune réservation trouvée</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50/80">
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">ID</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Client</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Trajet</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Date & Heure</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Place</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Agence</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Paiement</th>
                    <th className="text-left px-4 py-3 font-semibold text-gray-700">Statut</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((r, idx) => (
                    <tr key={r.id_reservation} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}>
                      <td className="px-4 py-4 font-mono text-gray-500">#{r.id_reservation}</td>
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 bg-[#0891b2]/10 rounded-full flex items-center justify-center">
                            <User className="w-4 h-4 text-[#0891b2]" />
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">{r.client?.prenom} {r.client?.nom}</div>
                            <div className="text-xs text-gray-500">CIN: {r.client?.cin}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-1 text-gray-700">
                          <MapPin className="w-3 h-3 text-[#0891b2]" />
                          {r.trajet?.ville_depart?.nom}
                          <span className="text-gray-400 mx-1">→</span>
                          {r.trajet?.ville_arrivee?.nom}
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-1 text-gray-700">
                          <Calendar className="w-3 h-3 text-gray-400" />
                          {r.trajet?.date_trajet}
                        </div>
                        <div className="text-xs text-gray-500 mt-0.5">{r.trajet?.heure_depart}</div>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-1">
                          <Armchair className="w-4 h-4 text-[#0891b2]" />
                          <span className="font-medium">N° {r.place?.numero_place}</span>
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex items-center gap-1 text-gray-700">
                          <Bus className="w-4 h-4 text-gray-400" />
                          {r.trajet?.agence?.nom}
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        {r.paiement ? (
                          <div>
                            <div className="flex items-center gap-1 text-gray-700">
                              <CreditCard className="w-3 h-3 text-green-600" />
                              {r.paiement.montant.toFixed(2)} MRU
                            </div>
                            <div className="text-xs text-gray-500 capitalize">{formatPaymentMode(r.paiement.mode_paiement)}</div>
                          </div>
                        ) : (
                          <span className="text-gray-400 text-xs">Non payé</span>
                        )}
                      </td>
                      <td className="px-4 py-4">
                        <Badge className={getStatusStyle(r.statut)}>
                          {formatStatus(r.statut)}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function getStatusStyle(statut: string): string {
  switch (statut) {
    case 'confirmee': return 'bg-green-100 text-green-700 hover:bg-green-100';
    case 'en_attente': return 'bg-amber-100 text-amber-700 hover:bg-amber-100';
    case 'annulee': return 'bg-red-100 text-red-700 hover:bg-red-100';
    default: return 'bg-gray-100 text-gray-700';
  }
}

function formatStatus(statut: string): string {
  const statuses: Record<string, string> = {
    'confirmee': 'Confirmée',
    'en_attente': 'En attente',
    'annulee': 'Annulée',
  };
  return statuses[statut] || statut;
}

function formatPaymentMode(mode?: string): string {
  const modes: Record<string, string> = {
    'carte': 'Carte',
    'mobile_money': 'Mobile',
    'virement': 'Virement',
    'especes': 'Espèces',
  };
  return modes[mode || ''] || mode || '';
}
