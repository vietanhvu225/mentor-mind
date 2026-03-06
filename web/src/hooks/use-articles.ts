"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";
import type { Article, TablesInsert, TablesUpdate } from "@/lib/supabase/types";

const supabase = createClient();

export function useArticles(status?: string) {
    return useQuery({
        queryKey: ["articles", status],
        queryFn: async () => {
            let query = supabase
                .from("articles")
                .select("*")
                .order("created_at", { ascending: false });

            if (status && status !== "all") {
                query = query.eq("status", status);
            }

            const { data, error } = await query;
            if (error) throw error;
            return data as Article[];
        },
    });
}

export function useArticle(id: string) {
    return useQuery({
        queryKey: ["articles", id],
        queryFn: async () => {
            const { data, error } = await supabase
                .from("articles")
                .select("*")
                .eq("id", id)
                .single();
            if (error) throw error;
            return data as Article;
        },
        enabled: !!id,
    });
}

export function useCreateArticle() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (article: TablesInsert<"articles">) => {
            const { data, error } = await supabase
                .from("articles")
                .insert(article)
                .select()
                .single();
            if (error) throw error;
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["articles"] });
        },
    });
}

export function useUpdateArticle() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({
            id,
            ...updates
        }: TablesUpdate<"articles"> & { id: string }) => {
            const { data, error } = await supabase
                .from("articles")
                .update(updates)
                .eq("id", id)
                .select()
                .single();
            if (error) throw error;
            return data;
        },
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ["articles"] });
            queryClient.invalidateQueries({ queryKey: ["articles", data.id] });
        },
    });
}
