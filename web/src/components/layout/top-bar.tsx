"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Search, Sparkles, User, Settings, LogOut } from "lucide-react";
import Link from "next/link";

interface TopBarProps {
    onAnalyzeClick?: () => void;
}

export function TopBar({ onAnalyzeClick }: TopBarProps) {
    return (
        <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-6">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                    placeholder="Search articles..."
                    className="pl-9 bg-muted/50 border-transparent focus:border-primary/50"
                />
            </div>

            <div className="flex items-center gap-3 ml-auto">
                {/* Analyze button */}
                <Button
                    onClick={onAnalyzeClick}
                    className="gap-2 bg-primary hover:bg-primary/90"
                >
                    <Sparkles className="h-4 w-4" />
                    Analyze
                </Button>

                {/* User menu */}
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="relative h-9 w-9 rounded-full">
                            <Avatar className="h-9 w-9">
                                <AvatarImage src="" alt="User avatar" />
                                <AvatarFallback className="bg-primary/10 text-primary text-sm font-semibold">
                                    A
                                </AvatarFallback>
                            </Avatar>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-48">
                        <DropdownMenuItem asChild>
                            <Link href="/settings/profile" className="gap-2">
                                <User className="h-4 w-4" />
                                Profile
                            </Link>
                        </DropdownMenuItem>
                        <DropdownMenuItem asChild>
                            <Link href="/settings" className="gap-2">
                                <Settings className="h-4 w-4" />
                                Settings
                            </Link>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="gap-2 text-destructive focus:text-destructive">
                            <LogOut className="h-4 w-4" />
                            Log out
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </header>
    );
}
