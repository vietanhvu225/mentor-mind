"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";
import type { Reflection, TablesInsert } from "@/lib/supabase/types";

const supabase = createClient();

export function useReflections(articleId?: string) {
    return useQuery({
        queryKey: ["reflections", articleId],
        queryFn: async () => {
            let query = supabase
                .from("reflections")
                .select("*")
                .order("created_at", { ascending: false });

            if (articleId) {
                query = query.eq("article_id", articleId);
            }

            const { data, error } = await query;
            if (error) throw error;
            return data as Reflection[];
        },
    });
}

export function useCreateReflection() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (reflection: TablesInsert<"reflections">) => {
            const { data, error } = await supabase
                .from("reflections")
                .insert(reflection)
                .select()
                .single();
            if (error) throw error;
            return data;
        },
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ["reflections"] });
            queryClient.invalidateQueries({
                queryKey: ["reflections", data.article_id],
            });
        },
    });
}
