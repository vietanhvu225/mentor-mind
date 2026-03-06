import { StatCard } from "@/components/shared/stat-card";
import { Heatmap } from "@/components/shared/heatmap";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FileText, Brain, Flame, TrendingUp } from "lucide-react";

// Mock data — will be replaced with TanStack Query hooks
const mockHeatmapData = Array.from({ length: 84 }, () =>
    Math.random() > 0.6 ? Math.floor(Math.random() * 5) : 0
);

const mockArticles = [
    { id: "1", title: "Understanding Transformer Architecture", status: "analyzed", source: "arxiv.org", date: "2 days ago" },
    { id: "2", title: "Building RAG Systems in Production", status: "reflected", source: "medium.com", date: "3 days ago" },
    { id: "3", title: "Next.js 15 App Router Deep Dive", status: "new", source: "vercel.com", date: "Today" },
];

export default function DashboardPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Dashboard</h1>
                <p className="text-muted-foreground">Your learning overview</p>
            </div>

            {/* Stats Row */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <StatCard icon={FileText} label="Total Articles" value={128} trend={{ value: 12, label: "this week" }} />
                <StatCard icon={Brain} label="Analyzed" value={96} subtitle="75% completion rate" />
                <StatCard icon={Flame} label="Current Streak" value="7 days" />
                <StatCard icon={TrendingUp} label="Reflections" value={42} trend={{ value: 5, label: "this week" }} />
            </div>

            {/* Heatmap */}
            <Card>
                <CardHeader className="pb-3">
                    <CardTitle className="text-base font-medium">Learning Activity</CardTitle>
                </CardHeader>
                <CardContent>
                    <Heatmap data={mockHeatmapData} weeks={12} />
                </CardContent>
            </Card>

            {/* Recent Articles */}
            <Card>
                <CardHeader className="pb-3">
                    <CardTitle className="text-base font-medium">Recent Articles</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-3">
                        {mockArticles.map((article) => (
                            <div
                                key={article.id}
                                className="flex items-center justify-between rounded-lg border border-border/50 p-3 hover:bg-muted/30 transition-colors"
                            >
                                <div className="min-w-0 flex-1">
                                    <p className="font-medium truncate">{article.title}</p>
                                    <p className="text-xs text-muted-foreground">
                                        {article.source} • {article.date}
                                    </p>
                                </div>
                                <Badge
                                    variant={article.status === "reflected" ? "default" : "secondary"}
                                    className="ml-3 shrink-0"
                                >
                                    {article.status}
                                </Badge>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
