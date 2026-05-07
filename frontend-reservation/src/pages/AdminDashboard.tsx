import { useState, useEffect } from 'react';
import { Link } from 'react-router';
import {
  ArrowUpRight,
  Bus,
  CalendarDays,
  Ticket,
  Users,
  CreditCard,
  TrendingUp,
  MapPin,
  Clock,
  ChevronRight,
  Armchair,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getAllReservations, getAllTrajets } from '@/services/api';
import { agences } from '@/data/mockData';
import type { ReservationComplet, TrajetComplet } from '@/types';

export default function AdminDashboard() {
  const [reservations, setReservations] = useState<ReservationComplet[]>([]);
  const [trajets, setTrajets] = useState<TrajetComplet[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getAllReservations(), getAllTrajets()]).then(([res, traj]) => {
      setReservations(res);
      setTrajets(traj);
      setLoading(false);
    });
  }, []);

  const stats = {
    totalReservations: reservations.length,
    confirmed: reservations.filter(r => r.statut === 'confirmee').length,
    pending: reservations.filter(r => r.statut === 'en_attente').length,
    cancelled: reservations.filter(r => r.statut === 'annulee').length,
    totalRevenue: reservations
      .filter(r => r.statut === 'confirmee')
      .reduce((sum, r) => sum + (r.paiement?.montant || 0), 0),
    activeTrajets: trajets.filter(t => (t.date_trajet ?? '') >= new Date().toISOString().split('T')[0]).length,
  };

  const recentReservations = reservations.slice(0, 5);

  return (
    <div>
      {/* Page Title */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Tableau de bord</h1>
        <p className="text-sm text-gray-500 mt-1">Vue d'ensemble du système de réservation</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <Card className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Réservations totales</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{stats.totalReservations}</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-green-600">
                  <ArrowUpRight className="w-3 h-3" />
                  <span>+12% ce mois</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-[#0891b2]/10 rounded-xl flex items-center justify-center">
                <Ticket className="w-5 h-5 text-[#0891b2]" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Revenus confirmés</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{stats.totalRevenue.toFixed(0)} MRU</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-green-600">
                  <ArrowUpRight className="w-3 h-3" />
                  <span>+8% ce mois</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-green-50 rounded-xl flex items-center justify-center">
                <CreditCard className="w-5 h-5 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Trajets actifs</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{stats.activeTrajets}</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
                  <CalendarDays className="w-3 h-3" />
                  <span>Aujourd'hui</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-amber-50 rounded-xl flex items-center justify-center">
                <Bus className="w-5 h-5 text-amber-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Clients enregistrés</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{reservations.length}</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-green-600">
                  <ArrowUpRight className="w-3 h-3" />
                  <span>+3 nouveaux</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-purple-50 rounded-xl flex items-center justify-center">
                <Users className="w-5 h-5 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Reservations */}
        <div className="lg:col-span-2">
          <Card className="border border-gray-200 shadow-sm">
            <CardHeader className="pb-4">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg font-semibold text-gray-900">Réservations récentes</CardTitle>
                <Link to="/admin/reservations">
                  <Button variant="ghost" size="sm" className="text-[#0891b2] hover:text-[#0c4a6e]">
                    Voir tout <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent className="pt-0">
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="w-6 h-6 border-2 border-[#0891b2]/30 border-t-[#0891b2] rounded-full animate-spin"></div>
                </div>
              ) : (
                <div className="space-y-3">
                  {recentReservations.map((r) => (
                    <div key={r.id_reservation} className="flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                          r.statut === 'confirmee' ? 'bg-green-50' : r.statut === 'en_attente' ? 'bg-amber-50' : 'bg-red-50'
                        }`}>
                          <Ticket className={`w-4 h-4 ${
                            r.statut === 'confirmee' ? 'text-green-600' : r.statut === 'en_attente' ? 'text-amber-600' : 'text-red-600'
                          }`} />
                        </div>
                        <div>
                          <div className="font-medium text-gray-900 text-sm">{r.client?.prenom} {r.client?.nom}</div>
                          <div className="text-xs text-gray-500 flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {r.trajet?.ville_depart?.nom} → {r.trajet?.ville_arrivee?.nom}
                            <span className="mx-1">|</span>
                            <Armchair className="w-3 h-3" />
                            Place {r.place?.numero_place}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold text-gray-900 text-sm">
                          {r.paiement ? `${r.paiement.montant.toFixed(0)} MRU` : '-'}
                        </div>
                        <div className={`text-xs font-medium ${
                          r.statut === 'confirmee' ? 'text-green-600' : r.statut === 'en_attente' ? 'text-amber-600' : 'text-red-600'
                        }`}>
                          {r.statut === 'confirmee' ? 'Confirmée' : r.statut === 'en_attente' ? 'En attente' : 'Annulée'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Occupancy Rate */}
          <Card className="border border-gray-200 shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg font-semibold text-gray-900">Taux d'occupation</CardTitle>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="space-y-4">
                {agences.map(agence => {
                  const agencyTrajets = trajets.filter(t => t.agence?.nom === agence.nom);
                  const agencyReservations = reservations.filter(r => r.trajet?.id_agence === agence.id_agence && r.statut === 'confirmee');
                  const totalPlaces = agencyTrajets.length * 12;
                  const rate = totalPlaces > 0 ? Math.round((agencyReservations.length / totalPlaces) * 100) : 0;

                  return (
                    <div key={agence.id_agence}>
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span className="text-gray-700 font-medium">{agence.nom}</span>
                        <span className="text-gray-900 font-bold">{rate}%</span>
                      </div>
                      <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] rounded-full transition-all"
                          style={{ width: `${rate}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="border border-gray-200 shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg font-semibold text-gray-900">Aperçu rapide</CardTitle>
            </CardHeader>
            <CardContent className="pt-0 space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 bg-blue-50 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-4 h-4 text-[#0891b2]" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">Taux de conversion</div>
                    <div className="text-xs text-gray-500">Réservations confirmées</div>
                  </div>
                </div>
                <div className="text-lg font-bold text-[#0c4a6e]">
                  {stats.totalReservations > 0 ? Math.round((stats.confirmed / stats.totalReservations) * 100) : 0}%
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 bg-green-50 rounded-lg flex items-center justify-center">
                    <Clock className="w-4 h-4 text-green-600" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">En attente de paiement</div>
                    <div className="text-xs text-gray-500">Réservations bloquées</div>
                  </div>
                </div>
                <div className="text-lg font-bold text-amber-600">{stats.pending}</div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 bg-purple-50 rounded-lg flex items-center justify-center">
                    <Bus className="w-4 h-4 text-purple-600" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">Bus en service</div>
                    <div className="text-xs text-gray-500">Flotte totale</div>
                  </div>
                </div>
                <div className="text-lg font-bold text-gray-900">{trajets.filter(t => !!t.bus).length}</div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
