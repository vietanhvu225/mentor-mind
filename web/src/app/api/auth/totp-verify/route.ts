import { verifyTOTP } from "@/lib/auth/totp";
import { NextResponse } from "next/server";
import { cookies } from "next/headers";

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

        return NextResponse.json({ success: true });
    } catch {
        return NextResponse.json(
            { success: false, error: "Verification failed" },
            { status: 500 }
        );
    }
}
