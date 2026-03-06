import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Wrench } from "lucide-react";

export default function AdvancedPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Advanced</h2>
                <p className="text-sm text-muted-foreground">Debug info and system configuration</p>
            </div>
            <Card>
                <CardHeader><CardTitle className="text-base flex items-center gap-2"><Wrench className="h-4 w-4" /> System Info</CardTitle></CardHeader>
                <CardContent>
                    <dl className="space-y-2 text-sm">
                        {[
                            ["Version", "2.0.0-alpha"],
                            ["Environment", "development"],
                            ["Auth Provider", "supabase + totp"],
                            ["Database", "Supabase PostgreSQL"],
                            ["Region", "Asia-Pacific (Singapore)"],
                        ].map(([label, value]) => (
                            <div key={label} className="flex justify-between">
                                <dt className="text-muted-foreground">{label}</dt>
                                <dd className="font-mono text-xs"><Badge variant="secondary">{value}</Badge></dd>
                            </div>
                        ))}
                    </dl>
                </CardContent>
            </Card>
        </div>
    );
}
