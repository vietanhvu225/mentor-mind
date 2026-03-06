import { cn } from "@/lib/utils";
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from "@/components/ui/tooltip";

interface HeatmapProps {
    /** Array of activity values for the last N days (0 = no activity) */
    data: number[];
    /** Number of weeks to display */
    weeks?: number;
    className?: string;
}

function getIntensity(value: number, max: number): string {
    if (value === 0) return "bg-muted/30";
    const ratio = value / max;
    if (ratio <= 0.25) return "bg-primary/20";
    if (ratio <= 0.5) return "bg-primary/40";
    if (ratio <= 0.75) return "bg-primary/60";
    return "bg-primary";
}

function formatDate(daysAgo: number): string {
    const date = new Date();
    date.setDate(date.getDate() - daysAgo);
    return date.toLocaleDateString("vi-VN", {
        day: "numeric",
        month: "short",
    });
}

export function Heatmap({ data, weeks = 12, className }: HeatmapProps) {
    const totalDays = weeks * 7;
    // Pad data to fill the grid
    const paddedData = [
        ...Array(Math.max(0, totalDays - data.length)).fill(0),
        ...data.slice(-totalDays),
    ];
    const max = Math.max(...paddedData, 1);

    // Build grid: columns = weeks, rows = 7 days (Mon-Sun)
    const grid: number[][] = [];
    for (let w = 0; w < weeks; w++) {
        const week: number[] = [];
        for (let d = 0; d < 7; d++) {
            week.push(paddedData[w * 7 + d]);
        }
        grid.push(week);
    }

    const dayLabels = ["Mon", "", "Wed", "", "Fri", "", ""];

    return (
        <div className={cn("flex gap-1", className)}>
            {/* Day labels */}
            <div className="flex flex-col gap-[3px] pr-1">
                {dayLabels.map((label, i) => (
                    <span
                        key={i}
                        className="h-3 w-6 text-[9px] text-muted-foreground leading-3"
                    >
                        {label}
                    </span>
                ))}
            </div>

            {/* Grid */}
            {grid.map((week, wi) => (
                <div key={wi} className="flex flex-col gap-[3px]">
                    {week.map((value, di) => {
                        const daysAgo = totalDays - (wi * 7 + di) - 1;
                        return (
                            <Tooltip key={`${wi}-${di}`}>
                                <TooltipTrigger asChild>
                                    <div
                                        className={cn(
                                            "h-3 w-3 rounded-[2px] transition-colors",
                                            getIntensity(value, max)
                                        )}
                                    />
                                </TooltipTrigger>
                                <TooltipContent side="top" className="text-xs">
                                    <p>
                                        {value} {value === 1 ? "article" : "articles"} •{" "}
                                        {formatDate(daysAgo)}
                                    </p>
                                </TooltipContent>
                            </Tooltip>
                        );
                    })}
                </div>
            ))}
        </div>
    );
}
