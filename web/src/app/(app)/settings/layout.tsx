import { SettingsSidebar } from "@/components/layout/settings-sidebar";

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex gap-6">
            <SettingsSidebar />
            <div className="flex-1 min-w-0 py-2">{children}</div>
        </div>
    );
}
