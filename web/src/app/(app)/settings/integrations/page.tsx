import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Puzzle, Key, Cloud, MessageSquare } from "lucide-react";

export default function IntegrationsPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Integrations</h2>
                <p className="text-sm text-muted-foreground">Connect external services</p>
            </div>
            <Card>
                <CardHeader><CardTitle className="text-base">Connected Services</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                    {[
                        { icon: Cloud, name: "Raindrop.io", status: "connected" },
                        { icon: MessageSquare, name: "Telegram Bot", status: "connected" },
                    ].map((svc) => (
                        <div key={svc.name} className="flex items-center justify-between p-3 rounded-lg border">
                            <div className="flex items-center gap-3">
                                <svc.icon className="h-5 w-5 text-muted-foreground" />
                                <span className="font-medium text-sm">{svc.name}</span>
                            </div>
                            <Badge>Connected</Badge>
                        </div>
                    ))}
                </CardContent>
            </Card>
            <Card>
                <CardHeader><CardTitle className="text-base">Available Integrations</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                    {["Notion", "Obsidian", "Readwise"].map((name) => (
                        <div key={name} className="flex items-center justify-between p-3 rounded-lg border border-dashed">
                            <div className="flex items-center gap-3">
                                <Puzzle className="h-5 w-5 text-muted-foreground" />
                                <div>
                                    <span className="font-medium text-sm">{name}</span>
                                    <p className="text-xs text-muted-foreground">Coming soon</p>
                                </div>
                            </div>
                            <Badge variant="secondary">Planned</Badge>
                        </div>
                    ))}
                </CardContent>
            </Card>
            <Card>
                <CardHeader><CardTitle className="text-base flex items-center gap-2"><Key className="h-4 w-4" /> API Access</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                    <div className="space-y-2">
                        <Label>API Key</Label>
                        <div className="flex gap-2">
                            <Input value="mm_sk_••••••••••••••••" disabled className="font-mono text-xs" />
                            <Button variant="outline" size="sm">Regenerate</Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
