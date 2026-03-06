import { verifyTOTP } from "@/lib/auth/totp";
import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient } from "@supabase/supabase-js";

// Admin client for generating sign-in links
function getAdminClient() {
    return createClient(
        process.env.NEXT_PUBLIC_SUPABASE_URL!,
        process.env.SUPABASE_SERVICE_ROLE_KEY!
    );
}

export async function POST(request: Request) {
    try {
        const { code, trustDevice } = await request.json();

        if (!code || typeof code !== "string" || code.length !== 6) {
            return NextResponse.json(
                { success: false, error: "Invalid code format" },
                { status: 400 }
            );
        }

        const isValid = verifyTOTP(code);

        if (!isValid) {
            return NextResponse.json(
                { success: false, error: "Invalid or expired code" },
                { status: 401 }
            );
        }

        // TOTP valid → create a Supabase session for the admin user
        const adminEmail = process.env.TOTP_ADMIN_EMAIL;
        if (!adminEmail) {
            return NextResponse.json(
                { success: false, error: "TOTP_ADMIN_EMAIL not configured" },
                { status: 500 }
            );
        }

        const supabaseAdmin = getAdminClient();

        // Generate a magic link for the admin user
        const { data, error } = await supabaseAdmin.auth.admin.generateLink({
            type: "magiclink",
            email: adminEmail,
        });

        if (error || !data?.properties?.hashed_token) {
            console.error("Failed to generate magic link:", error);
            return NextResponse.json(
                { success: false, error: "Failed to create session" },
                { status: 500 }
            );
        }

        // Set trust device cookie if requested
        if (trustDevice) {
            const cookieStore = await cookies();
            cookieStore.set("mm_trusted_device", "true", {
                httpOnly: true,
                secure: process.env.NODE_ENV === "production",
                sameSite: "lax",
                maxAge: 30 * 24 * 60 * 60, // 30 days
                path: "/",
            });
        }

        // Return the verification token so client can exchange it for a session
        const tokenHash = data.properties.hashed_token;
        return NextResponse.json({
            success: true,
            redirectUrl: `/auth/callback?token_hash=${tokenHash}&type=magiclink`,
        });
    } catch (err) {
        console.error("TOTP verify error:", err);
        return NextResponse.json(
            { success: false, error: "Verification failed" },
            { status: 500 }
        );
    }
}
