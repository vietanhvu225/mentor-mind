"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip";
import {
    LayoutDashboard,
    FileText,
    Search,
    Settings,
} from "lucide-react";

const navItems = [
    { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
    { href: "/articles", icon: FileText, label: "Articles" },
    { href: "/search", icon: Search, label: "Search" },
];

const bottomItems = [
    { href: "/settings", icon: Settings, label: "Settings" },
];

export function AppSidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 z-40 flex h-screen w-[60px] flex-col border-r border-sidebar-border bg-sidebar">
            {/* Logo */}
            <div className="flex h-14 items-center justify-center border-b border-sidebar-border">
                <span className="logo-font text-lg text-primary">M</span>
            </div>

            {/* Main nav */}
            <nav className="flex flex-1 flex-col items-center gap-1 py-3">
                {navItems.map((item) => {
                    const isActive =
                        pathname === item.href || pathname.startsWith(item.href + "/");
                    return (
                        <Tooltip key={item.href} delayDuration={0}>
                            <TooltipTrigger asChild>
                                <Link
                                    href={item.href}
                                    className={cn(
                                        "flex h-10 w-10 items-center justify-center rounded-lg transition-colors",
                                        isActive
                                            ? "bg-primary/10 text-primary"
                                            : "text-sidebar-foreground/60 hover:bg-sidebar-accent hover:text-sidebar-foreground"
                                    )}
                                >
                                    <item.icon className="h-5 w-5" />
                                </Link>
                            </TooltipTrigger>
                            <TooltipContent side="right" sideOffset={8}>
                                {item.label}
                            </TooltipContent>
                        </Tooltip>
                    );
                })}
            </nav>

            {/* Bottom nav */}
            <div className="flex flex-col items-center gap-1 py-3 border-t border-sidebar-border">
                {bottomItems.map((item) => {
                    const isActive =
                        pathname === item.href || pathname.startsWith(item.href + "/");
                    return (
                        <Tooltip key={item.href} delayDuration={0}>
                            <TooltipTrigger asChild>
                                <Link
                                    href={item.href}
                                    className={cn(
                                        "flex h-10 w-10 items-center justify-center rounded-lg transition-colors",
                                        isActive
                                            ? "bg-primary/10 text-primary"
                                            : "text-sidebar-foreground/60 hover:bg-sidebar-accent hover:text-sidebar-foreground"
                                    )}
                                >
                                    <item.icon className="h-5 w-5" />
                                </Link>
                            </TooltipTrigger>
                            <TooltipContent side="right" sideOffset={8}>
                                {item.label}
                            </TooltipContent>
                        </Tooltip>
                    );
                })}
            </div>
        </aside>
    );
}
