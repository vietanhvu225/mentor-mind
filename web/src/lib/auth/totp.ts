import * as OTPAuth from "otpauth";

/**
 * Verify a 6-digit TOTP code against the configured secret.
 * Uses SHA-1 algorithm, 6 digits, 30-second period (standard TOTP).
 */
export function verifyTOTP(token: string): boolean {
    const secret = process.env.TOTP_SECRET;
    if (!secret) {
        console.warn("TOTP_SECRET not configured");
        return false;
    }

    const totp = new OTPAuth.TOTP({
        issuer: process.env.TOTP_ISSUER || "MentorMind",
        label: "admin",
        algorithm: "SHA1",
        digits: 6,
        period: 30,
        secret: OTPAuth.Secret.fromBase32(secret),
    });

    // Allow 1 period window in each direction for clock drift
    const delta = totp.validate({ token, window: 1 });
    return delta !== null;
}
