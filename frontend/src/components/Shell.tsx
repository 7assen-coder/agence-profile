import { Link, NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Button } from './ui/Button'
import { IconBus } from './Icons'

const navClass = ({ isActive }: { isActive: boolean }) =>
  `rounded-xl px-4 py-3 text-lg font-medium transition duration-200 sm:px-5 sm:py-3 ${
    isActive
      ? 'bg-teal-600/10 text-teal-800'
      : 'text-slate-600 hover:bg-white/60 hover:text-slate-900'
  }`

export function Shell() {
  const { agence, logout, loading } = useAuth()

  return (
    <div className="flex min-h-dvh w-full flex-col bg-slate-100">
      <header className="sticky top-0 z-40 shrink-0 border-b border-slate-200/90 bg-white shadow-sm">
        <div className="mx-auto flex w-full max-w-[100rem] items-center justify-between gap-4 px-6 py-5 sm:px-10 sm:py-6 lg:px-14">
          <Link
            to="/"
            className="flex cursor-pointer items-center gap-4 font-semibold text-slate-900 transition hover:text-teal-800"
          >
            <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-teal-600 text-white shadow-md sm:h-16 sm:w-16">
              <IconBus className="h-8 w-8 sm:h-9 sm:w-9" />
            </span>
            <span className="text-xl font-bold tracking-tight sm:text-2xl lg:text-3xl">
              Trajets SaaS
            </span>
          </Link>

          <nav className="flex flex-1 items-center justify-end gap-2 sm:gap-3" aria-label="Principal">
            <NavLink to="/agences" className={navClass}>
              Agences
            </NavLink>
            {loading ? (
              <span className="px-5 py-3 text-lg text-slate-500">…</span>
            ) : agence ? (
              <>
                <NavLink to="/compte" className={navClass}>
                  Mon compte
                </NavLink>
                <Button
                  type="button"
                  variant="secondary"
                  className="!px-5 !py-3 !text-base sm:!text-lg"
                  onClick={() => logout()}
                >
                  Déconnexion
                </Button>
              </>
            ) : (
              <>
                <NavLink to="/connexion" className={navClass}>
                  Connexion
                </NavLink>
                <Link
                  to="/inscription"
                  className="inline-flex cursor-pointer items-center justify-center rounded-2xl border border-teal-700/20 bg-teal-600 px-6 py-3 text-base font-semibold text-white shadow-md transition-all duration-200 hover:bg-teal-700 sm:px-8 sm:py-3.5 sm:text-lg"
                >
                  Inscription
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      <main className="flex min-h-0 flex-1 flex-col">
        <Outlet />
      </main>

      <footer className="shrink-0 border-t border-slate-200 bg-slate-900 text-slate-400">
        <div className="mx-auto flex w-full max-w-[100rem] flex-col gap-8 px-6 py-14 sm:flex-row sm:items-center sm:justify-between sm:px-10 sm:py-16 lg:px-14">
          <div className="flex items-center gap-4">
            <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-teal-600/20 text-teal-400">
              <IconBus className="h-7 w-7" />
            </span>
            <div>
              <p className="text-lg font-semibold text-white sm:text-xl">Trajets SaaS</p>
              <p className="text-base sm:text-lg">Fiches agences, transport interurbain</p>
            </div>
          </div>
          <p className="text-base sm:text-right sm:text-lg">
            © {new Date().getFullYear()} Trajets SaaS
          </p>
        </div>
      </footer>
    </div>
  )
}
