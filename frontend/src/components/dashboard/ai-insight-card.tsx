"use client";

import { useEffect, useState, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Sparkles, ArrowRight, Loader2, Bot } from "lucide-react";
import { api } from "@/lib/api";
import Link from "next/link";

export function AiInsightCard() {
  const [content, setContent] = useState<string | null>(null);
  const [displayText, setDisplayText] = useState("");
  const [loading, setLoading] = useState(true);
  const [typed, setTyped] = useState(false);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchInsights() {
      try {
        const data = await api.post<{ content: string | null }>("/dashboard/insights");
        if (!cancelled && data.content) {
          setContent(data.content);
        }
      } catch {
        // Insight is a bonus feature, fail silently
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetchInsights();
    return () => { cancelled = true; };
  }, []);

  // Typing effect
  useEffect(() => {
    if (!content || typed) return;

    let i = 0;
    intervalRef.current = setInterval(() => {
      if (i < content.length) {
        setDisplayText(content.slice(0, i + 1));
        i++;
      } else {
        if (intervalRef.current) clearInterval(intervalRef.current);
        setTyped(true);
      }
    }, 12);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [content, typed]);

  if (!loading && !content) return null;

  return (
    <Card className="relative overflow-hidden border-0 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 p-0 text-white shadow-xl">
      {/* Animated background orbs */}
      <div className="absolute -right-16 -top-16 h-48 w-48 rounded-full bg-white/[0.04] animate-pulse" style={{ animationDuration: "4s" }} />
      <div className="absolute right-20 -bottom-10 h-32 w-32 rounded-full bg-white/[0.03] animate-pulse" style={{ animationDuration: "6s" }} />
      <div className="absolute -left-8 top-1/2 h-24 w-24 rounded-full bg-white/[0.02]" />

      <div className="relative p-5 sm:p-6">
        <div className="flex items-start gap-4">
          {/* AI Avatar */}
          <div className="shrink-0 flex h-10 w-10 items-center justify-center rounded-xl bg-white/10 backdrop-blur-sm border border-white/10">
            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin text-blue-200" />
            ) : (
              <Bot className="h-5 w-5 text-white" />
            )}
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[11px] font-bold uppercase tracking-widest text-blue-200">
                Analyse IA
              </span>
              <Sparkles className="h-3 w-3 text-amber-300" />
            </div>

            {loading ? (
              <div className="space-y-2">
                <div className="h-3.5 w-3/4 rounded-full bg-white/10 animate-pulse" />
                <div className="h-3.5 w-1/2 rounded-full bg-white/10 animate-pulse" style={{ animationDelay: "150ms" }} />
              </div>
            ) : (
              <>
                <p className="text-[14px] leading-relaxed text-white/90 font-medium">
                  {displayText}
                  {!typed && <span className="inline-block w-0.5 h-4 bg-white/70 ml-0.5 animate-pulse" />}
                </p>
                <div className="mt-3">
                  <Link href="/rapports">
                    <Button
                      size="sm"
                      className="bg-white/10 hover:bg-white/20 text-white border border-white/10 text-[12px] h-8 px-3.5 font-semibold rounded-lg backdrop-blur-sm transition-all hover:scale-[1.02]"
                    >
                      Voir le rapport complet
                      <ArrowRight className="ml-1.5 h-3 w-3" />
                    </Button>
                  </Link>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
}
