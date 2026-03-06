import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Toggle } from "@/components/ui/toggle";
import { PersonaTab } from "@/components/shared/persona-tab";
import type { PersonaType } from "@/components/shared/persona-tab";

const personas: { type: PersonaType; desc: string }[] = [
    { type: "scout", desc: "Explores and analyzes content, extracts key insights" },
    { type: "builder", desc: "System design perspective, evaluates applicability" },
    { type: "debater", desc: "Challenges claims, finds gaps, asks hard questions" },
    { type: "chief", desc: "Synthesizes insights, delivers final conclusions" },
];

export default function AnalysisTeamPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Analysis Team</h2>
                <p className="text-sm text-muted-foreground">Configure AI personas for article analysis</p>
            </div>
            {personas.map((p) => (
                <Card key={p.type}>
                    <CardContent className="p-4 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <PersonaTab persona={p.type} isActive />
                            <p className="text-sm text-muted-foreground">{p.desc}</p>
                        </div>
                        <Toggle defaultPressed aria-label={`Toggle ${p.type}`} />
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
