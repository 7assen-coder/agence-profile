import { useState, useEffect } from 'react';
import {
  CalendarDays,
  MapPin,
  Clock,
  Sun,
  Moon,
  Bus,
  Armchair,
  Search,
  TrendingUp,
  ArrowUpRight,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { getAllTrajets } from '@/services/api';
import type { TrajetComplet } from '@/types';

export default function AdminTrajets() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterPeriode, setFilterPeriode] = useState<'tous' | 'matin' | 'apres-midi'>('tous');
  const [trajetsComplet, setTrajetsComplet] = useState<TrajetComplet[]>([]);

  useEffect(() => {
    getAllTrajets().then((data: TrajetComplet[]) => setTrajetsComplet(data));
  }, []);

  const filtered = trajetsComplet
    .filter(t => filterPeriode === 'tous' || t.periode === filterPeriode)
    .filter(t => {
      if (!searchTerm) return true;
      const term = searchTerm.toLowerCase();
      return (
        t.ville_depart?.nom.toLowerCase().includes(term) ||
        t.ville_arrivee?.nom.toLowerCase().includes(term) ||
        t.agence?.nom.toLowerCase().includes(term)
      );
    });

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Gestion des trajets</h1>
        <p className="text-sm text-gray-500 mt-1">Tous les trajets et leur disponibilité</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-[#0891b2]/10 rounded-xl flex items-center justify-center">
              <CalendarDays className="w-6 h-6 text-[#0891b2]" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{trajetsComplet.length}</div>
              <div className="text-sm text-gray-500">Trajets programmés</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center">
              <Sun className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{trajetsComplet.filter(t => t.periode === 'matin').length}</div>
              <div className="text-sm text-gray-500">Départs matin</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center">
              <Moon className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">{trajetsComplet.filter(t => t.periode === 'apres-midi').length}</div>
              <div className="text-sm text-gray-500">Départs après-midi</div>
            </div>
          </CardContent>
        </Card>
        <Card className="border border-gray-200">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {trajetsComplet.reduce((sum, t) => sum + t.prix, 0).toFixed(0)} MRU
              </div>
              <div className="text-sm text-gray-500">Revenus potentiels</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-2 bg-white rounded-xl p-1 border border-gray-200 shadow-sm">
          <button onClick={() => setFilterPeriode('tous')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterPeriode === 'tous' ? 'bg-[#0891b2] text-white' : 'text-gray-600 hover:bg-gray-50'}`}>Tous</button>
          <button onClick={() => setFilterPeriode('matin')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterPeriode === 'matin' ? 'bg-amber-500 text-white' : 'text-gray-600 hover:bg-gray-50'}`}>Matin</button>
          <button onClick={() => setFilterPeriode('apres-midi')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${filterPeriode === 'apres-midi' ? 'bg-indigo-500 text-white' : 'text-gray-600 hover:bg-gray-50'}`}>Après-midi</button>
        </div>
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <Input placeholder="Rechercher par ville, agence..." value={searchTerm} onChange={e => setSearchTerm(e.target.value)} className="pl-10" />
        </div>
      </div>

      {/* Trajets Table */}
      <Card className="border border-gray-200 shadow-sm">
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50/80">
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">ID</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Route</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Date & Période</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Horaires</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Agence / Bus</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Places</th>
                  <th className="text-left px-4 py-3 font-semibold text-gray-700">Prix</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((t, idx) => (
                  <tr key={t.id_trajet} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/50'}>
                    <td className="px-4 py-4 font-mono text-gray-500">#{t.id_trajet}</td>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-1 font-medium text-gray-900">
                        <MapPin className="w-3 h-3 text-[#0891b2]" />
                        {t.ville_depart?.nom}
                        <ArrowUpRight className="w-3 h-3 text-gray-400" />
                        {t.ville_arrivee?.nom}
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="text-gray-700">{t.date_trajet}</div>
                      <Badge className={`mt-1 text-xs ${t.periode === 'matin' ? 'bg-amber-100 text-amber-700 hover:bg-amber-100' : 'bg-indigo-100 text-indigo-700 hover:bg-indigo-100'}`}>
                        {t.periode === 'matin' ? <Sun className="w-3 h-3 mr-1" /> : <Moon className="w-3 h-3 mr-1" />}
                        {t.periode === 'matin' ? 'Matin' : 'Après-midi'}
                      </Badge>
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-1 text-gray-700">
                        <Clock className="w-3 h-3 text-gray-400" />
                        {t.heure_depart} → {t.heure_arrivee}
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="text-gray-900 font-medium">{t.agence?.nom}</div>
                      <div className="text-xs text-gray-500 flex items-center gap-1">
                        <Bus className="w-3 h-3" /> {t.bus?.immatriculation}
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-1">
                        <Armchair className="w-4 h-4 text-[#0891b2]" />
                        <span className={`font-medium ${(t.places_disponibles || 0) > 6 ? 'text-green-600' : (t.places_disponibles || 0) > 3 ? 'text-amber-600' : 'text-red-600'}`}>
                          {t.places_disponibles} / 12
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-4">
                      <div className="font-bold text-[#0c4a6e]">{t.prix.toFixed(2)} MRU</div>
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
