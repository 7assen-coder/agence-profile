import { useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Users,
  Ticket,
  CreditCard,
  ArrowUpRight,
  CalendarDays,
  PieChart,
  Activity,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { agences, villes, paiements, trajets, reservations } from '@/data/mockData';
import type { Agence, Ville, Paiement, TrajetComplet, ReservationComplet } from '@/types';

export default function AdminStatistiques() {
  const [reservationsData] = useState<ReservationComplet[]>(reservations);
  const [agencesData] = useState<Agence[]>(agences);
  const [villesData] = useState<Ville[]>(villes);
  const [paiementsData] = useState<Paiement[]>(paiements);
  const [trajetsData] = useState<TrajetComplet[]>(trajets);

  const totalRevenue = reservationsData
    .filter(r => r.statut === 'confirmee')
    .reduce((sum, r) => sum + (r.paiement?.montant || 0), 0);

  const revenueByAgence = agencesData.map(a => {
    const revenue = reservationsData
      .filter(r => r.trajet?.id_agence === a.id_agence && r.statut === 'confirmee')
      .reduce((sum, r) => sum + (r.paiement?.montant || 0), 0);
    return { ...a, revenue };
  }).sort((a, b) => b.revenue - a.revenue);

  const reservationsByStatus = {
    confirmee: reservationsData.filter(r => r.statut === 'confirmee').length,
    en_attente: reservationsData.filter(r => r.statut === 'en_attente').length,
    annulee: reservationsData.filter(r => r.statut === 'annulee').length,
  };

  const paymentModes = {
    carte: paiementsData.filter(p => p.mode_paiement === 'carte').length,
    mobile_money: paiementsData.filter(p => p.mode_paiement === 'mobile_money').length,
    virement: paiementsData.filter(p => p.mode_paiement === 'virement').length,
    especes: paiementsData.filter(p => p.mode_paiement === 'especes').length,
  };

  const topRoutes = trajetsData.map(t => {
    const count = reservationsData.filter(r => r.id_trajet === t.id_trajet && r.statut === 'confirmee').length;
    return { ...t, count };
  }).sort((a, b) => b.count - a.count).slice(0, 5);

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Statistiques</h1>
        <p className="text-sm text-gray-500 mt-1">Analyse détaillée des performances</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Revenus totaux</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{totalRevenue.toFixed(0)} MRU</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-green-600">
                  <ArrowUpRight className="w-3 h-3" />
                  <span>+15% vs mois dernier</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-green-50 rounded-xl flex items-center justify-center">
                <CreditCard className="w-5 h-5 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Billets vendus</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{reservationsData.filter(r => r.statut === 'confirmee').length}</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-green-600">
                  <ArrowUpRight className="w-3 h-3" />
                  <span>+8% ce mois</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-[#0891b2]/10 rounded-xl flex items-center justify-center">
                <Ticket className="w-5 h-5 text-[#0891b2]" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Nouveaux clients</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">{new Set(reservationsData.map(r => r.id_client)).size}</h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-gray-500">
                  <Users className="w-3 h-3" />
                  <span>Clients uniques</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-purple-50 rounded-xl flex items-center justify-center">
                <Users className="w-5 h-5 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200 shadow-sm">
          <CardContent className="p-5">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Taux de remplissage</p>
                <h3 className="text-2xl font-bold text-gray-900 mt-1">
                  {Math.round((reservationsData.filter(r => r.statut === 'confirmee').length / (trajetsData.length * 12)) * 100)}%
                </h3>
                <div className="flex items-center gap-1 mt-2 text-xs text-green-600">
                  <TrendingUp className="w-3 h-3" />
                  <span>+5% cette semaine</span>
                </div>
              </div>
              <div className="w-11 h-11 bg-amber-50 rounded-xl flex items-center justify-center">
                <Activity className="w-5 h-5 text-amber-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue by Agency */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-[#0891b2]" />
              Revenus par agence
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-4">
              {revenueByAgence.map(agency => (
                <div key={agency.id_agence}>
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="text-gray-700 font-medium">{agency.nom}</span>
                    <span className="text-gray-900 font-bold">{agency.revenue.toFixed(0)} MRU</span>
                  </div>
                  <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] rounded-full transition-all"
                         style={{ width: `${totalRevenue > 0 ? (agency.revenue / totalRevenue) * 100 : 0}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Payment Methods */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <PieChart className="w-5 h-5 text-[#0891b2]" />
              Modes de paiement
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-4">
              {Object.entries(paymentModes).map(([mode, count]) => {
                const labels: Record<string, string> = {
                  carte: 'Carte bancaire',
                  mobile_money: 'Mobile Money',
                  virement: 'Virement bancaire',
                  especes: 'Espèces',
                };
                const colors: Record<string, string> = {
                  carte: 'from-blue-500 to-blue-600',
                  mobile_money: 'from-green-500 to-green-600',
                  virement: 'from-purple-500 to-purple-600',
                  especes: 'from-amber-500 to-amber-600',
                };
                const total = Object.values(paymentModes).reduce((a, b) => a + b, 0);
                return (
                  <div key={mode}>
                    <div className="flex items-center justify-between text-sm mb-2">
                      <span className="text-gray-700 font-medium">{labels[mode]}</span>
                      <span className="text-gray-900 font-bold">{count} ({total > 0 ? Math.round((count / total) * 100) : 0}%)</span>
                    </div>
                    <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                      <div className={`h-full bg-gradient-to-r ${colors[mode]} rounded-full transition-all`}
                           style={{ width: `${total > 0 ? (count / total) * 100 : 0}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Top Routes */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <CalendarDays className="w-5 h-5 text-[#0891b2]" />
              Trajets les plus réservés
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-3">
              {topRoutes.map((route, idx) => {
                const depart = villesData.find(v => v.id_ville === route.id_ville_depart);
                const arrivee = villesData.find(v => v.id_ville === route.id_ville_arrivee);
                return (
                  <div key={route.id_trajet} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-[#0891b2]/10 rounded-lg flex items-center justify-center text-sm font-bold text-[#0891b2]">
                        {idx + 1}
                      </div>
                      <div>
                        <div className="font-medium text-gray-900 text-sm">{depart?.nom} → {arrivee?.nom}</div>
                        <div className="text-xs text-gray-500">{route.date_trajet} | {route.heure_depart}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-gray-900">{route.count} résa.</div>
                      <div className="text-xs text-gray-500">{route.prix.toFixed(0)} MRU</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Status Distribution */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Activity className="w-5 h-5 text-[#0891b2]" />
              Distribution des statuts
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-4">
              {Object.entries(reservationsByStatus).map(([status, count]) => {
                const labels: Record<string, string> = {
                  confirmee: 'Confirmées',
                  en_attente: 'En attente',
                  annulee: 'Annulées',
                };
                const colors: Record<string, string> = {
                  confirmee: 'from-green-500 to-green-600',
                  en_attente: 'from-amber-500 to-amber-600',
                  annulee: 'from-red-500 to-red-600',
                };
                const total = Object.values(reservationsByStatus).reduce((a, b) => a + b, 0);
                return (
                  <div key={status}>
                    <div className="flex items-center justify-between text-sm mb-2">
                      <span className="text-gray-700 font-medium">{labels[status]}</span>
                      <span className="text-gray-900 font-bold">{count} ({total > 0 ? Math.round((count / total) * 100) : 0}%)</span>
                    </div>
                    <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                      <div className={`h-full bg-gradient-to-r ${colors[status]} rounded-full transition-all`}
                           style={{ width: `${total > 0 ? (count / total) * 100 : 0}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
