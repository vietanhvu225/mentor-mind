import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

export type PersonaType = "scout" | "builder" | "debater" | "chief";

interface PersonaTabProps {
    persona: PersonaType;
    count?: number;
    isActive?: boolean;
    onClick?: () => void;
    className?: string;
}

const personaConfig: Record<
    PersonaType,
    { emoji: string; label: string; color: string; activeColor: string }
> = {
    scout: {
        emoji: "🔍",
        label: "Scout",
        color: "text-blue-400",
        activeColor: "bg-blue-500/10 border-blue-500/30",
    },
    builder: {
        emoji: "🔧",
        label: "Builder",
        color: "text-green-400",
        activeColor: "bg-green-500/10 border-green-500/30",
    },
    debater: {
        emoji: "⚖️",
        label: "Debater",
        color: "text-amber-400",
        activeColor: "bg-amber-500/10 border-amber-500/30",
    },
    chief: {
        emoji: "🎯",
        label: "Chief",
        color: "text-purple-400",
        activeColor: "bg-purple-500/10 border-purple-500/30",
    },
};

export function PersonaTab({
    persona,
    count,
    isActive = false,
    onClick,
    className,
}: PersonaTabProps) {
    const config = personaConfig[persona];

    return (
        <button
            type="button"
            onClick={onClick}
            className={cn(
                "flex items-center gap-2 px-3 py-2 rounded-lg border border-transparent",
                "transition-colors cursor-pointer",
                "hover:bg-muted/50",
                isActive && config.activeColor,
                className
            )}
        >
            <span className="text-base" role="img" aria-label={config.label}>
                {config.emoji}
            </span>
            <span
                className={cn(
                    "text-sm font-medium",
                    isActive ? config.color : "text-muted-foreground"
                )}
            >
                {config.label}
            </span>
            {count !== undefined && count > 0 && (
                <Badge
                    variant="secondary"
                    className="h-5 min-w-5 px-1.5 text-[10px] font-semibold"
                >
                    {count}
                </Badge>
            )}
        </button>
    );
}
