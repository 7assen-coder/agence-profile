import { useState, useCallback } from 'react';
import type { BookingFlow, TrajetComplet, Place, Client, Paiement, Reservation } from '@/types';

export function useReservation() {
  const [flow, setFlow] = useState<BookingFlow>({ step: 'search' });

  const goToSearch = useCallback(() => setFlow({ step: 'search' }), []);
  
  const goToResults = useCallback(() => {
    setFlow(prev => ({ ...prev, step: 'results' }));
  }, []);

  const selectTrajet = useCallback((trajet: TrajetComplet) => {
    setFlow(prev => ({ ...prev, step: 'seats', selectedTrajet: trajet }));
  }, []);

  const selectPlace = useCallback((place: Place) => {
    setFlow(prev => ({ ...prev, step: 'payment', selectedPlace: place }));
  }, []);

  const setClientInfo = useCallback((client: Partial<Client>, paiement?: Partial<Paiement>) => {
    setFlow(prev => ({ ...prev, client, paiement }));
  }, []);

  const completeBooking = useCallback((reservation: Reservation) => {
    setFlow(prev => ({ ...prev, step: 'ticket', reservation }));
  }, []);

  const goBack = useCallback(() => {
    setFlow(prev => {
      const steps: BookingFlow['step'][] = ['search', 'results', 'seats', 'payment', 'ticket'];
      const currentIdx = steps.indexOf(prev.step);
      if (currentIdx > 0) {
        const prevStep = steps[currentIdx - 1];
        return { ...prev, step: prevStep };
      }
      return prev;
    });
  }, []);

  return {
    flow,
    goToSearch,
    goToResults,
    selectTrajet,
    selectPlace,
    setClientInfo,
    completeBooking,
    goBack,
  };
}
