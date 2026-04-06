"use client";

import { useState } from "react";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Mail, ArrowLeft, ArrowRight, Loader2, CheckCircle2 } from "lucide-react";

export default function MotDePasseOubliePage() {
  const supabase = createClient();

  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSent, setIsSent] = useState(false);

  async function handleReset(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/connexion`,
    });

    if (error) {
      setError("Erreur lors de l'envoi. Verifiez votre adresse email.");
      setIsLoading(false);
      return;
    }

    setIsSent(true);
    setIsLoading(false);
  }

  if (isSent) {
    return (
      <div className="text-center animate-fade-in">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-green-50">
          <CheckCircle2 className="h-7 w-7 text-green-600" />
        </div>
        <h1 className="text-xl font-semibold text-ink">Email envoye</h1>
        <p className="mt-2 text-sm text-ink-3">
          Si un compte existe avec l&apos;adresse{" "}
          <span className="font-medium text-ink-2">{email}</span>, vous
          recevrez un lien de reinitialisation.
        </p>
        <Link href="/connexion">
          <Button variant="ghost" className="mt-6 text-blue-600">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Retour a la connexion
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold text-ink">Mot de passe oublie</h1>
        <p className="mt-1.5 text-sm text-ink-3">
          Entrez votre email pour recevoir un lien de reinitialisation
        </p>
      </div>

      <form onSubmit={handleReset} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <Input
              id="email"
              type="email"
              placeholder="votre@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
            />
          </div>
        </div>

        {error && (
          <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
            {error}
          </div>
        )}

        <Button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white h-11 text-sm font-medium"
          disabled={isLoading}
        >
          {isLoading ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <ArrowRight className="mr-2 h-4 w-4" />
          )}
          Envoyer le lien
        </Button>
      </form>

      <div className="mt-6 text-center">
        <Link
          href="/connexion"
          className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
          Retour a la connexion
        </Link>
      </div>
    </div>
  );
}
