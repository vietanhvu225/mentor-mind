import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { MessageSquare, Mail, Globe } from "lucide-react";

export default function NotificationsPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Notifications</h2>
                <p className="text-sm text-muted-foreground">Manage how you receive alerts</p>
            </div>
            <Card>
                <CardHeader><CardTitle className="text-base">Channels</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                    {[
                        { icon: MessageSquare, label: "Telegram", desc: "Analysis results & weekly reports", defaultChecked: true },
                        { icon: Mail, label: "Email", desc: "Weekly digest summary", defaultChecked: false },
                        { icon: Globe, label: "Browser Push", desc: "Real-time analysis completion", defaultChecked: false },
                    ].map((ch) => (
                        <div key={ch.label} className="flex items-center gap-3">
                            <Checkbox id={ch.label} defaultChecked={ch.defaultChecked} />
                            <ch.icon className="h-4 w-4 text-muted-foreground" />
                            <div>
                                <Label htmlFor={ch.label} className="cursor-pointer">{ch.label}</Label>
                                <p className="text-xs text-muted-foreground">{ch.desc}</p>
                            </div>
                        </div>
                    ))}
                </CardContent>
            </Card>
            <Card>
                <CardHeader><CardTitle className="text-base">Quiet Hours</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                    <div className="flex items-center gap-3">
                        <Checkbox id="quiet" />
                        <Label htmlFor="quiet">Enable quiet hours</Label>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-1">
                            <Label className="text-xs">From</Label>
                            <Input type="time" defaultValue="22:00" />
                        </div>
                        <div className="space-y-1">
                            <Label className="text-xs">To</Label>
                            <Input type="time" defaultValue="07:00" />
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
