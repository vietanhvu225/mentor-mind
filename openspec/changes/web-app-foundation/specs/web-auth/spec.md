# Web Authentication

## Purpose
Hybrid authentication flow supporting Google SSO, email/password, and TOTP OTP.

## Requirements

### Requirement: Auth Provider Config
- `AUTH_PROVIDER` env var controls which auth methods are shown
- Values: `supabase` (Google + email), `totp` (OTP only), `both` (all 3)
- Config read at build time via `src/lib/auth/config.ts`

### Requirement: Google SSO
- Supabase Auth Google provider
- One-click "Sign in with Google" button
- Redirects to Google → callback → session → `/dashboard`

### Requirement: Email/Password
- Supabase Auth email provider
- Email + password fields
- Collapsed under "▸ More sign-in options" (hidden by default)
- Sign up disabled (single-user app — admin creates accounts)

### Requirement: TOTP OTP
- 6-digit input boxes (standard TOTP format)
- Verification via `otpauth` npm library
- Secret configured via `TOTP_SECRET` env var
- "Verify Code" button

### Requirement: Trust Device
- "Trust this device for 30 days" checkbox
- Sets httpOnly cookie `mm_trusted_device` with 30-day expiry
- When trusted: skip OTP on subsequent logins (go directly to dashboard)

### Requirement: Auth Middleware
- Next.js middleware (`middleware.ts`) at project root
- Checks Supabase session on every request to `(app)` routes
- No session → redirect to `/login`
- Valid session → continue
- `/login` with valid session → redirect to `/dashboard`

### Requirement: Auth Provider Component
- `AuthProvider` React context wrapping app
- Provides: `user`, `session`, `signOut()`, `isLoading`
- Listens to Supabase auth state changes
- `useAuth()` hook for consuming components

### Requirement: Login Page UI
- Matches Stitch mockup S6
- Logo `> MentorMind_` centered
- Subtitle "Your AI Learning Companion"
- Visual hierarchy: Google SSO → OTP → Email (top to bottom)
- Footer: "Auth mode: {provider} • v2.0"
