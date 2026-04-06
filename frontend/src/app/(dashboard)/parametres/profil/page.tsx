"use client";

import { useState } from "react";
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, Save, Loader2, User, Mail, Globe } from "lucide-react";
import { toast } from "sonner";

export default function ProfilPage() {
  const [fullName, setFullName] = useState("Mohammed Alami");
  const [email] = useState("m.alami@entreprise.ma");
  const [language, setLanguage] = useState("fr");
  const [isSaving, setIsSaving] = useState(false);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setIsSaving(true);
    // Simulate save
    await new Promise((resolve) => setTimeout(resolve, 800));
    setIsSaving(false);
    toast.success("Profil mis a jour avec succes");
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 animate-fade-in">
      <Link
        href="/parametres"
        className="inline-flex items-center text-sm text-ink-3 hover:text-ink transition-colors"
      >
        <ArrowLeft className="mr-1.5 h-4 w-4" />
        Parametres
      </Link>

      <div>
        <h1 className="text-2xl font-bold text-ink tracking-tight">
          Mon profil
        </h1>
        <p className="mt-1 text-sm text-ink-3">
          Modifiez vos informations personnelles
        </p>
      </div>

      <Card className="border-border/50 bg-white p-6 shadow-sm">
        <form onSubmit={handleSave} className="space-y-6">
          {/* Avatar */}
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-100 text-xl font-bold text-blue-700">
              MA
            </div>
            <div>
              <p className="font-medium text-ink">{fullName}</p>
              <p className="text-sm text-ink-3">{email}</p>
            </div>
          </div>

          <Separator />

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="fullName">Nom complet</Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
                <Input
                  id="fullName"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
                <Input
                  id="email"
                  value={email}
                  disabled
                  className="pl-10 bg-gray-50"
                />
              </div>
              <p className="text-xs text-ink-3">
                L&apos;email ne peut pas etre modifie
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="language">Langue</Label>
              <div className="relative">
                <Globe className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
                <select
                  id="language"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="flex h-10 w-full rounded-lg border border-input bg-background pl-10 pr-3 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                >
                  <option value="fr">Francais</option>
                  <option value="ar">Arabe</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <Button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white"
              disabled={isSaving}
            >
              {isSaving ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Save className="mr-2 h-4 w-4" />
              )}
              Enregistrer
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
