"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Mail, Lock, ArrowRight, Loader2, Sparkles } from "lucide-react";

export default function ConnexionPage() {
  const router = useRouter();
  const supabase = createClient();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMagicLink, setIsMagicLink] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [magicLinkSent, setMagicLinkSent] = useState(false);

  async function handlePasswordLogin(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) {
      setError("Email ou mot de passe incorrect.");
      setIsLoading(false);
      return;
    }

    router.push("/tableau-de-bord");
  }

  async function handleMagicLink(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/tableau-de-bord`,
      },
    });

    if (error) {
      setError("Erreur lors de l'envoi du lien. Verifiez votre email.");
      setIsLoading(false);
      return;
    }

    setMagicLinkSent(true);
    setIsLoading(false);
  }

  if (magicLinkSent) {
    return (
      <div className="text-center animate-fade-in">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50">
          <Mail className="h-7 w-7 text-blue-600" />
        </div>
        <h1 className="text-xl font-semibold text-ink">Verifiez votre email</h1>
        <p className="mt-2 text-sm text-ink-3">
          Un lien de connexion a ete envoye a{" "}
          <span className="font-medium text-ink-2">{email}</span>
        </p>
        <Button
          variant="ghost"
          className="mt-6 text-blue-600"
          onClick={() => setMagicLinkSent(false)}
        >
          Retour
        </Button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold text-ink">Bon retour</h1>
        <p className="mt-1.5 text-sm text-ink-3">
          Connectez-vous a votre espace PilotBI
        </p>
      </div>

      <form
        onSubmit={isMagicLink ? handleMagicLink : handlePasswordLogin}
        className="space-y-4"
      >
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

        {!isMagicLink && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password">Mot de passe</Label>
              <Link
                href="/mot-de-passe-oublie"
                className="text-xs font-medium text-blue-600 hover:text-blue-700"
              >
                Mot de passe oublie ?
              </Link>
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
              <Input
                id="password"
                type="password"
                placeholder="Votre mot de passe"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="pl-10"
                required
              />
            </div>
          </div>
        )}

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
          {isMagicLink ? "Envoyer le lien" : "Se connecter"}
        </Button>
      </form>

      <div className="relative my-6">
        <Separator />
        <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-white px-3 text-xs text-ink-3">
          ou
        </span>
      </div>

      <Button
        variant="outline"
        className="w-full h-11 text-sm"
        onClick={() => {
          setIsMagicLink(!isMagicLink);
          setError(null);
        }}
      >
        <Sparkles className="mr-2 h-4 w-4 text-blue-500" />
        {isMagicLink ? "Se connecter avec mot de passe" : "Lien magique par email"}
      </Button>

      <p className="mt-6 text-center text-sm text-ink-3">
        Pas encore de compte ?{" "}
        <Link
          href="/inscription"
          className="font-medium text-blue-600 hover:text-blue-700"
        >
          Creer un compte
        </Link>
      </p>
    </div>
  );
}
