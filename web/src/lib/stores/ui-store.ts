import { create } from "zustand";
import type { ArticleStatus } from "@/lib/supabase/types";

interface UIState {
    // Sidebar
    sidebarCollapsed: boolean;
    toggleSidebar: () => void;

    // Modals
    analyzeModalOpen: boolean;
    setAnalyzeModalOpen: (open: boolean) => void;
    reflectionModalOpen: boolean;
    reflectionArticleId: string | null;
    openReflectionModal: (articleId: string) => void;
    closeReflectionModal: () => void;

    // Filters
    articleFilter: ArticleStatus | "all";
    setArticleFilter: (filter: ArticleStatus | "all") => void;
    searchQuery: string;
    setSearchQuery: (query: string) => void;
}

export const useUIStore = create<UIState>((set) => ({
    // Sidebar
    sidebarCollapsed: true,
    toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

    // Modals
    analyzeModalOpen: false,
    setAnalyzeModalOpen: (open) => set({ analyzeModalOpen: open }),
    reflectionModalOpen: false,
    reflectionArticleId: null,
    openReflectionModal: (articleId) =>
        set({ reflectionModalOpen: true, reflectionArticleId: articleId }),
    closeReflectionModal: () =>
        set({ reflectionModalOpen: false, reflectionArticleId: null }),

    // Filters
    articleFilter: "all",
    setArticleFilter: (filter) => set({ articleFilter: filter }),
    searchQuery: "",
    setSearchQuery: (query) => set({ searchQuery: query }),
}));
