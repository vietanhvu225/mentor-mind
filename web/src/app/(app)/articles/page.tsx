import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { ConfidenceDot } from "@/components/shared/confidence-dot";

const mockArticles = [
    { id: "1", title: "Understanding Transformer Architecture", status: "analyzed", source: "arxiv.org", date: "Mar 5", confidence: 8 },
    { id: "2", title: "Building RAG Systems in Production", status: "reflected", source: "medium.com", date: "Mar 4", confidence: 6 },
    { id: "3", title: "Next.js 15 App Router Deep Dive", status: "new", source: "vercel.com", date: "Mar 7", confidence: 0 },
    { id: "4", title: "PostgreSQL Performance Tuning Guide", status: "analyzing", source: "postgres.ai", date: "Mar 3", confidence: 0 },
    { id: "5", title: "System Design Interview Patterns", status: "analyzed", source: "github.com", date: "Mar 2", confidence: 7 },
];

export default function ArticlesPage() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold">Articles</h1>
                    <p className="text-muted-foreground">Manage your learning materials</p>
                </div>
            </div>

            {/* Filter Tabs */}
            <Tabs defaultValue="all">
                <TabsList>
                    <TabsTrigger value="all">All (128)</TabsTrigger>
                    <TabsTrigger value="new">New (32)</TabsTrigger>
                    <TabsTrigger value="analyzed">Analyzed (64)</TabsTrigger>
                    <TabsTrigger value="reflected">Reflected (32)</TabsTrigger>
                </TabsList>
            </Tabs>

            {/* Articles Table */}
            <Card>
                <CardContent className="p-0">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead className="w-[50%]">Title</TableHead>
                                <TableHead>Source</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-center">Confidence</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {mockArticles.map((article) => (
                                <TableRow key={article.id} className="cursor-pointer hover:bg-muted/30">
                                    <TableCell className="font-medium">{article.title}</TableCell>
                                    <TableCell className="text-muted-foreground">{article.source}</TableCell>
                                    <TableCell className="text-muted-foreground">{article.date}</TableCell>
                                    <TableCell>
                                        <Badge
                                            variant={article.status === "reflected" ? "default" : "secondary"}
                                        >
                                            {article.status}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-center">
                                        {article.confidence > 0 ? (
                                            <ConfidenceDot score={article.confidence} showLabel />
                                        ) : (
                                            <span className="text-xs text-muted-foreground">—</span>
                                        )}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
