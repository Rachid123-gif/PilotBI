"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Building2, MapPin, Users, ArrowRight } from "lucide-react";
import { MOROCCAN_CITIES } from "@/lib/constants";

export default function OnboardingStep1() {
  const router = useRouter();
  const [companyName, setCompanyName] = useState("");
  const [city, setCity] = useState("");
  const [employeeCount, setEmployeeCount] = useState("");

  function handleNext(e: React.FormEvent) {
    e.preventDefault();
    // Store in sessionStorage for later submission
    sessionStorage.setItem(
      "onboarding",
      JSON.stringify({
        companyName,
        city,
        employeeCount: parseInt(employeeCount),
      })
    );
    router.push("/onboarding/secteur");
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-8 text-center">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50">
          <Building2 className="h-7 w-7 text-blue-600" />
        </div>
        <h1 className="text-2xl font-bold text-ink">
          Parlez-nous de votre entreprise
        </h1>
        <p className="mt-2 text-sm text-ink-3">
          Ces informations nous aident a personnaliser votre experience
        </p>
      </div>

      <form onSubmit={handleNext} className="space-y-5">
        <div className="space-y-2">
          <Label htmlFor="company">Nom de l&apos;entreprise</Label>
          <div className="relative">
            <Building2 className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <Input
              id="company"
              placeholder="Alami Distribution SARL"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="pl-10"
              required
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="city">Ville</Label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <select
              id="city"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="flex h-10 w-full rounded-lg border border-input bg-background pl-10 pr-3 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              required
            >
              <option value="">Selectionnez une ville</option>
              {MOROCCAN_CITIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="employees">Nombre d&apos;employes</Label>
          <div className="relative">
            <Users className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <select
              id="employees"
              value={employeeCount}
              onChange={(e) => setEmployeeCount(e.target.value)}
              className="flex h-10 w-full rounded-lg border border-input bg-background pl-10 pr-3 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              required
            >
              <option value="">Selectionnez</option>
              <option value="5">1 - 10</option>
              <option value="25">11 - 50</option>
              <option value="100">51 - 200</option>
              <option value="300">200+</option>
            </select>
          </div>
        </div>

        <Button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white h-11 mt-4"
        >
          Continuer
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </form>
    </div>
  );
}
