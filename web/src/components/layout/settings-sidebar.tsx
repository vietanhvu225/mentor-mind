"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    User,
    Shield,
    Bot,
    Cloud,
    Users,
    Bell,
    Database,
    Puzzle,
    Wrench,
} from "lucide-react";

const settingsNav = [
    { href: "/settings/profile", icon: User, label: "Profile" },
    { href: "/settings/auth", icon: Shield, label: "Authentication" },
    { href: "/settings/ai-config", icon: Bot, label: "AI Config" },
    { href: "/settings/raindrop", icon: Cloud, label: "Raindrop Sync" },
    { href: "/settings/analysis-team", icon: Users, label: "Analysis Team" },
    { href: "/settings/notifications", icon: Bell, label: "Notifications" },
    { href: "/settings/data-export", icon: Database, label: "Data & Export" },
    { href: "/settings/integrations", icon: Puzzle, label: "Integrations" },
    { href: "/settings/advanced", icon: Wrench, label: "Advanced" },
];

export function SettingsSidebar() {
    const pathname = usePathname();

    return (
        <nav className="w-[200px] shrink-0 border-r border-border py-4 pr-4">
            <h2 className="px-3 mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Settings
            </h2>
            <div className="flex flex-col gap-0.5">
                {settingsNav.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition-colors",
                                isActive
                                    ? "bg-primary/10 text-primary border-l-2 border-primary font-medium"
                                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                            )}
                        >
                            <item.icon className="h-4 w-4 shrink-0" />
                            {item.label}
                        </Link>
                    );
                })}
            </div>
        </nav>
    );
}
