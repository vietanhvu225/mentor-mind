import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Shield } from "lucide-react";

export default function AuthSettingsPage() {
    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h2 className="text-xl font-bold">Authentication</h2>
                <p className="text-sm text-muted-foreground">Manage your sign-in methods</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base flex items-center gap-2">
                        <Shield className="h-4 w-4" /> Connected Accounts
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                    <div className="flex items-center justify-between p-3 rounded-lg border">
                        <div className="flex items-center gap-3">
                            <span className="text-lg">🔑</span>
                            <div>
                                <p className="font-medium text-sm">Google SSO</p>
                                <p className="text-xs text-muted-foreground">andy@gmail.com</p>
                            </div>
                        </div>
                        <Badge>Connected</Badge>
                    </div>
                    <div className="flex items-center justify-between p-3 rounded-lg border">
                        <div className="flex items-center gap-3">
                            <span className="text-lg">📱</span>
                            <div>
                                <p className="font-medium text-sm">TOTP Authenticator</p>
                                <p className="text-xs text-muted-foreground">Google Authenticator / Authy</p>
                            </div>
                        </div>
                        <Button variant="outline" size="sm">Setup</Button>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Change Password</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="current-pw">Current Password</Label>
                        <Input id="current-pw" type="password" />
                    </div>
                    <div className="space-y-2">
                        <Label htmlFor="new-pw">New Password</Label>
                        <Input id="new-pw" type="password" />
                    </div>
                    <Button>Update Password</Button>
                </CardContent>
            </Card>
        </div>
    );
}
