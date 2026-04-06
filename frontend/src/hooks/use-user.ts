"use client";

import { useCallback, useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import type { Profile, Subscription, Organization } from "@/types/database";
import type { User } from "@supabase/supabase-js";

interface UserState {
  user: User | null;
  profile: Profile | null;
  subscription: Subscription | null;
  organization: Organization | null;
  isLoading: boolean;
  error: string | null;
}

export function useUser() {
  const [state, setState] = useState<UserState>({
    user: null,
    profile: null,
    subscription: null,
    organization: null,
    isLoading: true,
    error: null,
  });

  const supabase = createClient();

  const fetchUserData = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, isLoading: true, error: null }));

      const {
        data: { user },
        error: userError,
      } = await supabase.auth.getUser();

      if (userError || !user) {
        setState({
          user: null,
          profile: null,
          subscription: null,
          organization: null,
          isLoading: false,
          error: userError?.message || null,
        });
        return;
      }

      // Fetch profile
      const { data: profile } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", user.id)
        .single();

      let subscription: Subscription | null = null;
      let organization: Organization | null = null;

      if (profile?.organization_id) {
        // Fetch organization
        const { data: org } = await supabase
          .from("organizations")
          .select("*")
          .eq("id", profile.organization_id)
          .single();
        organization = org;

        // Fetch subscription
        const { data: sub } = await supabase
          .from("subscriptions")
          .select("*")
          .eq("organization_id", profile.organization_id)
          .eq("status", "active")
          .single();
        subscription = sub;
      }

      setState({
        user,
        profile,
        subscription,
        organization,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      setState((prev) => ({
        ...prev,
        isLoading: false,
        error: err instanceof Error ? err.message : "Erreur inconnue",
      }));
    }
  }, [supabase]);

  useEffect(() => {
    fetchUserData();

    const {
      data: { subscription: authSubscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      if (session?.user) {
        fetchUserData();
      } else {
        setState({
          user: null,
          profile: null,
          subscription: null,
          organization: null,
          isLoading: false,
          error: null,
        });
      }
    });

    return () => {
      authSubscription.unsubscribe();
    };
  }, [fetchUserData, supabase.auth]);

  const signOut = useCallback(async () => {
    await supabase.auth.signOut();
  }, [supabase.auth]);

  return {
    ...state,
    signOut,
    refresh: fetchUserData,
    plan: (state.subscription?.plan ?? "starter") as
      | "starter"
      | "pro"
      | "equipe",
  };
}
