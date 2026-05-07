import { useEffect, useState } from 'react';
import { Download, Share2, Bus, MapPin, Clock, Calendar, User, CreditCard, Armchair, CheckCircle, Home } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { getReservationComplete } from '@/services/api';
import type { ReservationComplet } from '@/types';

interface TicketSectionProps {
  reservationId: number;
  onNewBooking: () => void;
}

export default function TicketSection({ reservationId, onNewBooking }: TicketSectionProps) {
  const [reservation, setReservation] = useState<ReservationComplet | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getReservationComplete(reservationId).then((data) => {
      setReservation(data as ReservationComplet);
      setLoading(false);
    });
  }, [reservationId]);

  const generateTicketCode = () => {
    if (!reservation) return '';
    const date = new Date(reservation.date_reservation);
    const dateStr = date.toISOString().slice(0, 10).replace(/-/g, '');
    return `TR${dateStr}-${reservation.id_reservation.toString().padStart(4, '0')}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-[#0891b2]/30 border-t-[#0891b2] rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!reservation) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-500">Réservation non trouvée</p>
          <Button onClick={onNewBooking} className="mt-4 bg-[#0891b2]">Nouvelle réservation</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0c4a6e] via-[#075985] to-gray-50">
      {/* Header */}
      <div className="text-white py-12 text-center">
        <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle className="w-8 h-8" />
        </div>
        <h1 className="text-3xl font-bold mb-2">Réservation confirmée !</h1>
        <p className="text-cyan-100/80">Votre ticket est prêt. Présentez-le au conducteur.</p>
      </div>

      <div className="max-w-lg mx-auto px-6 pb-16">
        {/* Ticket Card */}
        <Card className="border-0 shadow-2xl overflow-hidden bg-white">
          {/* Ticket Header */}
          <div className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] text-white p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                  <Bus className="w-6 h-6" />
                </div>
                <div>
                  <div className="font-bold text-lg">{reservation.trajet?.agence?.nom}</div>
                  <div className="text-sm text-cyan-200">{reservation.trajet?.bus?.immatriculation}</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-xs text-cyan-200">N° Ticket</div>
                <div className="font-mono font-bold">{generateTicketCode()}</div>
              </div>
            </div>
          </div>

          {/* Ticket Body */}
          <CardContent className="p-6">
            {/* Route */}
            <div className="flex items-center justify-between mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{reservation.trajet?.heure_depart}</div>
                <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                  <MapPin className="w-3 h-3" />
                  {reservation.trajet?.ville_depart?.nom}
                </div>
              </div>

              <div className="flex-1 flex flex-col items-center px-4">
                <div className="text-xs text-gray-400 mb-1 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {calculateDuration(reservation.trajet?.heure_depart || '', reservation.trajet?.heure_arrivee || '')}
                </div>
                <div className="w-full h-0.5 bg-[#0891b2] relative">
                  <div className="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#0891b2]"></div>
                  <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-[#0891b2]"></div>
                  <Bus className="w-4 h-4 text-[#0891b2] absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-white" />
                </div>
                <div className="text-xs text-gray-400 mt-1">Direct</div>
              </div>

              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">{reservation.trajet?.heure_arrivee}</div>
                <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                  <MapPin className="w-3 h-3" />
                  {reservation.trajet?.ville_arrivee?.nom}
                </div>
              </div>
            </div>

            {/* Info Grid */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-gray-50 rounded-xl p-4">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
                  <Calendar className="w-4 h-4 text-[#0891b2]" />
                  Date
                </div>
                <div className="font-semibold text-gray-900">{reservation.trajet?.date_trajet}</div>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
                  <Armchair className="w-4 h-4 text-[#0891b2]" />
                  Place
                </div>
                <div className="font-semibold text-gray-900">N° {reservation.place?.numero_place}</div>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
                  <User className="w-4 h-4 text-[#0891b2]" />
                  Passager
                </div>
                <div className="font-semibold text-gray-900">{reservation.client?.prenom} {reservation.client?.nom}</div>
                <div className="text-xs text-gray-400">CIN: {reservation.client?.cin}</div>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
                  <CreditCard className="w-4 h-4 text-[#0891b2]" />
                  Paiement
                </div>
                <div className="font-semibold text-gray-900">{reservation.paiement?.montant.toFixed(2)} MRU</div>
                <div className="text-xs text-gray-400 capitalize">{formatPaymentMode(reservation.paiement?.mode_paiement)}</div>
              </div>
            </div>

            {/* QR Code Area */}
            <div className="border-t border-dashed border-gray-300 pt-6">
              <div className="flex flex-col items-center">
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm mb-3">
                  {/* Simulated QR Code */}
                  <div className="w-40 h-40 relative">
                    <svg viewBox="0 0 160 160" className="w-full h-full">
                      <rect width="160" height="160" fill="white"/>
                      {/* QR pattern simulation */}
                      <rect x="10" y="10" width="40" height="40" fill="#0c4a6e" rx="4"/>
                      <rect x="16" y="16" width="28" height="28" fill="white" rx="2"/>
                      <rect x="22" y="22" width="16" height="16" fill="#0c4a6e" rx="1"/>
                      
                      <rect x="110" y="10" width="40" height="40" fill="#0c4a6e" rx="4"/>
                      <rect x="116" y="16" width="28" height="28" fill="white" rx="2"/>
                      <rect x="122" y="22" width="16" height="16" fill="#0c4a6e" rx="1"/>
                      
                      <rect x="10" y="110" width="40" height="40" fill="#0c4a6e" rx="4"/>
                      <rect x="16" y="116" width="28" height="28" fill="white" rx="2"/>
                      <rect x="22" y="122" width="16" height="16" fill="#0c4a6e" rx="1"/>
                      
                      {/* Data pattern */}
                      {Array.from({ length: 25 }).map((_, i) => {
                        const row = Math.floor(i / 5);
                        const col = i % 5;
                        const x = 60 + col * 12;
                        const y = 60 + row * 12;
                        if ((row + col) % 3 !== 0) {
                          return <rect key={i} x={x} y={y} width="8" height="8" fill="#0c4a6e" rx="1"/>;
                        }
                        return null;
                      })}
                      
                      {/* Bottom data */}
                      {Array.from({ length: 30 }).map((_, i) => {
                        const row = Math.floor(i / 10);
                        const col = i % 10;
                        const x = 60 + col * 10;
                        const y = 120 + row * 10;
                        if (Math.random() > 0.4) {
                          return <rect key={`b${i}`} x={x} y={y} width="6" height="6" fill="#0891b2" rx="1"/>;
                        }
                        return null;
                      })}
                    </svg>
                  </div>
                </div>
                <p className="text-xs text-gray-400 text-center">
                  Scannez ce QR code à l'embarquement
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Actions */}
        <div className="grid grid-cols-2 gap-3 mt-6">
          <Button
            variant="outline"
            className="h-12 rounded-xl border-gray-300 hover:bg-white"
            onClick={() => window.print()}
          >
            <Download className="w-4 h-4 mr-2" /> Télécharger
          </Button>
          <Button
            variant="outline"
            className="h-12 rounded-xl border-gray-300 hover:bg-white"
          >
            <Share2 className="w-4 h-4 mr-2" /> Partager
          </Button>
        </div>

        <Button
          onClick={onNewBooking}
          className="w-full mt-3 h-12 rounded-xl bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white font-medium shadow-lg shadow-[#0891b2]/20"
        >
          <Home className="w-4 h-4 mr-2" /> Nouvelle réservation
        </Button>
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

function formatPaymentMode(mode?: string): string {
  const modes: Record<string, string> = {
    'carte': 'Carte bancaire',
    'mobile_money': 'Mobile Money',
    'virement': 'Virement',
    'especes': 'Espèces',
  };
  return modes[mode || ''] || mode || '';
}
