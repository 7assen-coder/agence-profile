import { useState } from 'react';
import {
  Settings,
  Shield,
  Globe,
  CreditCard,
  Mail,
  Save,
  Check,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

export default function AdminParametres() {
  const [saved, setSaved] = useState(false);
  const [settings, setSettings] = useState({
    emailNotifications: true,
    smsNotifications: false,
    autoConfirm: false,
    maintenanceMode: false,
    allowOnlinePayment: true,
    allowCashPayment: true,
    cancelTimeout: 15,
  });

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Paramètres</h1>
        <p className="text-sm text-gray-500 mt-1">Configuration du système de réservation</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* General Settings */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Settings className="w-5 h-5 text-[#0891b2]" />
              Paramètres généraux
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">Notifications email</div>
                <div className="text-sm text-gray-500">Envoyer un email à chaque réservation</div>
              </div>
              <Switch
                checked={settings.emailNotifications}
                onCheckedChange={v => setSettings(prev => ({ ...prev, emailNotifications: v }))}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">Notifications SMS</div>
                <div className="text-sm text-gray-500">Envoyer un SMS de confirmation</div>
              </div>
              <Switch
                checked={settings.smsNotifications}
                onCheckedChange={v => setSettings(prev => ({ ...prev, smsNotifications: v }))}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">Confirmation automatique</div>
                <div className="text-sm text-gray-500">Confirmer les réservations sans validation manuelle</div>
              </div>
              <Switch
                checked={settings.autoConfirm}
                onCheckedChange={v => setSettings(prev => ({ ...prev, autoConfirm: v }))}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">Mode maintenance</div>
                <div className="text-sm text-gray-500">Désactiver temporairement les réservations</div>
              </div>
              <Switch
                checked={settings.maintenanceMode}
                onCheckedChange={v => setSettings(prev => ({ ...prev, maintenanceMode: v }))}
              />
            </div>
          </CardContent>
        </Card>

        {/* Payment Settings */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <CreditCard className="w-5 h-5 text-[#0891b2]" />
              Paiement
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">Paiement en ligne</div>
                <div className="text-sm text-gray-500">Carte bancaire et mobile money</div>
              </div>
              <Switch
                checked={settings.allowOnlinePayment}
                onCheckedChange={v => setSettings(prev => ({ ...prev, allowOnlinePayment: v }))}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">Paiement en espèces</div>
                <div className="text-sm text-gray-500">Paiement à l'agence ou au conducteur</div>
              </div>
              <Switch
                checked={settings.allowCashPayment}
                onCheckedChange={v => setSettings(prev => ({ ...prev, allowCashPayment: v }))}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="timeout" className="text-gray-700 font-medium">
                Délai d'annulation (minutes)
              </Label>
              <Input
                id="timeout"
                type="number"
                value={settings.cancelTimeout}
                onChange={e => setSettings(prev => ({ ...prev, cancelTimeout: parseInt(e.target.value) || 0 }))}
                className="w-32"
              />
              <p className="text-xs text-gray-500">Temps avant libération automatique des places non payées</p>
            </div>
          </CardContent>
        </Card>

        {/* Security */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Shield className="w-5 h-5 text-[#0891b2]" />
              Sécurité
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-3 bg-green-50 rounded-xl flex items-center gap-3">
              <Shield className="w-5 h-5 text-green-600" />
              <div>
                <div className="text-sm font-medium text-gray-900">Connexion sécurisée active</div>
                <div className="text-xs text-gray-500">SSL/TLS chiffrement activé</div>
              </div>
              <Check className="w-4 h-4 text-green-600 ml-auto" />
            </div>
            <div className="p-3 bg-gray-50 rounded-xl flex items-center gap-3">
              <Mail className="w-5 h-5 text-gray-600" />
              <div>
                <div className="text-sm font-medium text-gray-900">Vérification email requise</div>
                <div className="text-xs text-gray-500">Les clients doivent confirmer leur email</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* System Info */}
        <Card className="border border-gray-200 shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Globe className="w-5 h-5 text-[#0891b2]" />
              Informations système
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex justify-between text-sm py-2 border-b border-gray-100">
              <span className="text-gray-500">Version</span>
              <span className="font-medium text-gray-900">v1.0.0</span>
            </div>
            <div className="flex justify-between text-sm py-2 border-b border-gray-100">
              <span className="text-gray-500">Environnement</span>
              <span className="font-medium text-gray-900">Production</span>
            </div>
            <div className="flex justify-between text-sm py-2 border-b border-gray-100">
              <span className="text-gray-500">Base de données</span>
              <span className="font-medium text-gray-900">MySQL 8.0</span>
            </div>
            <div className="flex justify-between text-sm py-2 border-b border-gray-100">
              <span className="text-gray-500">Backend</span>
              <span className="font-medium text-gray-900">Flask + Python</span>
            </div>
            <div className="flex justify-between text-sm py-2">
              <span className="text-gray-500">Frontend</span>
              <span className="font-medium text-gray-900">React + TypeScript</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8 flex justify-end">
        <Button
          onClick={handleSave}
          className="bg-gradient-to-r from-[#0c4a6e] to-[#0891b2] hover:from-[#0a3d5c] hover:to-[#067a96] text-white rounded-xl h-11 px-6 font-medium shadow-lg shadow-[#0891b2]/20"
        >
          {saved ? (
            <span className="flex items-center gap-2">
              <Check className="w-4 h-4" /> Enregistré !
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <Save className="w-4 h-4" /> Enregistrer les modifications
            </span>
          )}
        </Button>
      </div>
    </div>
  );
}
