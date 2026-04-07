"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sparkles, ArrowRight, Loader2 } from "lucide-react";
import { api } from "@/lib/api";
import Link from "next/link";

export function AiInsightCard() {
  const [content, setContent] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function fetchInsights() {
      try {
        const data = await api.post("/dashboard/insights");
        if (!cancelled && data.content) {
          setContent(data.content);
        }
      } catch {
        // Silently fail — insight is a bonus, not critical
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchInsights();
    return () => { cancelled = true; };
  }, []);

  if (!loading && !content) return null;

  return (
    <Card className="relative overflow-hidden border-0 bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 p-5 text-white shadow-lg">
      {/* Decorative elements */}
      <div className="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-white/5" />
      <div className="absolute -right-2 -bottom-6 h-20 w-20 rounded-full bg-white/5" />

      <div className="relative">
        <div className="flex items-center gap-2 mb-3">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-white/15">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="text-xs font-semibold uppercase tracking-wider text-blue-200">
            Analyse IA
          </span>
        </div>

        {loading ? (
          <div className="flex items-center gap-2 py-2">
            <Loader2 className="h-4 w-4 animate-spin text-blue-200" />
            <span className="text-sm text-blue-200">
              Analyse de vos donnees en cours...
            </span>
          </div>
        ) : (
          <>
            <p className="text-sm leading-relaxed text-white/95">{content}</p>
            <div className="mt-3">
              <Link href="/rapports">
                <Button
                  size="sm"
                  className="bg-white/15 hover:bg-white/25 text-white border-0 text-xs h-8 px-3"
                >
                  Voir le rapport complet
                  <ArrowRight className="ml-1.5 h-3 w-3" />
                </Button>
              </Link>
            </div>
          </>
        )}
      </div>
    </Card>
  );
}
