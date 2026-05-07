import { useState } from 'react';
import {
  agences,
  villes,
  bus,
  places,
  trajets,
  clients,
  paiements,
  reservations,
  getAgenceById,
  getVilleById,
  getBusById,
} from '@/data/mockData';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Building2,
  MapPin,
  Bus,
  Armchair,
  CalendarDays,
  Users,
  CreditCard,
  Ticket,
  ChevronDown,
  ChevronUp,
  Database,
} from 'lucide-react';

type TableKey = 'agences' | 'villes' | 'bus' | 'places' | 'trajets' | 'clients' | 'paiements' | 'reservations';

const TABLES: { key: TableKey; label: string; icon: React.ElementType; color: string; bg: string }[] = [
  { key: 'agences',      label: 'Agences',      icon: Building2,   color: 'text-[#0891b2]',  bg: 'bg-[#0891b2]/10' },
  { key: 'villes',       label: 'Villes',        icon: MapPin,       color: 'text-purple-600', bg: 'bg-purple-50' },
  { key: 'bus',          label: 'Bus',           icon: Bus,          color: 'text-amber-600',  bg: 'bg-amber-50' },
  { key: 'places',       label: 'Places',        icon: Armchair,     color: 'text-green-600',  bg: 'bg-green-50' },
  { key: 'trajets',      label: 'Trajets',       icon: CalendarDays, color: 'text-indigo-600', bg: 'bg-indigo-50' },
  { key: 'clients',      label: 'Clients',       icon: Users,        color: 'text-pink-600',   bg: 'bg-pink-50' },
  { key: 'paiements',    label: 'Paiements',     icon: CreditCard,   color: 'text-emerald-600',bg: 'bg-emerald-50' },
  { key: 'reservations', label: 'Réservations',  icon: Ticket,       color: 'text-red-600',    bg: 'bg-red-50' },
];

const COUNTS: Record<TableKey, number> = {
  agences: agences.length,
  villes: villes.length,
  bus: bus.length,
  places: places.length,
  trajets: trajets.length,
  clients: clients.length,
  paiements: paiements.length,
  reservations: reservations.length,
};

export default function AdminDatabase() {
  const [open, setOpen] = useState<Record<TableKey, boolean>>({
    agences: true,
    villes: false,
    bus: false,
    places: false,
    trajets: true,
    clients: false,
    paiements: false,
    reservations: true,
  });

  const toggle = (key: TableKey) =>
    setOpen(prev => ({ ...prev, [key]: !prev[key] }));

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-1">
          <div className="w-10 h-10 bg-[#0891b2]/10 rounded-xl flex items-center justify-center">
            <Database className="w-5 h-5 text-[#0891b2]" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Base de données</h1>
        </div>
        <p className="text-sm text-gray-500 ml-13">Toutes les tables et leurs données complètes</p>
      </div>

      {/* Summary row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3 mb-8">
        {TABLES.map(({ key, label, icon: Icon, color, bg }) => (
          <button
            key={key}
            onClick={() => toggle(key)}
            className="flex flex-col items-center gap-1 p-3 bg-white border border-gray-200 rounded-xl hover:shadow-md hover:border-[#0891b2]/30 transition-all group"
          >
            <div className={`w-9 h-9 ${bg} rounded-lg flex items-center justify-center`}>
              <Icon className={`w-4 h-4 ${color}`} />
            </div>
            <span className="text-lg font-bold text-gray-900">{COUNTS[key]}</span>
            <span className="text-[10px] text-gray-500 font-medium">{label}</span>
          </button>
        ))}
      </div>

      <div className="space-y-4">

        {/* ── Agences ── */}
        <TableCard table="agences" open={open.agences} onToggle={() => toggle('agences')} icon={Building2} color="text-[#0891b2]" bg="bg-[#0891b2]/10">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id_agence</Th><Th>nom</Th><Th>telephone</Th><Th>email</Th><Th>adresse</Th>
            </tr></thead>
            <tbody>
              {agences.map((a, i) => (
                <tr key={a.id_agence} className={rowClass(i)}>
                  <Td mono>{a.id_agence}</Td><Td bold>{a.nom}</Td><Td>{a.telephone}</Td>
                  <Td>{a.email}</Td><Td>{a.adresse}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        </TableCard>

        {/* ── Villes ── */}
        <TableCard table="villes" open={open.villes} onToggle={() => toggle('villes')} icon={MapPin} color="text-purple-600" bg="bg-purple-50">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id_ville</Th><Th>nom</Th><Th>region</Th>
            </tr></thead>
            <tbody>
              {villes.map((v, i) => (
                <tr key={v.id_ville} className={rowClass(i)}>
                  <Td mono>{v.id_ville}</Td><Td bold>{v.nom}</Td><Td>{v.region}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        </TableCard>

        {/* ── Bus ── */}
        <TableCard table="bus" open={open.bus} onToggle={() => toggle('bus')} icon={Bus} color="text-amber-600" bg="bg-amber-50">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id_bus</Th><Th>immatriculation</Th><Th>capacite</Th><Th>agence</Th>
            </tr></thead>
            <tbody>
              {bus.map((b, i) => (
                <tr key={b.id_bus} className={rowClass(i)}>
                  <Td mono>{b.id_bus}</Td><Td bold>{b.immatriculation}</Td>
                  <Td>{b.capacite} places</Td>
                  <Td>{getAgenceById(b.id_agence)?.nom ?? b.id_agence}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        </TableCard>

        {/* ── Places ── */}
        <TableCard table="places" open={open.places} onToggle={() => toggle('places')} icon={Armchair} color="text-green-600" bg="bg-green-50">
          <div className="overflow-x-auto max-h-72 overflow-y-auto">
            <table className="w-full text-sm">
              <thead className="sticky top-0 z-10"><tr className="border-b bg-gray-50/80">
                <Th>id_place</Th><Th>numero_place</Th><Th>bus</Th><Th>agence</Th>
              </tr></thead>
              <tbody>
                {places.map((p, i) => {
                  const b = bus.find(b => b.id_bus === p.id_bus);
                  return (
                    <tr key={p.id_place} className={rowClass(i)}>
                      <Td mono>{p.id_place}</Td><Td bold>N° {p.numero_place}</Td>
                      <Td>{b?.immatriculation}</Td>
                      <Td>{b ? getAgenceById(b.id_agence)?.nom : '—'}</Td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </TableCard>

        {/* ── Trajets ── */}
        <TableCard table="trajets" open={open.trajets} onToggle={() => toggle('trajets')} icon={CalendarDays} color="text-indigo-600" bg="bg-indigo-50">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id</Th><Th>date</Th><Th>période</Th><Th>départ</Th><Th>arrivée</Th>
              <Th>h. départ</Th><Th>h. arrivée</Th><Th>prix</Th><Th>agence</Th><Th>bus</Th>
            </tr></thead>
            <tbody>
              {trajets.map((t, i) => (
                <tr key={t.id_trajet} className={rowClass(i)}>
                  <Td mono>#{t.id_trajet}</Td>
                  <Td bold>{t.date_trajet}</Td>
                  <Td>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${t.periode === 'matin' ? 'bg-amber-100 text-amber-700' : 'bg-indigo-100 text-indigo-700'}`}>
                      {t.periode === 'matin' ? 'Matin' : 'Après-midi'}
                    </span>
                  </Td>
                  <Td>{getVilleById(t.id_ville_depart)?.nom}</Td>
                  <Td>{getVilleById(t.id_ville_arrivee)?.nom}</Td>
                  <Td>{t.heure_depart}</Td>
                  <Td>{t.heure_arrivee}</Td>
                  <Td bold>{t.prix} MRU</Td>
                  <Td>{getAgenceById(t.id_agence)?.nom}</Td>
                  <Td>{getBusById(t.id_bus)?.immatriculation}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        </TableCard>

        {/* ── Clients ── */}
        <TableCard table="clients" open={open.clients} onToggle={() => toggle('clients')} icon={Users} color="text-pink-600" bg="bg-pink-50">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id_client</Th><Th>nom complet</Th><Th>cin</Th><Th>telephone</Th><Th>email</Th>
            </tr></thead>
            <tbody>
              {clients.map((c, i) => (
                <tr key={c.id_client} className={rowClass(i)}>
                  <Td mono>{c.id_client}</Td>
                  <Td bold>{c.prenom} {c.nom}</Td>
                  <Td>{c.cin}</Td><Td>{c.telephone}</Td><Td>{c.email}</Td>
                </tr>
              ))}
            </tbody>
          </table>
        </TableCard>

        {/* ── Paiements ── */}
        <TableCard table="paiements" open={open.paiements} onToggle={() => toggle('paiements')} icon={CreditCard} color="text-emerald-600" bg="bg-emerald-50">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id_paiement</Th><Th>client</Th><Th>montant</Th><Th>mode</Th><Th>statut</Th><Th>date</Th>
            </tr></thead>
            <tbody>
              {paiements.map((p, i) => {
                const client = clients.find(c => c.id_client === p.id_client);
                return (
                  <tr key={p.id_paiement} className={rowClass(i)}>
                    <Td mono>{p.id_paiement}</Td>
                    <Td bold>{client ? `${client.prenom} ${client.nom}` : p.id_client}</Td>
                    <Td bold>{p.montant.toFixed(2)} MRU</Td>
                    <Td>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${modeColor(p.mode_paiement)}`}>
                        {modeLabel(p.mode_paiement)}
                      </span>
                    </Td>
                    <Td>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statutPaiementColor(p.statut)}`}>
                        {p.statut}
                      </span>
                    </Td>
                    <Td>{new Date(p.date_paiement).toLocaleDateString('fr-FR')}</Td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </TableCard>

        {/* ── Réservations ── */}
        <TableCard table="reservations" open={open.reservations} onToggle={() => toggle('reservations')} icon={Ticket} color="text-red-600" bg="bg-red-50">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50/80">
              <Th>id</Th><Th>client</Th><Th>trajet</Th><Th>date trajet</Th>
              <Th>place</Th><Th>paiement</Th><Th>statut</Th><Th>date résa.</Th>
            </tr></thead>
            <tbody>
              {reservations.map((r, i) => {
                const client = clients.find(c => c.id_client === r.id_client);
                const trajet = trajets.find(t => t.id_trajet === r.id_trajet);
                const paiement = paiements.find(p => p.id_paiement === r.id_paiement);
                const place = places.find(p => p.id_place === r.id_place);
                return (
                  <tr key={r.id_reservation} className={rowClass(i)}>
                    <Td mono>#{r.id_reservation}</Td>
                    <Td bold>{client ? `${client.prenom} ${client.nom}` : '—'}</Td>
                    <Td>
                      {trajet
                        ? `${getVilleById(trajet.id_ville_depart)?.nom} → ${getVilleById(trajet.id_ville_arrivee)?.nom}`
                        : '—'}
                    </Td>
                    <Td>{trajet?.date_trajet ?? '—'}</Td>
                    <Td>N° {place?.numero_place ?? '—'}</Td>
                    <Td>{paiement ? `${paiement.montant} MRU` : <span className="text-gray-400 text-xs">Non payé</span>}</Td>
                    <Td>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statutReservationColor(r.statut)}`}>
                        {statutReservationLabel(r.statut)}
                      </span>
                    </Td>
                    <Td>{new Date(r.date_reservation).toLocaleDateString('fr-FR')}</Td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </TableCard>

      </div>
    </div>
  );
}

// ── Sub-components ───────────────────────────────────────────

function TableCard({
  table, open, onToggle, icon: Icon, color, bg, children,
}: {
  table: TableKey; open: boolean; onToggle: () => void;
  icon: React.ElementType; color: string; bg: string; children: React.ReactNode;
}) {
  const label = TABLES.find(t => t.key === table)!.label;
  const count = COUNTS[table];
  return (
    <Card className="border border-gray-200 shadow-sm overflow-hidden">
      <CardHeader className="pb-0 pt-0 px-0">
        <button
          onClick={onToggle}
          className="flex items-center justify-between w-full px-5 py-4 hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className={`w-9 h-9 ${bg} rounded-lg flex items-center justify-center`}>
              <Icon className={`w-4 h-4 ${color}`} />
            </div>
            <CardTitle className="text-base font-semibold text-gray-900">{label}</CardTitle>
            <span className="text-xs bg-gray-100 text-gray-500 font-mono px-2 py-0.5 rounded-full">{count} lignes</span>
          </div>
          {open
            ? <ChevronUp className="w-4 h-4 text-gray-400" />
            : <ChevronDown className="w-4 h-4 text-gray-400" />}
        </button>
      </CardHeader>
      {open && (
        <CardContent className="p-0 border-t border-gray-100 overflow-x-auto">
          {children}
        </CardContent>
      )}
    </Card>
  );
}

const Th = ({ children }: { children: React.ReactNode }) => (
  <th className="text-left px-4 py-2.5 text-xs font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap">{children}</th>
);

const Td = ({ children, mono, bold }: { children: React.ReactNode; mono?: boolean; bold?: boolean }) => (
  <td className={`px-4 py-3 text-sm whitespace-nowrap ${mono ? 'font-mono text-gray-400' : ''} ${bold ? 'font-semibold text-gray-900' : 'text-gray-600'}`}>
    {children}
  </td>
);

const rowClass = (i: number) => `border-b border-gray-50 ${i % 2 === 0 ? 'bg-white' : 'bg-gray-50/40'} hover:bg-blue-50/30 transition-colors`;

const modeLabel = (m: string) => ({ carte: 'Carte', mobile_money: 'Mobile Money', virement: 'Virement', especes: 'Espèces' }[m] ?? m);
const modeColor = (m: string) => ({ carte: 'bg-blue-100 text-blue-700', mobile_money: 'bg-green-100 text-green-700', virement: 'bg-purple-100 text-purple-700', especes: 'bg-amber-100 text-amber-700' }[m] ?? 'bg-gray-100 text-gray-700');
const statutPaiementColor = (s: string) => ({ confirme: 'bg-green-100 text-green-700', en_attente: 'bg-amber-100 text-amber-700', echoue: 'bg-red-100 text-red-700', rembourse: 'bg-purple-100 text-purple-700' }[s] ?? 'bg-gray-100 text-gray-700');
const statutReservationLabel = (s: string) => ({ confirmee: 'Confirmée', en_attente: 'En attente', annulee: 'Annulée' }[s] ?? s);
const statutReservationColor = (s: string) => ({ confirmee: 'bg-green-100 text-green-700', en_attente: 'bg-amber-100 text-amber-700', annulee: 'bg-red-100 text-red-700' }[s] ?? 'bg-gray-100 text-gray-700');
