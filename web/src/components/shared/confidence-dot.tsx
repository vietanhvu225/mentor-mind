import { cn } from "@/lib/utils";

interface ConfidenceDotProps {
    score: number; // 1-10
    size?: "sm" | "md" | "lg";
    showLabel?: boolean;
    className?: string;
}

function getConfidenceColor(score: number) {
    if (score <= 3) return "bg-destructive"; // Red
    if (score <= 6) return "bg-warning"; // Amber
    return "bg-success"; // Green
}

function getConfidenceLabel(score: number) {
    if (score <= 3) return "Low";
    if (score <= 6) return "Medium";
    return "High";
}

const sizeMap = {
    sm: "h-2 w-2",
    md: "h-2.5 w-2.5",
    lg: "h-3 w-3",
};

export function ConfidenceDot({
    score,
    size = "md",
    showLabel = false,
    className,
}: ConfidenceDotProps) {
    return (
        <span className={cn("inline-flex items-center gap-1.5", className)}>
            <span
                className={cn("rounded-full shrink-0", sizeMap[size], getConfidenceColor(score))}
                title={`Confidence: ${score}/10`}
            />
            {showLabel && (
                <span className="text-xs text-muted-foreground">
                    {getConfidenceLabel(score)}
                </span>
            )}
        </span>
    );
}
