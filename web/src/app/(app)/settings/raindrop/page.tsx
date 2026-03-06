import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Cloud, RefreshCw } from "lucide-react";

export default function RaindropPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Raindrop Sync</h2>
                <p className="text-sm text-muted-foreground">Configure article sync from Raindrop.io</p>
            </div>
            <Card>
                <CardHeader>
                    <CardTitle className="text-base flex items-center gap-2">
                        <Cloud className="h-4 w-4" /> Connection Status
                    </CardTitle>
                </CardHeader>
                <CardContent className="flex items-center justify-between">
                    <div>
                        <p className="text-sm">Raindrop.io</p>
                        <p className="text-xs text-muted-foreground">Last sync: 10 minutes ago</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <Badge variant="default">Connected</Badge>
                        <Button variant="outline" size="sm"><RefreshCw className="h-3 w-3 mr-1" /> Sync Now</Button>
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader><CardTitle className="text-base">Sync Mode</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label>Collection Filter</Label>
                        <Select defaultValue="whitelist">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="whitelist">Whitelist (selected collections only)</SelectItem>
                                <SelectItem value="blacklist">Blacklist (exclude selected)</SelectItem>
                                <SelectItem value="all">All collections</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
