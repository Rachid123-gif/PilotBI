"use client";

import Link from "next/link";
import { Card } from "@/components/ui/card";
import { User, CreditCard, ArrowRight } from "lucide-react";

const SETTINGS_LINKS = [
  {
    href: "/parametres/profil",
    title: "Mon profil",
    description: "Modifiez votre nom, email et preferences de langue",
    icon: User,
  },
  {
    href: "/parametres/facturation",
    title: "Facturation",
    description: "Gerez votre abonnement, consultez votre usage et factures",
    icon: CreditCard,
  },
];

export default function ParametresPage() {
  return (
    <div className="mx-auto max-w-2xl space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-ink tracking-tight">
          Parametres
        </h1>
        <p className="mt-1 text-sm text-ink-3">
          Gerez votre compte et votre abonnement
        </p>
      </div>

      <div className="grid gap-4">
        {SETTINGS_LINKS.map((item) => (
          <Link key={item.href} href={item.href}>
            <Card className="border-border/50 bg-white p-5 shadow-sm hover:shadow-md hover:border-blue-200 transition-all duration-200 group cursor-pointer">
              <div className="flex items-center gap-4">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-blue-600 group-hover:bg-blue-100 transition-colors">
                  <item.icon className="h-5 w-5" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-ink">{item.title}</h3>
                  <p className="text-sm text-ink-3">{item.description}</p>
                </div>
                <ArrowRight className="h-4 w-4 text-ink-3 group-hover:text-blue-600 group-hover:translate-x-0.5 transition-all" />
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
