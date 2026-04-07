import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#FAFCFF]">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-blue-100/50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-400 rounded-lg flex items-center justify-center text-white font-extrabold text-sm shadow-md">P</div>
            <span className="text-lg font-extrabold text-gray-900 tracking-tight">Pilot<span className="text-blue-600">BI</span></span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#solution" className="text-sm font-medium text-gray-500 hover:text-blue-600 transition-colors">Solution</a>
            <a href="#features" className="text-sm font-medium text-gray-500 hover:text-blue-600 transition-colors">Fonctions</a>
            <a href="#pricing" className="text-sm font-medium text-gray-500 hover:text-blue-600 transition-colors">Tarifs</a>
            <Link href="/connexion" className="px-5 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition-all shadow-md shadow-blue-600/20">
              Essai gratuit
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-gradient-radial from-blue-100/40 to-transparent rounded-full -translate-y-1/2 translate-x-1/4" />
        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center relative z-10">
          <div>
            <div className="inline-flex items-center gap-2 bg-white border border-blue-200 rounded-full px-4 py-1.5 text-sm text-gray-600 shadow-sm mb-6">
              Lancement 2026 <span className="bg-blue-600 text-white text-[10px] font-bold px-2.5 py-0.5 rounded-full">NOUVEAU</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-black text-gray-900 tracking-tight leading-[1.08] mb-5">
              Pilotez votre PME avec vos <span className="bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">vrais chiffres</span>.
            </h1>
            <p className="text-lg text-gray-500 leading-relaxed mb-8 max-w-lg">
              PilotBI transforme vos fichiers Excel et ERP en tableaux de bord intelligents avec des rapports IA en fran&ccedil;ais. Con&ccedil;u pour les PMEs marocaines.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 mb-10">
              <Link href="/inscription" className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl text-base font-bold shadow-lg shadow-blue-600/25 hover:-translate-y-0.5 transition-all text-center">
                D&eacute;marrer l&apos;essai gratuit &rarr;
              </Link>
              <a href="#solution" className="px-8 py-4 bg-white border border-gray-200 text-gray-800 rounded-xl text-base font-semibold hover:border-blue-300 hover:bg-blue-50 transition-all text-center">
                D&eacute;couvrir la solution
              </a>
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-500">
              <div className="flex -space-x-2.5">
                <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold border-2 border-white">MK</div>
                <div className="w-8 h-8 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-xs font-bold border-2 border-white">YB</div>
                <div className="w-8 h-8 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center text-xs font-bold border-2 border-white">SA</div>
              </div>
              <span><strong className="text-gray-900">14 jours gratuits</strong> &middot; Sans carte bancaire</span>
            </div>
          </div>

          {/* Dashboard mockup */}
          <div className="bg-white rounded-2xl shadow-2xl border border-blue-50 overflow-hidden">
            <div className="h-10 bg-gradient-to-r from-gray-900 to-gray-800 flex items-center px-4 gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-red-400" />
              <div className="w-2.5 h-2.5 rounded-full bg-amber-400" />
              <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
              <span className="text-white/50 text-xs ml-2">PilotBI — Tableau de bord</span>
            </div>
            <div className="p-5 grid grid-cols-2 gap-3">
              <div className="bg-blue-50/50 rounded-xl p-4 border border-blue-100/50">
                <div className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Chiffre d&apos;affaires</div>
                <div className="text-2xl font-extrabold text-gray-900">2.4M</div>
                <div className="text-xs font-semibold text-green-600 mt-1">&#9650; +12.5%</div>
              </div>
              <div className="bg-blue-50/50 rounded-xl p-4 border border-blue-100/50">
                <div className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Marge nette</div>
                <div className="text-2xl font-extrabold text-gray-900">18.3%</div>
                <div className="text-xs font-semibold text-green-600 mt-1">&#9650; +2.1 pts</div>
              </div>
              <div className="bg-blue-50/50 rounded-xl p-4 border border-blue-100/50">
                <div className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Clients actifs</div>
                <div className="text-2xl font-extrabold text-gray-900">347</div>
                <div className="text-xs font-semibold text-green-600 mt-1">&#9650; +28</div>
              </div>
              <div className="bg-blue-50/50 rounded-xl p-4 border border-blue-100/50">
                <div className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">Stock critique</div>
                <div className="text-2xl font-extrabold text-red-500">12</div>
                <div className="text-xs font-semibold text-red-500 mt-1">&#9660; Alerte</div>
              </div>
              <div className="col-span-2 bg-blue-50/50 rounded-xl p-4 border border-blue-100/50">
                <div className="text-xs font-semibold text-gray-500 mb-3">Ventes mensuelles — 2026</div>
                <div className="flex items-end gap-1.5 h-16">
                  {[45,52,48,65,58,72,68,80,75,88,82,95].map((h, i) => (
                    <div key={i} className="flex-1 bg-gradient-to-t from-blue-600 to-blue-300 rounded-t" style={{height: `${h}%`}} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="solution" className="py-20 px-6 bg-blue-50/40">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-blue-600 bg-blue-50 border border-blue-200 rounded-full px-4 py-1.5 mb-5">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" /> Comment &ccedil;a marche
          </div>
          <h2 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-4">5 &eacute;tapes simples</h2>
          <p className="text-gray-500 max-w-xl mx-auto mb-14">Aucune comp&eacute;tence technique. Connectez vos donn&eacute;es, laissez PilotBI faire le reste.</p>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              {n:"1", icon:"🔗", title:"Connexion", desc:"Excel, Sheets, Odoo, Sage"},
              {n:"2", icon:"⚙️", title:"Configuration", desc:"5 questions sur votre activité"},
              {n:"3", icon:"📊", title:"Dashboard", desc:"Tableau de bord en 48h"},
              {n:"4", icon:"🤖", title:"Rapport IA", desc:"Narratif mensuel + 3 actions"},
              {n:"5", icon:"🔔", title:"Alertes", desc:"WhatsApp et email"},
            ].map((s) => (
              <div key={s.n} className="bg-white rounded-2xl p-6 border border-blue-50 hover:-translate-y-1 hover:shadow-lg transition-all text-center">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-400 text-white rounded-xl flex items-center justify-center text-sm font-extrabold mx-auto mb-3 shadow-md shadow-blue-600/20">{s.n}</div>
                <div className="text-2xl mb-2">{s.icon}</div>
                <h4 className="font-bold text-gray-900 text-sm mb-1">{s.title}</h4>
                <p className="text-xs text-gray-500">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-blue-600 bg-blue-50 border border-blue-200 rounded-full px-4 py-1.5 mb-5">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" /> Fonctionnalit&eacute;s
          </div>
          <h2 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-12">Tout pour piloter votre entreprise</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="md:row-span-2 bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-8 text-left text-white">
              <div className="w-12 h-12 bg-white/15 rounded-xl flex items-center justify-center text-2xl mb-5">🤖</div>
              <h4 className="text-lg font-bold mb-2">Rapports IA en fran&ccedil;ais</h4>
              <p className="text-white/80 text-sm leading-relaxed mb-6">Chaque mois, un rapport narratif qui analyse vos chiffres et recommande 3 actions prioritaires.</p>
              <div className="bg-white/10 rounded-xl p-4 text-sm text-white/90 leading-relaxed">
                <div className="text-[10px] uppercase tracking-wider text-white/50 mb-2">Extrait rapport</div>
                &laquo; Votre marge sur la cat&eacute;gorie &eacute;lectronique a baiss&eacute; de 4.2 pts. Recommandation : ren&eacute;gocier le fournisseur X... &raquo;
              </div>
            </div>
            {[
              {icon:"📊", title:"Dashboard interactif", desc:"Ventes, marges, clients, stocks — visualisés en temps réel."},
              {icon:"🔔", title:"Alertes intelligentes", desc:"Stock critique, baisse de marge — alertes WhatsApp et email."},
              {icon:"🔗", title:"Connexion automatique", desc:"Excel, Google Sheets, Odoo, Sage — en quelques clics."},
              {icon:"🇲🇦", title:"100% adapté au Maroc", desc:"Interface FR/AR, KPIs locaux, support réactif, prix en MAD."},
            ].map((f) => (
              <div key={f.title} className="bg-white rounded-2xl p-6 text-left border border-blue-50 hover:-translate-y-1 hover:shadow-lg transition-all">
                <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center text-2xl mb-4">{f.icon}</div>
                <h4 className="font-bold text-gray-900 mb-1">{f.title}</h4>
                <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 px-6 bg-blue-50/40">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-blue-600 bg-blue-50 border border-blue-200 rounded-full px-4 py-1.5 mb-5">
            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full" /> Tarification
          </div>
          <h2 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-4">Simple, transparent</h2>
          <p className="text-gray-500 mb-14">Moins qu&apos;une journ&eacute;e de consultant. Essai gratuit 14 jours.</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 max-w-4xl mx-auto items-start">
            {/* Starter */}
            <div className="bg-white rounded-2xl p-8 border border-gray-100 hover:-translate-y-1 hover:shadow-lg transition-all">
              <div className="text-xs font-bold uppercase tracking-widest text-blue-600 mb-2">Starter</div>
              <div className="text-5xl font-black text-gray-900 tracking-tight">990</div>
              <div className="text-sm text-gray-500 mb-5">MAD / mois</div>
              <div className="text-xs text-gray-400 border-b border-gray-100 pb-5 mb-5">PME 10–30 salari&eacute;s</div>
              <ul className="space-y-3 text-sm text-gray-600 text-left mb-6">
                <li className="flex gap-2"><span className="text-green-500">✓</span> 1 source de donn&eacute;es</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Dashboard personnalis&eacute;</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Rapport IA mensuel</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Support email</li>
              </ul>
              <Link href="/inscription" className="block w-full py-3 text-center rounded-xl border border-blue-200 text-blue-600 font-bold text-sm hover:bg-blue-50 transition-colors">Essai gratuit</Link>
            </div>
            {/* Pro */}
            <div className="bg-white rounded-2xl p-8 border-2 border-blue-500 shadow-xl shadow-blue-600/10 relative md:scale-105">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-600 to-blue-400 text-white text-[10px] font-bold uppercase tracking-widest px-4 py-1 rounded-full">Populaire</div>
              <div className="text-xs font-bold uppercase tracking-widest text-blue-600 mb-2">Pro</div>
              <div className="text-5xl font-black text-gray-900 tracking-tight">1 990</div>
              <div className="text-sm text-gray-500 mb-5">MAD / mois</div>
              <div className="text-xs text-gray-400 border-b border-gray-100 pb-5 mb-5">DAF / Dir. Commercial</div>
              <ul className="space-y-3 text-sm text-gray-600 text-left mb-6">
                <li className="flex gap-2"><span className="text-green-500">✓</span> 3 sources de donn&eacute;es</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Dashboard personnalis&eacute;</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Rapport IA + alertes temps r&eacute;el</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> WhatsApp + email</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Support prioritaire</li>
              </ul>
              <Link href="/inscription" className="block w-full py-3 text-center rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 text-white font-bold text-sm shadow-lg shadow-blue-600/25 hover:-translate-y-0.5 transition-all">Choisir Pro</Link>
            </div>
            {/* Equipe */}
            <div className="bg-white rounded-2xl p-8 border border-gray-100 hover:-translate-y-1 hover:shadow-lg transition-all">
              <div className="text-xs font-bold uppercase tracking-widest text-blue-600 mb-2">&Eacute;quipe</div>
              <div className="text-5xl font-black text-gray-900 tracking-tight">3 490</div>
              <div className="text-sm text-gray-500 mb-5">MAD / mois</div>
              <div className="text-xs text-gray-400 border-b border-gray-100 pb-5 mb-5">PME 50–200 salari&eacute;s</div>
              <ul className="space-y-3 text-sm text-gray-600 text-left mb-6">
                <li className="flex gap-2"><span className="text-green-500">✓</span> Sources illimit&eacute;es</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Multi-utilisateurs (5)</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Acc&egrave;s API</li>
                <li className="flex gap-2"><span className="text-green-500">✓</span> Support d&eacute;di&eacute; CSM</li>
              </ul>
              <Link href="/inscription" className="block w-full py-3 text-center rounded-xl border border-blue-200 text-blue-600 font-bold text-sm hover:bg-blue-50 transition-colors">Contacter</Link>
            </div>
          </div>
          <p className="text-sm text-gray-400 mt-8"><strong className="text-blue-600">–15% sur l&apos;engagement annuel</strong> &middot; 14 jours gratuits &middot; Sans carte bancaire</p>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-gradient-to-br from-blue-950 via-blue-900 to-blue-800 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="max-w-3xl mx-auto text-center relative z-10">
          <h2 className="text-4xl md:text-5xl font-black text-white tracking-tight mb-4">Pr&ecirc;t &agrave; piloter votre PME ?</h2>
          <p className="text-lg text-white/60 mb-8">Rejoignez les dirigeants marocains qui prennent des d&eacute;cisions &eacute;clair&eacute;es. Essai gratuit 14 jours.</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/inscription" className="px-8 py-4 bg-white text-blue-700 rounded-xl font-bold shadow-lg hover:-translate-y-0.5 transition-all">D&eacute;marrer gratuitement &rarr;</Link>
            <Link href="/connexion" className="px-8 py-4 bg-white/10 text-white border border-white/15 rounded-xl font-semibold hover:bg-white/15 transition-all">Se connecter</Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-950 py-12 px-6 text-gray-500">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between gap-8">
          <div>
            <div className="flex items-center gap-2.5 mb-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-400 rounded-lg flex items-center justify-center text-white font-extrabold text-sm">P</div>
              <span className="text-lg font-extrabold text-white tracking-tight">Pilot<span className="text-blue-400">BI</span></span>
            </div>
            <p className="text-sm max-w-xs">Intelligence d&eacute;cisionnelle pour PMEs marocaines.</p>
          </div>
          <div className="flex gap-16 text-sm">
            <div>
              <div className="font-bold text-white/70 uppercase tracking-wider text-xs mb-3">Produit</div>
              <div className="space-y-2"><a href="#solution" className="block hover:text-blue-400">Solution</a><a href="#features" className="block hover:text-blue-400">Fonctions</a><a href="#pricing" className="block hover:text-blue-400">Tarifs</a></div>
            </div>
            <div>
              <div className="font-bold text-white/70 uppercase tracking-wider text-xs mb-3">Contact</div>
              <div className="space-y-2"><span className="block">contact@pilotbi.ma</span><span className="block">LinkedIn</span></div>
            </div>
          </div>
        </div>
        <div className="max-w-6xl mx-auto border-t border-white/10 mt-8 pt-6 text-xs text-center">&copy; 2026 PilotBI. Tous droits r&eacute;serv&eacute;s.</div>
      </footer>
    </div>
  );
}
