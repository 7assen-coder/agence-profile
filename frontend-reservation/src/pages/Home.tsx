import { useState, useCallback } from 'react';
import SearchSection from '@/sections/SearchSection';
import ResultsSection from '@/sections/ResultsSection';
import SeatSection from '@/sections/SeatSection';
import { creerReservation } from '@/services/api';
import type { TrajetComplet, Place, SearchParams } from '@/types';

// Seulement 3 étapes — paiement et ticket appartiennent à d'autres modules
type Step = 'search' | 'results' | 'seats' | 'confirmation';

export default function Home() {
  const [step, setStep]                   = useState<Step>('search');
  const [searchResults, setSearchResults] = useState<TrajetComplet[]>([]);
  const [searchParams, setSearchParams]   = useState<SearchParams | null>(null);
  const [selectedTrajet, setSelectedTrajet] = useState<TrajetComplet | null>(null);
  const [reservationId, setReservationId] = useState<number | null>(null);
  const [loading, setLoading]             = useState(false);
  const [error, setError]                 = useState<string | null>(null);

  const handleSearchResults = useCallback((results: TrajetComplet[], params: SearchParams) => {
    setSearchResults(results);
    setSearchParams(params);
    setStep('results');
  }, []);

  const handleSelectTrajet = useCallback((trajet: TrajetComplet) => {
    setSelectedTrajet(trajet);
    setStep('seats');
  }, []);

  // Quand le client choisit une place → on bloque la place côté Flask
  const handleSelectPlace = useCallback(async (place: Place) => {
    if (!selectedTrajet) return;
    setLoading(true);
    setError(null);

    try {
      const reservation = await creerReservation({
        trajet_id:    selectedTrajet.id_trajet,
        client_nom:   'Client',          // sera complété par le module Paiement
        client_email: 'temp@temp.com',   // sera complété par le module Paiement
        numero_place: place.numero_place,
      });
      setReservationId(reservation.id_reservation);
      setStep('confirmation');
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Erreur lors de la réservation';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [selectedTrajet]);

  const handleBack = useCallback(() => {
    const order: Step[] = ['search', 'results', 'seats', 'confirmation'];
    const idx = order.indexOf(step);
    if (idx > 0) setStep(order[idx - 1]);
  }, [step]);

  const handleNewBooking = useCallback(() => {
    setStep('search');
    setSearchResults([]);
    setSearchParams(null);
    setSelectedTrajet(null);
    setReservationId(null);
    setError(null);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">

      {step === 'search' && (
        <SearchSection onSearchResults={handleSearchResults} />
      )}

      {step === 'results' && searchParams && (
        <ResultsSection
          results={searchResults}
          searchParams={searchParams}
          onSelectTrajet={handleSelectTrajet}
          onBack={handleBack}
        />
      )}

      {step === 'seats' && selectedTrajet && (
        <>
          {error && (
            <div className="max-w-4xl mx-auto px-6 pt-4">
              <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm">
                ⚠️ {error}
              </div>
            </div>
          )}
          <SeatSection
            trajet={selectedTrajet}
            onSelectPlace={handleSelectPlace}
            onBack={handleBack}
          />
          {loading && (
            <div className="fixed inset-0 bg-black/20 flex items-center justify-center z-50">
              <div className="bg-white rounded-xl px-8 py-6 shadow-xl flex items-center gap-4">
                <div className="w-6 h-6 border-2 border-[#0891b2]/30 border-t-[#0891b2] rounded-full animate-spin" />
                <span className="text-gray-700 font-medium">Blocage de la place en cours…</span>
              </div>
            </div>
          )}
        </>
      )}

      {/* Confirmation — la place est bloquée, le module Paiement prend le relais */}
      {step === 'confirmation' && reservationId && selectedTrajet && (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
          <div className="bg-white rounded-2xl shadow-xl p-10 max-w-md w-full text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>

            <h2 className="text-2xl font-bold text-gray-900 mb-2">Place bloquée !</h2>
            <p className="text-gray-500 mb-6">
              Votre place est réservée temporairement pendant <strong>15 minutes</strong>.
              Procédez au paiement pour confirmer définitivement.
            </p>

            <div className="bg-gray-50 rounded-xl p-4 mb-6 text-left space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">N° de réservation</span>
                <span className="font-bold text-[#0c4a6e]">#{reservationId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Trajet</span>
                <span className="font-medium">
                  {selectedTrajet.ville_depart?.nom} → {selectedTrajet.ville_arrivee?.nom}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Date</span>
                <span className="font-medium">{selectedTrajet.date_trajet}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Prix</span>
                <span className="font-bold text-[#0c4a6e]">{selectedTrajet.prix} MRU</span>
              </div>
            </div>

            <p className="text-xs text-amber-600 bg-amber-50 rounded-lg p-3 mb-6">
              ⏱ Sans paiement dans les 15 min, la place sera automatiquement libérée.
            </p>

            <button
              onClick={handleNewBooking}
              className="w-full bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] text-white rounded-xl h-12 font-medium"
            >
              Faire une nouvelle réservation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
