import { Link } from 'react-router-dom'
import { GlassPanel } from '../components/ui/GlassPanel'
import { Button } from '../components/ui/Button'

export function Home() {
  return (
    <div className="w-full px-6 py-14 sm:px-10 sm:py-16 lg:px-14">
      <div className="mx-auto w-full max-w-4xl">
        <GlassPanel>
          <h1 className="text-4xl font-bold text-slate-900">Trajets SaaS</h1>
          <p className="mt-4 text-lg text-slate-600">
            Plateforme de réservation de transport interurbain
          </p>
          
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="rounded-lg bg-slate-50 p-6">
              <h2 className="font-semibold text-slate-900">Pour les agences</h2>
              <p className="mt-2 text-sm text-slate-600">
                Gérez vos trajets et votre profil d'agence
              </p>
              <div className="mt-4 flex gap-2">
                <Link to="/connexion">
                  <Button>Se connecter</Button>
                </Link>
                <Link to="/inscription">
                  <Button variant="outline">S'inscrire</Button>
                </Link>
              </div>
            </div>
            
            <div className="rounded-lg bg-slate-50 p-6">
              <h2 className="font-semibold text-slate-900">Découvrir les trajets</h2>
              <p className="mt-2 text-sm text-slate-600">
                Consultez les agences et leurs trajets disponibles
              </p>
              <div className="mt-4">
                <Link to="/agences">
                  <Button>Voir les agences</Button>
                </Link>
              </div>
            </div>
          </div>
        </GlassPanel>
      </div>
    </div>
  )
}
