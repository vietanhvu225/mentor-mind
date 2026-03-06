"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { authConfig } from "@/lib/auth/config";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Separator } from "@/components/ui/separator";
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
    Loader2,
    ChevronRight,
    Mail,
    Lock,
} from "lucide-react";

export default function LoginPage() {
    const router = useRouter();
    const supabase = createClient();

    const [loading, setLoading] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Email form
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [emailOpen, setEmailOpen] = useState(false);

    // TOTP form
    const [otpDigits, setOtpDigits] = useState(["", "", "", "", "", ""]);
    const [trustDevice, setTrustDevice] = useState(false);

    // ── Google SSO ──
    const handleGoogleLogin = async () => {
        setLoading("google");
        setError(null);
        const { error } = await supabase.auth.signInWithOAuth({
            provider: "google",
            options: {
                redirectTo: `${window.location.origin}/auth/callback`,
            },
        });
        if (error) {
            setError(error.message);
            setLoading(null);
        }
    };

    // ── Email/Password ──
    const handleEmailLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading("email");
        setError(null);
        const { error } = await supabase.auth.signInWithPassword({
            email,
            password,
        });
        if (error) {
            setError(error.message);
            setLoading(null);
        } else {
            router.push("/dashboard");
        }
    };

    // ── TOTP ──
    const handleOtpChange = (index: number, value: string) => {
        if (value.length > 1) value = value.slice(-1);
        if (!/^\d*$/.test(value)) return;

        const newDigits = [...otpDigits];
        newDigits[index] = value;
        setOtpDigits(newDigits);

        // Auto-focus next input
        if (value && index < 5) {
            const next = document.getElementById(`otp-${index + 1}`);
            next?.focus();
        }
    };

    const handleOtpKeyDown = (index: number, e: React.KeyboardEvent) => {
        if (e.key === "Backspace" && !otpDigits[index] && index > 0) {
            const prev = document.getElementById(`otp-${index - 1}`);
            prev?.focus();
        }
    };

    const handleOtpPaste = (e: React.ClipboardEvent) => {
        e.preventDefault();
        const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
        const newDigits = [...otpDigits];
        for (let i = 0; i < pasted.length; i++) {
            newDigits[i] = pasted[i];
        }
        setOtpDigits(newDigits);
        // Focus last filled or the 6th box
        const focusIdx = Math.min(pasted.length, 5);
        document.getElementById(`otp-${focusIdx}`)?.focus();
    };

    const handleOtpVerify = async () => {
        const code = otpDigits.join("");
        if (code.length !== 6) return;

        setLoading("totp");
        setError(null);

        try {
            const res = await fetch("/api/auth/totp-verify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code, trustDevice }),
            });
            const data = await res.json();
            if (data.success && data.redirectUrl) {
                // Redirect to auth callback to establish Supabase session
                window.location.href = data.redirectUrl;
            } else {
                setError(data.error || "Invalid code");
                setLoading(null);
            }
        } catch {
            setError("Verification failed");
            setLoading(null);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4">
            <div className="w-full max-w-sm space-y-6">
                {/* Logo & tagline */}
                <div className="text-center space-y-1">
                    <h1 className="logo-font text-3xl text-primary">&gt; MentorMind_</h1>
                    <p className="text-sm text-muted-foreground">
                        Your AI Learning Companion
                    </p>
                </div>

                <Card className="border-border/50">
                    <CardContent className="pt-6 space-y-4">
                        {/* Error display */}
                        {error && (
                            <div className="rounded-lg bg-destructive/10 border border-destructive/30 p-3 text-sm text-destructive">
                                {error}
                            </div>
                        )}

                        {/* ── Google SSO ── */}
                        {authConfig.googleEnabled && (
                            <Button
                                variant="outline"
                                className="w-full h-11 gap-3 text-sm font-medium"
                                onClick={handleGoogleLogin}
                                disabled={loading !== null}
                            >
                                {loading === "google" ? (
                                    <Loader2 className="h-4 w-4 animate-spin" />
                                ) : (
                                    <svg className="h-5 w-5" viewBox="0 0 24 24">
                                        <path
                                            fill="#4285F4"
                                            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
                                        />
                                        <path
                                            fill="#34A853"
                                            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                        />
                                        <path
                                            fill="#FBBC05"
                                            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                        />
                                        <path
                                            fill="#EA4335"
                                            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                        />
                                    </svg>
                                )}
                                Sign in with Google
                            </Button>
                        )}

                        {/* ── TOTP ── */}
                        {authConfig.totpEnabled && (
                            <>
                                {authConfig.googleEnabled && (
                                    <div className="relative">
                                        <Separator />
                                        <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-card px-2 text-xs text-muted-foreground">
                                            or
                                        </span>
                                    </div>
                                )}

                                <div className="space-y-3">
                                    <Label className="text-sm font-medium">Authenticator Code</Label>
                                    <div
                                        className="flex gap-2 justify-center"
                                        onPaste={handleOtpPaste}
                                    >
                                        {otpDigits.map((digit, i) => (
                                            <Input
                                                key={i}
                                                id={`otp-${i}`}
                                                type="text"
                                                inputMode="numeric"
                                                maxLength={1}
                                                value={digit}
                                                onChange={(e) => handleOtpChange(i, e.target.value)}
                                                onKeyDown={(e) => handleOtpKeyDown(i, e)}
                                                className="w-10 h-12 text-center text-lg font-mono"
                                                disabled={loading !== null}
                                            />
                                        ))}
                                    </div>

                                    <div className="flex items-center gap-2">
                                        <Checkbox
                                            id="trust-device"
                                            checked={trustDevice}
                                            onCheckedChange={(checked) =>
                                                setTrustDevice(checked === true)
                                            }
                                        />
                                        <Label htmlFor="trust-device" className="text-xs text-muted-foreground cursor-pointer">
                                            Trust this device for 30 days
                                        </Label>
                                    </div>

                                    <Button
                                        className="w-full"
                                        onClick={handleOtpVerify}
                                        disabled={otpDigits.join("").length !== 6 || loading !== null}
                                    >
                                        {loading === "totp" ? (
                                            <Loader2 className="h-4 w-4 animate-spin mr-2" />
                                        ) : null}
                                        Verify Code
                                    </Button>
                                </div>
                            </>
                        )}

                        {/* ── Email/Password (collapsed) ── */}
                        {authConfig.emailEnabled && (
                            <>
                                <Separator />
                                <Collapsible open={emailOpen} onOpenChange={setEmailOpen}>
                                    <CollapsibleTrigger className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors w-full">
                                        <ChevronRight
                                            className={`h-4 w-4 transition-transform ${emailOpen ? "rotate-90" : ""}`}
                                        />
                                        More sign-in options
                                    </CollapsibleTrigger>
                                    <CollapsibleContent className="pt-3">
                                        <form onSubmit={handleEmailLogin} className="space-y-3">
                                            <div className="space-y-2">
                                                <Label htmlFor="email" className="text-xs">Email</Label>
                                                <div className="relative">
                                                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                                    <Input
                                                        id="email"
                                                        type="email"
                                                        placeholder="you@example.com"
                                                        value={email}
                                                        onChange={(e) => setEmail(e.target.value)}
                                                        className="pl-9"
                                                        disabled={loading !== null}
                                                    />
                                                </div>
                                            </div>
                                            <div className="space-y-2">
                                                <Label htmlFor="password" className="text-xs">Password</Label>
                                                <div className="relative">
                                                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                                                    <Input
                                                        id="password"
                                                        type="password"
                                                        placeholder="••••••••"
                                                        value={password}
                                                        onChange={(e) => setPassword(e.target.value)}
                                                        className="pl-9"
                                                        disabled={loading !== null}
                                                    />
                                                </div>
                                            </div>
                                            <Button
                                                type="submit"
                                                variant="secondary"
                                                className="w-full"
                                                disabled={!email || !password || loading !== null}
                                            >
                                                {loading === "email" ? (
                                                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                                                ) : null}
                                                Sign in with Email
                                            </Button>
                                        </form>
                                    </CollapsibleContent>
                                </Collapsible>
                            </>
                        )}
                    </CardContent>
                </Card>

                {/* Footer */}
                <p className="text-center text-xs text-muted-foreground">
                    Auth mode: {authConfig.mode} • v2.0
                </p>
            </div>
        </div>
    );
}
