import { useState } from 'react';
import { ArrowLeft, CreditCard, User, Phone, Mail, FileText, Check, Shield, MapPin, Armchair, Banknote } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { createClient, createPaiement, createReservation, confirmerReservation } from '@/services/api';
import type { TrajetComplet, Place, Paiement, Reservation } from '@/types';

interface PaymentSectionProps {
  trajet: TrajetComplet;
  place: Place;
  onComplete: (reservation: Reservation) => void;
  onBack: () => void;
}

export default function PaymentSection({ trajet, place, onComplete, onBack }: PaymentSectionProps) {
  const [step, setStep] = useState<'client' | 'payment' | 'processing'>('client');
  const [clientData, setClientData] = useState({
    nom: '',
    prenom: '',
    telephone: '',
    email: '',
    cin: '',
  });
  const [paymentMode, setPaymentMode] = useState<Paiement['mode_paiement']>('carte');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateClient = () => {
    const newErrors: Record<string, string> = {};
    if (!clientData.nom.trim()) newErrors.nom = 'Le nom est requis';
    if (!clientData.prenom.trim()) newErrors.prenom = 'Le prénom est requis';
    if (!clientData.telephone.trim()) newErrors.telephone = 'Le téléphone est requis';
    if (!clientData.cin.trim()) newErrors.cin = 'Le CIN est requis';
    if (clientData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clientData.email)) {
      newErrors.email = 'Email invalide';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleContinueToPayment = () => {
    if (validateClient()) {
      setStep('payment');
    }
  };

  const handlePayment = async () => {
    setIsSubmitting(true);
    setStep('processing');

    try {
      // 1. Créer le client
      const newClient = await createClient({
        nom: clientData.nom,
        prenom: clientData.prenom,
        telephone: clientData.telephone,
        email: clientData.email,
        cin: clientData.cin,
      });

      // 2. Créer le paiement
      const newPaiement = await createPaiement({
        id_client: newClient.id_client,
        montant: trajet.prix,
        mode_paiement: paymentMode,
        statut: 'confirme',
      });

      // 3. Créer la réservation
      const newReservation = await createReservation({
        id_client: newClient.id_client,
        id_place: place.id_place,
        id_trajet: trajet.id_trajet,
      });

      // 4. Confirmer la réservation
      const confirmed = await confirmerReservation(newReservation.id_reservation, newPaiement.id_paiement.toString());

      if (confirmed) {
        onComplete(confirmed);
      }
    } catch (error) {
      console.error('Payment error:', error);
      setIsSubmitting(false);
    }
  };

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
            <ArrowLeft className="w-4 h-4 mr-2" /> Retour à la sélection
          </Button>
          
          <h1 className="text-xl font-bold">Finaliser la réservation</h1>
          <div className="flex items-center gap-2 text-cyan-100/80 text-sm mt-1">
            <MapPin className="w-4 h-4" />
            {trajet.ville_depart?.nom} → {trajet.ville_arrivee?.nom}
            <span className="mx-1">|</span>
            Place N° {place.numero_place}
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center gap-4">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium ${
              step === 'client' ? 'bg-[#0891b2] text-white' : 'bg-[#0891b2]/10 text-[#0891b2]'
            }`}>
              <User className="w-4 h-4" /> Informations
            </div>
            <div className="w-8 h-0.5 bg-gray-200"></div>
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium ${
              step === 'payment' ? 'bg-[#0891b2] text-white' : step === 'client' ? 'bg-gray-100 text-gray-400' : 'bg-[#0891b2]/10 text-[#0891b2]'
            }`}>
              <CreditCard className="w-4 h-4" /> Paiement
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Form */}
          <div className="lg:col-span-2">
            {step === 'client' && (
              <Card className="border border-gray-200 shadow-lg">
                <CardContent className="p-6">
                  <h2 className="text-lg font-semibold text-gray-800 mb-6 flex items-center gap-2">
                    <User className="w-5 h-5 text-[#0891b2]" />
                    Informations du voyageur
                  </h2>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="nom" className="text-gray-700">Nom *</Label>
                      <Input
                        id="nom"
                        value={clientData.nom}
                        onChange={e => setClientData(prev => ({ ...prev, nom: e.target.value }))}
                        placeholder="Ex: Benali"
                        className={errors.nom ? 'border-red-400' : ''}
                      />
                      {errors.nom && <p className="text-xs text-red-500">{errors.nom}</p>}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="prenom" className="text-gray-700">Prénom *</Label>
                      <Input
                        id="prenom"
                        value={clientData.prenom}
                        onChange={e => setClientData(prev => ({ ...prev, prenom: e.target.value }))}
                        placeholder="Ex: Youssef"
                        className={errors.prenom ? 'border-red-400' : ''}
                      />
                      {errors.prenom && <p className="text-xs text-red-500">{errors.prenom}</p>}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="cin" className="text-gray-700">CIN *</Label>
                      <div className="relative">
                        <FileText className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                        <Input
                          id="cin"
                          value={clientData.cin}
                          onChange={e => setClientData(prev => ({ ...prev, cin: e.target.value.toUpperCase() }))}
                          placeholder="Ex: AB123456"
                          className={`pl-10 ${errors.cin ? 'border-red-400' : ''}`}
                        />
                      </div>
                      {errors.cin && <p className="text-xs text-red-500">{errors.cin}</p>}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="telephone" className="text-gray-700">Téléphone *</Label>
                      <div className="relative">
                        <Phone className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                        <Input
                          id="telephone"
                          value={clientData.telephone}
                          onChange={e => setClientData(prev => ({ ...prev, telephone: e.target.value }))}
                          placeholder="Ex: +212 612 345 678"
                          className={`pl-10 ${errors.telephone ? 'border-red-400' : ''}`}
                        />
                      </div>
                      {errors.telephone && <p className="text-xs text-red-500">{errors.telephone}</p>}
                    </div>

                    <div className="space-y-2 md:col-span-2">
                      <Label htmlFor="email" className="text-gray-700">Email</Label>
                      <div className="relative">
                        <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                        <Input
                          id="email"
                          type="email"
                          value={clientData.email}
                          onChange={e => setClientData(prev => ({ ...prev, email: e.target.value }))}
                          placeholder="Ex: vous@email.ma"
                          className={`pl-10 ${errors.email ? 'border-red-400' : ''}`}
                        />
                      </div>
                      {errors.email && <p className="text-xs text-red-500">{errors.email}</p>}
                    </div>
                  </div>

                  <div className="mt-8 flex justify-end">
                    <Button
                      onClick={handleContinueToPayment}
                      className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white rounded-xl h-11 px-6 font-medium shadow-lg shadow-[#0891b2]/20"
                    >
                      Continuer <ArrowLeft className="w-4 h-4 ml-2 rotate-180" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {step === 'payment' && (
              <Card className="border border-gray-200 shadow-lg">
                <CardContent className="p-6">
                  <h2 className="text-lg font-semibold text-gray-800 mb-6 flex items-center gap-2">
                    <CreditCard className="w-5 h-5 text-[#0891b2]" />
                    Mode de paiement
                  </h2>

                  <RadioGroup
                    value={paymentMode}
                    onValueChange={(v) => setPaymentMode(v as Paiement['mode_paiement'])}
                    className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6"
                  >
                    <div>
                      <RadioGroupItem value="carte" id="carte" className="peer sr-only" />
                      <Label
                        htmlFor="carte"
                        className="flex items-center gap-3 p-4 rounded-xl border-2 border-gray-200 cursor-pointer transition-all peer-data-[state=checked]:border-[#0891b2] peer-data-[state=checked]:bg-[#0891b2]/5 hover:border-gray-300"
                      >
                        <CreditCard className="w-5 h-5 text-[#0891b2]" />
                        <div>
                          <div className="font-medium text-gray-900">Carte bancaire</div>
                          <div className="text-xs text-gray-500">Paiement sécurisé</div>
                        </div>
                      </Label>
                    </div>

                    <div>
                      <RadioGroupItem value="mobile_money" id="mobile_money" className="peer sr-only" />
                      <Label
                        htmlFor="mobile_money"
                        className="flex items-center gap-3 p-4 rounded-xl border-2 border-gray-200 cursor-pointer transition-all peer-data-[state=checked]:border-[#0891b2] peer-data-[state=checked]:bg-[#0891b2]/5 hover:border-gray-300"
                      >
                        <Phone className="w-5 h-5 text-[#0891b2]" />
                        <div>
                          <div className="font-medium text-gray-900">Mobile Money</div>
                          <div className="text-xs text-gray-500">Inwi Money, Orange Cash</div>
                        </div>
                      </Label>
                    </div>

                    <div>
                      <RadioGroupItem value="virement" id="virement" className="peer sr-only" />
                      <Label
                        htmlFor="virement"
                        className="flex items-center gap-3 p-4 rounded-xl border-2 border-gray-200 cursor-pointer transition-all peer-data-[state=checked]:border-[#0891b2] peer-data-[state=checked]:bg-[#0891b2]/5 hover:border-gray-300"
                      >
                        <Banknote className="w-5 h-5 text-[#0891b2]" />
                        <div>
                          <div className="font-medium text-gray-900">Virement bancaire</div>
                          <div className="text-xs text-gray-500">Compte bancaire</div>
                        </div>
                      </Label>
                    </div>

                    <div>
                      <RadioGroupItem value="especes" id="especes" className="peer sr-only" />
                      <Label
                        htmlFor="especes"
                        className="flex items-center gap-3 p-4 rounded-xl border-2 border-gray-200 cursor-pointer transition-all peer-data-[state=checked]:border-[#0891b2] peer-data-[state=checked]:bg-[#0891b2]/5 hover:border-gray-300"
                      >
                        <Banknote className="w-5 h-5 text-[#0891b2]" />
                        <div>
                          <div className="font-medium text-gray-900">Espèces</div>
                          <div className="text-xs text-gray-500">Paiement à l'agence</div>
                        </div>
                      </Label>
                    </div>
                  </RadioGroup>

                  <div className="bg-gray-50 rounded-xl p-4 mb-6">
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Shield className="w-4 h-4 text-green-600" />
                      Vos données sont chiffrées et sécurisées conformément aux standards PCI DSS.
                    </div>
                  </div>

                  <div className="flex justify-between">
                    <Button
                      variant="outline"
                      onClick={() => setStep('client')}
                      className="rounded-xl h-11 px-6"
                    >
                      <ArrowLeft className="w-4 h-4 mr-2" /> Retour
                    </Button>
                    <Button
                      onClick={handlePayment}
                      disabled={isSubmitting}
                      className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white rounded-xl h-11 px-8 font-medium shadow-lg shadow-[#0891b2]/20"
                    >
                      {isSubmitting ? (
                        <span className="flex items-center gap-2">
                          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                          Traitement...
                        </span>
                      ) : (
                        <span className="flex items-center gap-2">
                          Payer {trajet.prix.toFixed(2)} MRU <Check className="w-4 h-4" />
                        </span>
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {step === 'processing' && (
              <Card className="border border-gray-200 shadow-lg">
                <CardContent className="p-12 text-center">
                  <div className="w-16 h-16 bg-[#0891b2]/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <div className="w-8 h-8 border-2 border-[#0891b2]/30 border-t-[#0891b2] rounded-full animate-spin"></div>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-800 mb-2">Traitement de votre paiement...</h3>
                  <p className="text-gray-500">Veuillez patienter pendant que nous confirmons votre réservation.</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar Summary */}
          <div className="lg:col-span-1">
            <Card className="border border-gray-200 shadow-lg sticky top-6">
              <CardContent className="p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Résumé de la réservation</h3>
                
                <div className="space-y-3 text-sm mb-6">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Trajet</span>
                    <span className="font-medium text-gray-900 text-right">{trajet.ville_depart?.nom} → {trajet.ville_arrivee?.nom}</span>
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
                    <span className="text-gray-500">Agence</span>
                    <span className="font-medium text-gray-900">{trajet.agence?.nom}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Bus</span>
                    <span className="font-medium text-gray-900">{trajet.bus?.immatriculation}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-500">Place</span>
                    <span className="flex items-center gap-1 font-medium text-[#0891b2]">
                      <Armchair className="w-4 h-4" /> N° {place.numero_place}
                    </span>
                  </div>
                </div>

                <div className="border-t border-gray-100 pt-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-600">Prix du billet</span>
                    <span className="font-medium">{trajet.prix.toFixed(2)} MRU</span>
                  </div>
                  <div className="flex justify-between items-center text-sm text-gray-500 mb-3">
                    <span>Frais de service</span>
                    <span>0.00 MRU</span>
                  </div>
                  <div className="flex justify-between items-center pt-3 border-t border-gray-100">
                    <span className="text-gray-800 font-semibold">Total à payer</span>
                    <span className="text-2xl font-bold text-[#0c4a6e]">{trajet.prix.toFixed(2)} MRU</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
