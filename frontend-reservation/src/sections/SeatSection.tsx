import { useState, useEffect } from 'react';
import { ArrowLeft, Bus, Check, Info, MapPin, Armchair } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { getPlacesForTrajet } from '@/services/api';
import type { TrajetComplet, Place } from '@/types';

interface SeatSectionProps {
  trajet: TrajetComplet;
  onSelectPlace: (place: Place) => void;
  onBack: () => void;
}

export default function SeatSection({ trajet, onSelectPlace, onBack }: SeatSectionProps) {
  const [places, setPlaces] = useState<(Place & { statut: 'disponible' | 'reservee' | 'selectionnee' })[]>([]);
  const [selectedPlace, setSelectedPlace] = useState<Place | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPlacesForTrajet(trajet.id_trajet).then(data => {
      setPlaces(data as (Place & { statut: 'disponible' | 'reservee' | 'selectionnee' })[]);
      setLoading(false);
    });
  }, [trajet.id_trajet]);

  const handleSeatClick = (place: Place & { statut: string }) => {
    if (place.statut === 'reservee') return;
    
    setPlaces(prev => prev.map(p => ({
      ...p,
      statut: p.id_place === place.id_place ? 'selectionnee' : (p.statut === 'selectionnee' ? 'disponible' : p.statut)
    })));
    
    if (place.statut !== 'selectionnee') {
      setSelectedPlace(place);
    } else {
      setSelectedPlace(null);
    }
  };

  const handleConfirm = () => {
    if (selectedPlace) {
      onSelectPlace(selectedPlace);
    }
  };

  // Organiser les places en rangées (3 colonnes × 4 rangées = 12 places)
  // Layout: [1] [2]   [3]
  //         [4] [5]   [6]
  //         [7] [8]   [9]
  //         [10][11] [12]
  const rows: number[][] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
  ];

  const getPlaceByNumero = (num: number) => places.find(p => p.numero_place === num);

  const disponiblesCount = places.filter(p => p.statut === 'disponible').length;
  const reserveesCount = places.filter(p => p.statut === 'reservee').length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] text-white">
        <div className="max-w-4xl mx-auto px-6 py-6">
          <Button
            variant="ghost"
            onClick={onBack}
            className="text-white/80 hover:text-white hover:bg-white/10 mb-3 -ml-3"
          >
            <ArrowLeft className="w-4 h-4 mr-2" /> Retour aux trajets
          </Button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold">Sélectionner votre place</h1>
              <div className="flex items-center gap-2 text-cyan-100/80 text-sm mt-1">
                <MapPin className="w-4 h-4" />
                {trajet.ville_depart?.nom} → {trajet.ville_arrivee?.nom}
                <span className="mx-1">|</span>
                <Bus className="w-4 h-4" />
                {trajet.bus?.immatriculation}
                <span className="mx-1">|</span>
                {trajet.date_trajet}
              </div>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold">{trajet.prix.toFixed(2)} MRU</div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Seat Map */}
          <div className="lg:col-span-2">
            <Card className="border border-gray-200 shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                    <Armchair className="w-5 h-5 text-[#0891b2]" />
                    Plan du bus
                  </h2>
                  <div className="flex items-center gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 rounded bg-white border-2 border-gray-300"></div>
                      <span className="text-gray-600">Disponible</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 rounded bg-[#0891b2] border-2 border-[#0891b2]"></div>
                      <span className="text-gray-600">Sélectionnée</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 rounded bg-gray-200 border-2 border-gray-300"></div>
                      <span className="text-gray-600">Réservée</span>
                    </div>
                  </div>
                </div>

                {loading ? (
                  <div className="flex items-center justify-center py-16">
                    <div className="w-8 h-8 border-2 border-[#0891b2]/30 border-t-[#0891b2] rounded-full animate-spin"></div>
                  </div>
                ) : (
                  <div className="relative">
                    {/* Front of bus indicator */}
                    <div className="flex items-center justify-center mb-6">
                      <div className="bg-gray-100 rounded-t-3xl px-8 py-3 text-sm text-gray-500 font-medium">
                        <Bus className="w-5 h-5 inline mr-2" />
                        AVANT DU BUS
                      </div>
                    </div>

                    {/* Seat Grid */}
                    <div className="space-y-3 max-w-sm mx-auto">
                      {rows.map((row, rowIdx) => (
                        <div key={rowIdx} className="flex items-center justify-center gap-3">
                          {row.map((seatNum, colIdx) => {
                            const place = getPlaceByNumero(seatNum);
                            if (!place) return null;

                            const isSelected = place.statut === 'selectionnee';
                            const isReserved = place.statut === 'reservee';

                            // Aisle between col 1 and col 2
                            const isAisle = colIdx === 1;

                            return (
                              <div key={seatNum} className="flex items-center gap-3">
                                {isAisle && <div className="w-10"></div>}
                                <button
                                  onClick={() => handleSeatClick(place)}
                                  disabled={isReserved}
                                  className={`
                                    relative w-16 h-16 rounded-xl border-2 transition-all duration-200 flex flex-col items-center justify-center
                                    ${isReserved 
                                      ? 'bg-gray-100 border-gray-200 cursor-not-allowed opacity-60' 
                                      : isSelected
                                        ? 'bg-[#0891b2] border-[#0891b2] text-white shadow-lg shadow-[#0891b2]/30 scale-105'
                                        : 'bg-white border-gray-300 hover:border-[#0891b2] hover:shadow-md cursor-pointer'
                                    }
                                  `}
                                >
                                  {isSelected && (
                                    <Check className="w-4 h-4 absolute top-1 right-1" />
                                  )}
                                  <Armchair className={`w-6 h-6 ${isReserved ? 'text-gray-400' : isSelected ? 'text-white' : 'text-gray-600'}`} />
                                  <span className={`text-xs font-bold mt-0.5 ${isReserved ? 'text-gray-400' : isSelected ? 'text-white' : 'text-gray-700'}`}>
                                    {seatNum}
                                  </span>
                                </button>
                              </div>
                            );
                          })}
                        </div>
                      ))}
                    </div>

                    {/* Back of bus indicator */}
                    <div className="flex items-center justify-center mt-6">
                      <div className="bg-gray-100 rounded-b-3xl px-8 py-3 text-sm text-gray-500 font-medium w-48 text-center">
                        ARRIÈRE
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Info card */}
            <Card className="mt-4 border border-gray-200">
              <CardContent className="p-4 flex items-start gap-3">
                <Info className="w-5 h-5 text-[#0891b2] flex-shrink-0 mt-0.5" />
                <div className="text-sm text-gray-600">
                  <p className="font-medium text-gray-800 mb-1">Informations importantes</p>
                  <p>• Votre place est bloquée temporairement pendant 15 minutes pendant le paiement.</p>
                  <p>• Sans confirmation de paiement, la place sera libérée automatiquement.</p>
                  <p>• Présentez votre ticket digital ou imprimé au conducteur.</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar Summary */}
          <div className="lg:col-span-1">
            <Card className="border border-gray-200 shadow-lg sticky top-6">
              <CardContent className="p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Résumé</h3>
                
                <div className="space-y-3 text-sm mb-6">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Agence</span>
                    <span className="font-medium text-gray-900">{trajet.agence?.nom}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Trajet</span>
                    <span className="font-medium text-gray-900">{trajet.ville_depart?.nom} → {trajet.ville_arrivee?.nom}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Date</span>
                    <span className="font-medium text-gray-900">{trajet.date_trajet}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Heure</span>
                    <span className="font-medium text-gray-900">{trajet.heure_depart}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Bus</span>
                    <span className="font-medium text-gray-900">{trajet.bus?.immatriculation}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Places dispo.</span>
                    <span className="font-medium text-green-600">{disponiblesCount} / 12</span>
                  </div>
                </div>

                <div className="border-t border-gray-100 pt-4 mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-500">Place sélectionnée</span>
                    <span className="font-semibold text-gray-900">
                      {selectedPlace ? `N° ${selectedPlace.numero_place}` : '-'}
                    </span>
                  </div>
                </div>

                <div className="border-t border-gray-100 pt-4 mb-6">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-700 font-medium">Total</span>
                    <span className="text-2xl font-bold text-[#0c4a6e]">{trajet.prix.toFixed(2)} MRU</span>
                  </div>
                </div>

                <Button
                  onClick={handleConfirm}
                  disabled={!selectedPlace}
                  className="w-full bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white rounded-xl h-12 font-medium shadow-lg shadow-[#0891b2]/20 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Continuer vers le paiement
                </Button>

                <p className="text-xs text-gray-400 text-center mt-3">
                  {reserveesCount} place{reserveesCount !== 1 ? 's' : ''} déjà réservée{reserveesCount !== 1 ? 's' : ''}
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
