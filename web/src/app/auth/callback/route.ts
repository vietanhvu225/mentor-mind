import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
    const { searchParams, origin } = new URL(request.url);
    const code = searchParams.get("code");
    const tokenHash = searchParams.get("token_hash");
    const type = searchParams.get("type") as string | null;
    const next = searchParams.get("next") ?? "/dashboard";

    const supabase = await createClient();

    // OAuth code exchange (Google SSO)
    if (code) {
        const { error } = await supabase.auth.exchangeCodeForSession(code);
        if (!error) {
            return NextResponse.redirect(`${origin}${next}`);
        }
    }

    // Magic link token exchange (TOTP flow)
    if (tokenHash && type) {
        const { error } = await supabase.auth.verifyOtp({
            token_hash: tokenHash,
            type: type as "magiclink",
        });
        if (!error) {
            return NextResponse.redirect(`${origin}${next}`);
        }
    }

    // Auth error — redirect to login with error
    return NextResponse.redirect(`${origin}/login?error=auth_failed`);
}
