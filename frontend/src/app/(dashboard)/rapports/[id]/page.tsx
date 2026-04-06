import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  ArrowLeft,
  Download,
  FileBarChart,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Lightbulb,
} from "lucide-react";

// Demo report content
const DEMO_REPORT = {
  title: "Rapport mensuel - Mars 2026",
  period: "1 - 31 Mars 2026",
  generatedAt: "1 avril 2026",
  sections: {
    resume: `Le mois de mars 2026 marque une croissance significative pour l'entreprise avec un chiffre d'affaires de 2 847 500 MAD, en hausse de 8.9% par rapport au mois precedent. La marge nette s'est amelioree a 14.2%, portee par une meilleure gestion des couts d'approvisionnement et une diversification des fournisseurs. Le nombre de clients actifs atteint 347, un record historique pour l'entreprise.`,
    analyse: `L'analyse detaillee revele plusieurs tendances positives. Le segment alimentaire reste le moteur principal avec 45% du CA total (1.28M MAD). Les boissons progressent de 12% grace aux contrats avec deux nouveaux distributeurs regionaux. Le segment hygiene montre une croissance organique de 5%, soutenue par les campagnes promotionnelles du Ramadan. Le panier moyen B2B a augmente de 6.2% a 23 400 MAD, tandis que le delai moyen de paiement s'est reduit de 42 a 38 jours.`,
    anomalies: [
      "Depenses logistiques en hausse de 23% sans augmentation proportionnelle du volume - verifier les tarifs transporteur",
      "12 references en stock critique (seuil minimum atteint) - risque de rupture sur les produits a forte rotation",
      "Ecart de 45 000 MAD entre les ventes facturees et les encaissements du mois - relance necessaire",
    ],
    actions: [
      "Renegocier les contrats transport avant le 15 avril pour reduire les couts de 10-15%",
      "Passer commande urgente sur les 12 references critiques, priorite aux produits alimentaires",
      "Lancer la campagne de relance clients avec soldes superieurs a 30 000 MAD",
      "Preparer l'approvisionnement special Ramadan : augmenter les stocks boissons et dattes de 40%",
      "Evaluer l'opportunite d'ajouter un commercial terrain pour la region de Tanger-Tetouan",
    ],
  },
};

export default async function ReportDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <div className="mx-auto max-w-4xl space-y-6 animate-fade-in">
      {/* Back + actions */}
      <div className="flex items-center justify-between">
        <Link
          href="/rapports"
          className="inline-flex items-center text-sm text-ink-3 hover:text-ink transition-colors"
        >
          <ArrowLeft className="mr-1.5 h-4 w-4" />
          Retour aux rapports
        </Link>
        <Button variant="outline" size="sm">
          <Download className="mr-1.5 h-3.5 w-3.5" />
          Exporter PDF
        </Button>
      </div>

      {/* Header */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50">
            <FileBarChart className="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-ink">{DEMO_REPORT.title}</h1>
            <div className="mt-1 flex items-center gap-3 text-sm text-ink-3">
              <span>Periode : {DEMO_REPORT.period}</span>
              <span>|</span>
              <span>Genere le {DEMO_REPORT.generatedAt}</span>
            </div>
            <Badge className="mt-2 bg-emerald-50 text-emerald-700 border-emerald-200" variant="outline">
              Rapport #{id}
            </Badge>
          </div>
        </div>
      </Card>

      {/* Resume */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="h-5 w-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-ink">Resume executif</h2>
        </div>
        <p className="text-sm leading-relaxed text-ink-2">
          {DEMO_REPORT.sections.resume}
        </p>
      </Card>

      {/* Analyse */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <FileBarChart className="h-5 w-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-ink">Analyse detaillee</h2>
        </div>
        <p className="text-sm leading-relaxed text-ink-2">
          {DEMO_REPORT.sections.analyse}
        </p>
      </Card>

      {/* Anomalies */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="h-5 w-5 text-amber-500" />
          <h2 className="text-lg font-semibold text-ink">
            Anomalies detectees
          </h2>
        </div>
        <div className="space-y-3">
          {DEMO_REPORT.sections.anomalies.map((anomaly, index) => (
            <div
              key={index}
              className="flex gap-3 rounded-xl bg-amber-50 p-4"
            >
              <AlertTriangle className="h-4 w-4 shrink-0 text-amber-500 mt-0.5" />
              <p className="text-sm text-amber-800">{anomaly}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Actions */}
      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb className="h-5 w-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-ink">
            Actions recommandees
          </h2>
        </div>
        <div className="space-y-3">
          {DEMO_REPORT.sections.actions.map((action, index) => (
            <div
              key={index}
              className="flex gap-3 rounded-xl bg-blue-50 p-4"
            >
              <CheckCircle2 className="h-4 w-4 shrink-0 text-blue-600 mt-0.5" />
              <p className="text-sm text-blue-800">{action}</p>
            </div>
          ))}
        </div>
      </Card>

      <Separator />

      <p className="text-center text-xs text-ink-3 pb-4">
        Ce rapport a ete genere automatiquement par PilotBI. Les donnees
        proviennent de vos sources connectees.
      </p>
    </div>
  );
}
