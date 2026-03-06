/**
 * Auth configuration — reads AUTH_PROVIDER env to determine enabled methods.
 *
 * "supabase" → Google SSO + Email/Password
 * "totp"     → OTP only
 * "both"     → All methods (default)
 */

export type AuthMode = "supabase" | "totp" | "both";

export const AUTH_MODE: AuthMode =
    (process.env.AUTH_PROVIDER as AuthMode) || "both";

export const authConfig = {
    mode: AUTH_MODE,
    googleEnabled: AUTH_MODE === "supabase" || AUTH_MODE === "both",
    emailEnabled: AUTH_MODE === "supabase" || AUTH_MODE === "both",
    totpEnabled: AUTH_MODE === "totp" || AUTH_MODE === "both",
    trustDeviceDays: 30,
    trustDeviceCookieName: "mm_trusted_device",
    totpIssuer: process.env.TOTP_ISSUER || "MentorMind",
};
