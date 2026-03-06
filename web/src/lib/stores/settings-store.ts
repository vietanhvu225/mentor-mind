import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsState {
    // AI Config
    stage1Model: string;
    stage2Model: string;
    setStage1Model: (model: string) => void;
    setStage2Model: (model: string) => void;

    // Display
    language: string;
    setLanguage: (lang: string) => void;

    // Trust device (for TOTP skip)
    trustedDevice: boolean;
    setTrustedDevice: (trusted: boolean) => void;
}

export const useSettingsStore = create<SettingsState>()(
    persist(
        (set) => ({
            stage1Model: "gemini-3-pro",
            stage2Model: "claude-opus",
            setStage1Model: (model) => set({ stage1Model: model }),
            setStage2Model: (model) => set({ stage2Model: model }),

            language: "vi",
            setLanguage: (lang) => set({ language: lang }),

            trustedDevice: false,
            setTrustedDevice: (trusted) => set({ trustedDevice: trusted }),
        }),
        {
            name: "mentormind-settings",
        }
    )
);
