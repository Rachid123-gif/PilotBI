"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { User, Mail, Lock, Building2, ArrowRight, Loader2 } from "lucide-react";

export default function InscriptionPage() {
  const router = useRouter();
  const supabase = createClient();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSignUp(e: React.FormEvent) {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    if (password.length < 8) {
      setError("Le mot de passe doit contenir au moins 8 caracteres.");
      setIsLoading(false);
      return;
    }

    // Sign up with Supabase Auth
    // The DB trigger handle_new_user() auto-creates org + profile + trial subscription
    const { error: authError } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName,
          company_name: companyName,
        },
      },
    });

    if (authError) {
      setError(
        authError.message === "User already registered"
          ? "Cet email est deja utilise."
          : authError.message
      );
      setIsLoading(false);
      return;
    }

    router.push("/onboarding");
  }

  return (
    <div className="animate-fade-in">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold text-ink">Creer votre compte</h1>
        <p className="mt-1.5 text-sm text-ink-3">
          Commencez gratuitement, sans carte bancaire
        </p>
      </div>

      <form onSubmit={handleSignUp} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="fullName">Nom complet</Label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <Input
              id="fullName"
              type="text"
              placeholder="Mohammed Alami"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="pl-10"
              required
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">Email professionnel</Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <Input
              id="email"
              type="email"
              placeholder="m.alami@entreprise.ma"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10"
              required
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="password">Mot de passe</Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <Input
              id="password"
              type="password"
              placeholder="Minimum 8 caracteres"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10"
              minLength={8}
              required
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="company">Nom de l&apos;entreprise</Label>
          <div className="relative">
            <Building2 className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-ink-3" />
            <Input
              id="company"
              type="text"
              placeholder="Alami Distribution SARL"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
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
          Creer mon compte
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-ink-3">
        Deja un compte ?{" "}
        <Link
          href="/connexion"
          className="font-medium text-blue-600 hover:text-blue-700"
        >
          Se connecter
        </Link>
      </p>
    </div>
  );
}
