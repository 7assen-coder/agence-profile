import { ArrowLeft, ArrowRight, Bus, Clock, MapPin, Users, Sun, Moon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import type { TrajetComplet, SearchParams } from '@/types';

interface ResultsSectionProps {
  results: TrajetComplet[];
  searchParams: SearchParams;
  onSelectTrajet: (trajet: TrajetComplet) => void;
  onBack: () => void;
}

export default function ResultsSection({ results, searchParams, onSelectTrajet, onBack }: ResultsSectionProps) {
  const departVille = results[0]?.ville_depart?.nom || '';
  const arriveeVille = results[0]?.ville_arrivee?.nom || '';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] text-white">
        <div className="max-w-5xl mx-auto px-6 py-8">
          <Button
            variant="ghost"
            onClick={onBack}
            className="text-white/80 hover:text-white hover:bg-white/10 mb-4 -ml-3"
          >
            <ArrowLeft className="w-4 h-4 mr-2" /> Retour à la recherche
          </Button>
          
          <h1 className="text-2xl font-bold mb-2">
            {departVille} <ArrowRight className="w-5 h-5 inline mx-2 text-cyan-300" /> {arriveeVille}
          </h1>
          <div className="flex items-center gap-4 text-cyan-100/80 text-sm">
            <span>{searchParams.date_trajet}</span>
            <span className="w-1 h-1 rounded-full bg-cyan-300"></span>
            <span>{results.length} trajet{results.length !== 1 ? 's' : ''} trouvé{results.length !== 1 ? 's' : ''}</span>
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="max-w-5xl mx-auto px-6 py-8">
        {results.length === 0 ? (
          <div className="text-center py-16">
            <Bus className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">Aucun trajet trouvé</h3>
            <p className="text-gray-500">Essayez avec une autre date ou une autre période.</p>
            <Button onClick={onBack} className="mt-4 bg-[#0891b2] hover:bg-[#067a96]">
              Modifier la recherche
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {results.map((trajet) => (
              <Card key={trajet.id_trajet} className="border border-gray-200 hover:shadow-lg transition-all duration-200 overflow-hidden">
                <CardContent className="p-0">
                  <div className="flex flex-col lg:flex-row">
                    {/* Left: Time & Route */}
                    <div className="flex-1 p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <div className="w-10 h-10 bg-[#0891b2]/10 rounded-lg flex items-center justify-center">
                            <Bus className="w-5 h-5 text-[#0891b2]" />
                          </div>
                          <div>
                            <div className="font-semibold text-gray-900">{trajet.agence?.nom}</div>
                            <div className="text-xs text-gray-500">Bus {trajet.bus?.immatriculation}</div>
                          </div>
                        </div>
                        <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium ${
                          trajet.periode === 'matin' 
                            ? 'bg-amber-50 text-amber-700' 
                            : 'bg-indigo-50 text-indigo-700'
                        }`}>
                          {trajet.periode === 'matin' ? <Sun className="w-3 h-3" /> : <Moon className="w-3 h-3" />}
                          {trajet.periode === 'matin' ? 'Matin' : 'Après-midi'}
                        </div>
                      </div>

                      <div className="flex items-center gap-6">
                        {/* Départ */}
                        <div className="text-center">
                          <div className="text-2xl font-bold text-gray-900">{trajet.heure_depart}</div>
                          <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                            <MapPin className="w-3 h-3" />
                            {trajet.ville_depart?.nom}
                          </div>
                        </div>

                        {/* Duration Line */}
                        <div className="flex-1 flex flex-col items-center px-4">
                          <div className="text-xs text-gray-400 mb-2 flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {calculateDuration(trajet.heure_depart, trajet.heure_arrivee)}
                          </div>
                          <div className="w-full h-0.5 bg-gray-200 relative">
                            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#0891b2]"></div>
                            <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#0891b2]"></div>
                          </div>
                          <div className="text-xs text-gray-400 mt-2">Direct</div>
                        </div>

                        {/* Arrivée */}
                        <div className="text-center">
                          <div className="text-2xl font-bold text-gray-900">{trajet.heure_arrivee}</div>
                          <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                            <MapPin className="w-3 h-3" />
                            {trajet.ville_arrivee?.nom}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Right: Price & Action */}
                    <div className="lg:w-64 bg-gray-50/80 border-t lg:border-t-0 lg:border-l border-gray-100 p-6 flex flex-col justify-center items-center">
                      <div className="text-center mb-4">
                        <div className="text-3xl font-bold text-[#0c4a6e]">{trajet.prix.toFixed(2)} <span className="text-lg">MRU</span></div>
                        <div className="text-xs text-gray-500 mt-1">par personne</div>
                      </div>
                      
                      <div className="flex items-center gap-1 text-sm text-gray-500 mb-4">
                        <Users className="w-4 h-4" />
                        <span className={trajet.places_disponibles! > 3 ? 'text-green-600' : 'text-amber-600'}>
                          {trajet.places_disponibles} place{trajet.places_disponibles !== 1 ? 's' : ''} disponible{trajet.places_disponibles !== 1 ? 's' : ''}
                        </span>
                      </div>

                      <Button
                        onClick={() => onSelectTrajet(trajet)}
                        className="w-full bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white rounded-xl h-11 font-medium shadow-lg shadow-[#0891b2]/20"
                      >
                        Choisir ce trajet <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function calculateDuration(depart: string, arrivee: string): string {
  const [h1, m1] = depart.split(':').map(Number);
  const [h2, m2] = arrivee.split(':').map(Number);
  let diff = (h2 * 60 + m2) - (h1 * 60 + m1);
  if (diff < 0) diff += 24 * 60;
  const hours = Math.floor(diff / 60);
  const mins = diff % 60;
  return `${hours}h ${mins.toString().padStart(2, '0')}min`;
}
