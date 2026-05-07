import { useState, useEffect } from 'react';
import { MapPin, Calendar, Sun, Bus, ArrowRight, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { getVilles, searchTrajets } from '@/services/api';
import type { Ville, SearchParams, TrajetComplet } from '@/types';

interface SearchSectionProps {
  onSearchResults: (results: TrajetComplet[], params: SearchParams) => void;
}

export default function SearchSection({ onSearchResults }: SearchSectionProps) {
  const [villes, setVilles] = useState<Ville[]>([]);
  const [depart, setDepart] = useState<string>('');
  const [arrivee, setArrivee] = useState<string>('');
  const [date, setDate] = useState<string>('');
  const [periode, setPeriode] = useState<'matin' | 'apres-midi' | 'tous'>('tous');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    getVilles().then(setVilles);
    // Set default date to today
    setDate(new Date().toISOString().split('T')[0]);
  }, []);

  const handleSearch = async () => {
    const newErrors: Record<string, string> = {};
    if (!depart) newErrors.depart = 'Sélectionnez une ville de départ';
    if (!arrivee) newErrors.arrivee = 'Sélectionnez une ville d\'arrivée';
    if (!date) newErrors.date = 'Sélectionnez une date';
    if (depart && arrivee && depart === arrivee) newErrors.arrivee = 'La ville d\'arrivée doit être différente';
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    const params: SearchParams = {
      id_ville_depart: parseInt(depart),
      id_ville_arrivee: parseInt(arrivee),
      date_trajet: date,
      periode,
    };

    const results = await searchTrajets(params);
    onSearchResults(results, params);
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-[#0c4a6e] via-[#075985] to-[#0891b2] text-white overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-32 h-32 rounded-full bg-white/20"></div>
          <div className="absolute bottom-20 right-20 w-48 h-48 rounded-full bg-white/10"></div>
          <div className="absolute top-40 right-40 w-24 h-24 rounded-full bg-white/15"></div>
        </div>
        
        <div className="relative z-10 px-6 pt-16 pb-24 max-w-7xl mx-auto">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
              <Bus className="w-7 h-7" />
            </div>
            <span className="text-xl font-bold tracking-tight">TransportReserve</span>
          </div>
          
          <div className="max-w-2xl">
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Réservez votre voyage<br />
              <span className="text-cyan-300">en toute simplicité</span>
            </h1>
            <p className="text-lg text-cyan-100/80 mb-10 leading-relaxed max-w-lg">
              Découvrez une nouvelle façon de voyager entre les villes. 
              Réservez votre place en temps réel, payez en ligne et recevez votre ticket instantanément.
            </p>
            
            <div className="flex items-center gap-6 text-sm text-cyan-200">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>Réservation rapide</span>
              </div>
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                <span>10 villes couvertes</span>
              </div>
              <div className="flex items-center gap-2">
                <Bus className="w-4 h-4" />
                <span>4 agences partenaires</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Search Form Card */}
      <div className="px-6 -mt-16 mb-12 max-w-5xl mx-auto w-full">
        <Card className="shadow-2xl border-0 bg-white">
          <CardContent className="p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center gap-2">
              <Bus className="w-5 h-5 text-[#0891b2]" />
              Rechercher un trajet
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-6">
              {/* Ville départ */}
              <div className="space-y-2">
                <Label htmlFor="depart" className="text-gray-700 font-medium">
                  <MapPin className="w-4 h-4 inline mr-1 text-[#0891b2]" />
                  Ville de départ
                </Label>
                <select
                  id="depart"
                  value={depart}
                  onChange={(e) => { setDepart(e.target.value); setErrors(prev => ({ ...prev, depart: '' })); }}
                  className={`w-full h-11 px-3 rounded-lg border ${errors.depart ? 'border-red-400' : 'border-gray-200'} bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#0891b2] focus:border-transparent text-gray-900`}
                >
                  <option value="">Choisir...</option>
                  {villes.map(v => (
                    <option key={v.id_ville} value={v.id_ville}>{v.nom}</option>
                  ))}
                </select>
                {errors.depart && <p className="text-xs text-red-500">{errors.depart}</p>}
              </div>

              {/* Ville arrivée */}
              <div className="space-y-2">
                <Label htmlFor="arrivee" className="text-gray-700 font-medium">
                  <MapPin className="w-4 h-4 inline mr-1 text-[#0891b2]" />
                  Ville d'arrivée
                </Label>
                <select
                  id="arrivee"
                  value={arrivee}
                  onChange={(e) => { setArrivee(e.target.value); setErrors(prev => ({ ...prev, arrivee: '' })); }}
                  className={`w-full h-11 px-3 rounded-lg border ${errors.arrivee ? 'border-red-400' : 'border-gray-200'} bg-gray-50 focus:outline-none focus:ring-2 focus:ring-[#0891b2] focus:border-transparent text-gray-900`}
                >
                  <option value="">Choisir...</option>
                  {villes.map(v => (
                    <option key={v.id_ville} value={v.id_ville}>{v.nom}</option>
                  ))}
                </select>
                {errors.arrivee && <p className="text-xs text-red-500">{errors.arrivee}</p>}
              </div>

              {/* Date */}
              <div className="space-y-2">
                <Label htmlFor="date" className="text-gray-700 font-medium">
                  <Calendar className="w-4 h-4 inline mr-1 text-[#0891b2]" />
                  Date du voyage
                </Label>
                <Input
                  id="date"
                  type="date"
                  value={date}
                  min={new Date().toISOString().split('T')[0]}
                  onChange={(e) => { setDate(e.target.value); setErrors(prev => ({ ...prev, date: '' })); }}
                  className={`h-11 ${errors.date ? 'border-red-400' : ''}`}
                />
                {errors.date && <p className="text-xs text-red-500">{errors.date}</p>}
              </div>

              {/* Période */}
              <div className="space-y-2">
                <Label className="text-gray-700 font-medium">
                  <Sun className="w-4 h-4 inline mr-1 text-[#0891b2]" />
                  Période
                </Label>
                <RadioGroup
                  value={periode}
                  onValueChange={(v) => setPeriode(v as 'matin' | 'apres-midi' | 'tous')}
                  className="flex gap-2"
                >
                  <div className="flex items-center space-x-1">
                    <RadioGroupItem value="matin" id="matin" className="text-[#0891b2]" />
                    <Label htmlFor="matin" className="text-sm cursor-pointer">Matin</Label>
                  </div>
                  <div className="flex items-center space-x-1">
                    <RadioGroupItem value="apres-midi" id="apres-midi" className="text-[#0891b2]" />
                    <Label htmlFor="apres-midi" className="text-sm cursor-pointer">Après-midi</Label>
                  </div>
                  <div className="flex items-center space-x-1">
                    <RadioGroupItem value="tous" id="tous" className="text-[#0891b2]" />
                    <Label htmlFor="tous" className="text-sm cursor-pointer">Tous</Label>
                  </div>
                </RadioGroup>
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-gray-100">
              <div className="text-sm text-gray-500">
                <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                Réservation en temps réel
              </div>
              <Button
                onClick={handleSearch}
                disabled={loading}
                className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white px-8 h-12 text-base font-medium rounded-xl shadow-lg shadow-[#0891b2]/20 transition-all"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Recherche...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    Rechercher <ArrowRight className="w-4 h-4" />
                  </span>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Popular Routes */}
      <div className="px-6 max-w-5xl mx-auto w-full pb-16">
        <h3 className="text-lg font-semibold text-gray-800 mb-5">Trajets populaires</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { from: 'Nouakchott', to: 'Nouadhibou', prix: '850 MRU', time: '6h 00min' },
            { from: 'Nouakchott', to: 'Kaédi', prix: '700 MRU', time: '8h 00min' },
            { from: 'Nouadhibou', to: 'Sélibabi', prix: '1500 MRU', time: '14h 00min' },
          ].map((route, idx) => (
            <Card key={idx} className="border border-gray-100 hover:shadow-md transition-shadow cursor-pointer bg-gray-50/50">
              <CardContent className="p-4 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 text-sm font-medium text-gray-900">
                    <MapPin className="w-4 h-4 text-[#0891b2]" />
                    {route.from}
                    <ArrowRight className="w-3 h-3 text-gray-400" />
                    {route.to}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{route.time}</div>
                </div>
                <div className="text-right">
                  <div className="text-[#0891b2] font-bold">{route.prix}</div>
                  <div className="text-xs text-gray-400">par personne</div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
