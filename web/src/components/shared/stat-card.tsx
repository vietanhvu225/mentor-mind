import { cn } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import type { LucideIcon } from "lucide-react";

interface StatCardProps {
    icon: LucideIcon;
    label: string;
    value: string | number;
    subtitle?: string;
    trend?: { value: number; label: string };
    className?: string;
}

export function StatCard({
    icon: Icon,
    label,
    value,
    subtitle,
    trend,
    className,
}: StatCardProps) {
    return (
        <Card className={cn("border-border/50", className)}>
            <CardContent className="p-4">
                <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
                        <Icon className="h-5 w-5 text-primary" />
                    </div>
                    <div className="min-w-0 flex-1">
                        <p className="text-xs font-medium text-muted-foreground truncate">
                            {label}
                        </p>
                        <div className="flex items-baseline gap-2">
                            <p className="text-2xl font-bold tracking-tight">{value}</p>
                            {trend && (
                                <span
                                    className={cn(
                                        "text-xs font-medium",
                                        trend.value >= 0 ? "text-success" : "text-destructive"
                                    )}
                                >
                                    {trend.value >= 0 ? "+" : ""}
                                    {trend.value}% {trend.label}
                                </span>
                            )}
                        </div>
                        {subtitle && (
                            <p className="text-xs text-muted-foreground mt-0.5">{subtitle}</p>
                        )}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
