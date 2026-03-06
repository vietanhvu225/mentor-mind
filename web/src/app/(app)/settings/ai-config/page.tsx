import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";

export default function AiConfigPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">AI Configuration</h2>
                <p className="text-sm text-muted-foreground">Configure AI models and analysis behavior</p>
            </div>
            <Card>
                <CardHeader><CardTitle className="text-base">Model Settings</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label>Stage 1 Model (Scout)</Label>
                        <Select defaultValue="gemini-3-pro">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="gemini-3-pro">Gemini 3 Pro</SelectItem>
                                <SelectItem value="gemini-3-flash">Gemini 3 Flash</SelectItem>
                                <SelectItem value="claude-sonnet">Claude Sonnet</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <Label>Stage 2 Model (Builder, Debater, Chief)</Label>
                        <Select defaultValue="claude-opus">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="claude-opus">Claude Opus (Thinking)</SelectItem>
                                <SelectItem value="gemini-3-pro">Gemini 3 Pro</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
