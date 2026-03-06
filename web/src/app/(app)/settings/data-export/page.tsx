import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Database, Download, Trash2, HardDrive } from "lucide-react";

export default function DataExportPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Data & Export</h2>
                <p className="text-sm text-muted-foreground">Manage your data and backups</p>
            </div>
            <Card>
                <CardHeader>
                    <CardTitle className="text-base flex items-center gap-2"><HardDrive className="h-4 w-4" /> Storage</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-2xl font-bold">12.4 MB</p>
                            <p className="text-xs text-muted-foreground">of 500 MB used</p>
                        </div>
                        <div className="h-2 flex-1 mx-6 rounded-full bg-muted overflow-hidden">
                            <div className="h-full w-[2.5%] bg-primary rounded-full" />
                        </div>
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader><CardTitle className="text-base flex items-center gap-2"><Download className="h-4 w-4" /> Export</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                    <Button variant="outline" className="w-full justify-start gap-2"><Download className="h-4 w-4" /> Export Articles (JSON)</Button>
                    <Button variant="outline" className="w-full justify-start gap-2"><Download className="h-4 w-4" /> Export Reflections (CSV)</Button>
                    <Button variant="outline" className="w-full justify-start gap-2"><Download className="h-4 w-4" /> Export All Data (ZIP)</Button>
                </CardContent>
            </Card>
            <Card>
                <CardHeader><CardTitle className="text-base flex items-center gap-2"><Database className="h-4 w-4" /> Backup</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                    <div className="space-y-2">
                        <Label>Auto Backup</Label>
                        <Select defaultValue="weekly">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                                <SelectItem value="disabled">Disabled</SelectItem>
                                <SelectItem value="daily">Daily</SelectItem>
                                <SelectItem value="weekly">Weekly</SelectItem>
                                <SelectItem value="monthly">Monthly</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>
            <Card className="border-destructive/30">
                <CardHeader>
                    <CardTitle className="text-base text-destructive flex items-center gap-2"><Trash2 className="h-4 w-4" /> Danger Zone</CardTitle>
                    <CardDescription>These actions are irreversible</CardDescription>
                </CardHeader>
                <CardContent>
                    <Button variant="destructive" size="sm">Delete All Data</Button>
                </CardContent>
            </Card>
        </div>
    );
}
