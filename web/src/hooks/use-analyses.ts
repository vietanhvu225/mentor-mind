"use client";

import { useQuery } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";
import type { ArticleAnalysis, PersonaType } from "@/lib/supabase/types";

const supabase = createClient();

export function useAnalyses(articleId: string) {
    return useQuery({
        queryKey: ["analyses", articleId],
        queryFn: async () => {
            const { data, error } = await supabase
                .from("article_analyses")
                .select("*")
                .eq("article_id", articleId)
                .order("created_at", { ascending: true });
            if (error) throw error;
            return data as ArticleAnalysis[];
        },
        enabled: !!articleId,
    });
}

export function useAnalysisByPersona(articleId: string, persona: PersonaType) {
    return useQuery({
        queryKey: ["analyses", articleId, persona],
        queryFn: async () => {
            const { data, error } = await supabase
                .from("article_analyses")
                .select("*")
                .eq("article_id", articleId)
                .eq("persona", persona)
                .single();
            if (error) throw error;
            return data as ArticleAnalysis;
        },
        enabled: !!articleId,
    });
}
