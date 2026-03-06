"use client";

import { useQuery } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";
import type { UserProfile, UserSettings } from "@/lib/supabase/types";
import { useEffect, useState } from "react";
import type { User } from "@supabase/supabase-js";

const supabase = createClient();

/** Auth state hook — listens to Supabase auth changes */
export function useAuth() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Get initial session
        supabase.auth.getUser().then(({ data: { user } }) => {
            setUser(user);
            setLoading(false);
        });

        // Listen for changes
        const {
            data: { subscription },
        } = supabase.auth.onAuthStateChange((_event, session) => {
            setUser(session?.user ?? null);
        });

        return () => subscription.unsubscribe();
    }, []);

    return { user, loading, isAuthenticated: !!user };
}

/** User profile hook */
export function useProfile() {
    const { user } = useAuth();
    return useQuery({
        queryKey: ["profile", user?.id],
        queryFn: async () => {
            const { data, error } = await supabase
                .from("users_profile")
                .select("*")
                .eq("id", user!.id)
                .single();
            if (error) throw error;
            return data as UserProfile;
        },
        enabled: !!user?.id,
    });
}

/** User settings hook */
export function useSettings() {
    const { user } = useAuth();
    return useQuery({
        queryKey: ["settings", user?.id],
        queryFn: async () => {
            const { data, error } = await supabase
                .from("user_settings")
                .select("*")
                .eq("user_id", user!.id)
                .single();
            if (error) throw error;
            return data as UserSettings;
        },
        enabled: !!user?.id,
    });
}
