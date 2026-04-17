import { Link } from 'react-router-dom'
import { IconBus, IconShield, IconUser } from '../components/Icons'

export function HomePage() {
  return (
    <div className="flex w-full flex-1 flex-col">
      <section className="relative flex min-h-[calc(100dvh-5.5rem)] flex-col justify-center border-b border-slate-200/80 bg-gradient-to-b from-white via-slate-50 to-slate-100/95 px-6 py-16 sm:min-h-[calc(100dvh-6rem)] sm:px-10 sm:py-24 lg:px-14 lg:py-28 xl:px-20 xl:py-32">
        <div className="mx-auto w-full max-w-[100rem]">
          <div className="grid items-center gap-16 lg:grid-cols-2 lg:gap-24 xl:gap-28">
            <div className="max-w-4xl">
              <p className="text-base font-semibold uppercase tracking-[0.2em] text-teal-700 sm:text-lg">
                Espace agences
              </p>
              <h1 className="mt-6 text-[clamp(2.25rem,5.5vw+0.75rem,5rem)] font-bold leading-[1.06] tracking-tight text-slate-900 xl:text-[clamp(3rem,4vw+1.5rem,5.5rem)]">
                Votre agence{' '}
                <span className="text-teal-700">en ligne</span>
              </h1>
              <p className="mt-10 text-xl leading-relaxed text-slate-600 sm:text-2xl lg:text-3xl lg:leading-relaxed">
                Compte, profil, logo : annuaire des agences de transport interurbain. Interface
                adaptée au téléphone et au bureau.
              </p>
              <div className="mt-12 flex flex-col gap-5 sm:flex-row sm:flex-wrap sm:gap-6 lg:mt-14">
                <Link
                  to="/inscription"
                  className="inline-flex min-h-[3.75rem] min-w-[14rem] items-center justify-center rounded-3xl bg-teal-600 px-12 py-5 text-xl font-semibold text-white shadow-xl shadow-teal-900/20 transition hover:bg-teal-700 sm:min-h-16 sm:px-14 sm:text-2xl"
                >
                  Créer un compte agence
                </Link>
                <Link
                  to="/agences"
                  className="inline-flex min-h-[3.75rem] min-w-[14rem] items-center justify-center rounded-3xl border-2 border-slate-300 bg-white px-12 py-5 text-xl font-semibold text-slate-800 shadow-md transition hover:border-slate-400 hover:bg-slate-50 sm:min-h-16 sm:px-14 sm:text-2xl"
                >
                  Consulter les agences
                </Link>
              </div>
            </div>

            <aside className="grid gap-6 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
              <div className="rounded-3xl border border-slate-200/80 bg-white p-10 shadow-2xl shadow-slate-900/8 sm:col-span-2 lg:col-span-1 xl:col-span-2 xl:grid xl:grid-cols-2 xl:gap-0 xl:divide-x xl:divide-slate-100 xl:p-0">
                <div className="bg-gradient-to-br from-teal-600 to-teal-800 p-10 text-white xl:rounded-l-3xl lg:p-12">
                  <IconBus className="mb-6 h-16 w-16 opacity-95" aria-hidden />
                  <p className="text-base font-medium uppercase tracking-wide opacity-90 sm:text-lg">
                    Réseau
                  </p>
                  <p className="mt-3 text-4xl font-bold tracking-tight sm:text-5xl">Interurbain</p>
                  <p className="mt-5 text-lg leading-relaxed opacity-95 sm:text-xl">
                    Fiche publique consultable par les usagers.
                  </p>
                </div>
                <div className="flex flex-col justify-center p-10 xl:rounded-r-3xl lg:p-12">
                  <IconShield className="mb-5 h-14 w-14 text-teal-600" aria-hidden />
                  <p className="text-2xl font-semibold text-slate-900 sm:text-3xl">Compte agence</p>
                  <p className="mt-3 text-lg leading-relaxed text-slate-600 sm:text-xl">
                    Connexion et rôles pour gérer la fiche.
                  </p>
                </div>
              </div>
              <div className="rounded-3xl border border-dashed border-teal-400/50 bg-teal-50/80 p-8 sm:col-span-2 lg:col-span-1 xl:col-span-2 lg:p-10">
                <IconUser className="mb-4 h-12 w-12 text-teal-700" aria-hidden />
                <p className="text-xl leading-relaxed text-slate-800 sm:text-2xl">
                  Texte lisible, contrastes corrects, navigation simple.
                </p>
              </div>
            </aside>
          </div>
        </div>
      </section>

      <section className="border-b border-slate-200 bg-white py-16 sm:py-20 lg:py-24">
        <div className="mx-auto grid max-w-[100rem] grid-cols-1 gap-12 px-6 sm:grid-cols-3 sm:gap-10 sm:px-10 lg:gap-14 lg:px-14">
          {[
            { k: 'Profil structuré', v: 'Coordonnées, ville, description' },
            { k: 'Logo & image', v: 'Mise en avant de votre marque' },
            { k: 'Visibilité', v: 'Annuaire des agences actives' },
          ].map((item) => (
            <div
              key={item.k}
              className="text-center sm:border-l sm:border-slate-200 sm:pl-10 sm:text-left first:sm:border-l-0 first:sm:pl-0"
            >
              <p className="text-3xl font-bold text-slate-900 sm:text-4xl lg:text-5xl">{item.k}</p>
              <p className="mt-3 text-lg text-slate-600 sm:text-xl lg:text-2xl">{item.v}</p>
            </div>
          ))}
        </div>
      </section>

      <section
        aria-labelledby="fonctionnalites"
        className="flex flex-1 flex-col bg-slate-100/90 py-20 sm:py-24 lg:py-32"
      >
        <div className="mx-auto flex w-full max-w-[100rem] flex-1 flex-col px-6 sm:px-10 lg:px-14">
          <h2
            id="fonctionnalites"
            className="text-center text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl lg:text-6xl xl:text-7xl"
          >
            Tout pour votre profil agence
          </h2>
          <p className="mx-auto mt-8 max-w-4xl text-center text-xl text-slate-600 sm:text-2xl lg:text-3xl">
            Inscription, profil et annuaire pour afficher votre activité.
          </p>
          <div className="mt-16 grid flex-1 grid-cols-1 gap-8 sm:mt-20 sm:grid-cols-2 sm:gap-10 lg:mt-24 lg:grid-cols-3 lg:gap-12">
            {[
              {
                title: 'Inscription & connexion',
                text: 'Formulaire d’inscription et page de connexion.',
              },
              {
                title: 'Profil & logo',
                text: 'Mise à jour du profil et dépôt de logo aux formats autorisés.',
              },
              {
                title: 'Annuaire public',
                text: 'Liste des agences actives, recherche par ville, fiche détaillée.',
              },
            ].map((f) => (
              <article
                key={f.title}
                className="flex flex-col rounded-3xl border border-slate-200/90 bg-white p-10 shadow-xl shadow-slate-900/[0.06] sm:p-12 lg:p-14"
              >
                <h3 className="text-2xl font-bold text-slate-900 sm:text-3xl lg:text-4xl">
                  {f.title}
                </h3>
                <p className="mt-6 flex-1 text-xl leading-relaxed text-slate-600 sm:text-2xl">
                  {f.text}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-teal-800 px-6 py-16 text-white sm:px-10 sm:py-20 lg:px-14 lg:py-24">
        <div className="mx-auto flex max-w-[100rem] flex-col items-start justify-between gap-10 lg:flex-row lg:items-center">
          <div>
            <h2 className="text-3xl font-bold sm:text-4xl lg:text-5xl xl:text-6xl">
              Prêt à publier votre agence ?
            </h2>
            <p className="mt-5 max-w-2xl text-xl text-teal-100 sm:text-2xl lg:text-3xl">
              Ouvrez un compte et renseignez les champs du profil.
            </p>
          </div>
          <Link
            to="/inscription"
            className="inline-flex min-h-[3.75rem] shrink-0 items-center justify-center rounded-3xl bg-white px-12 py-5 text-xl font-semibold text-teal-900 shadow-xl transition hover:bg-teal-50 sm:min-h-16 sm:px-14 sm:text-2xl"
          >
            Commencer
          </Link>
        </div>
      </section>
    </div>
  )
}
