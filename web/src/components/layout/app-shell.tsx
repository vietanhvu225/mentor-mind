"use client";

import { AppSidebar } from "./app-sidebar";
import { TopBar } from "./top-bar";
import { useState } from "react";
import { AnalyzeModal } from "@/components/modals/analyze-modal";

export function AppShell({ children }: { children: React.ReactNode }) {
    const [analyzeOpen, setAnalyzeOpen] = useState(false);

    return (
        <div className="min-h-screen">
            <AppSidebar />
            <div className="ml-[60px] flex flex-col min-h-screen">
                <TopBar onAnalyzeClick={() => setAnalyzeOpen(true)} />
                <main className="flex-1 p-6">{children}</main>
            </div>
            <AnalyzeModal open={analyzeOpen} onOpenChange={setAnalyzeOpen} />
        </div>
    );
}
