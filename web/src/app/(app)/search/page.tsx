import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

export default function SearchPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Search</h1>
                <p className="text-muted-foreground">Search across your articles and analyses</p>
            </div>
            <div className="relative max-w-lg">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search by keyword, topic, or persona insight..." className="pl-9 h-11" />
            </div>
            <Card>
                <CardContent className="p-8 text-center text-muted-foreground">
                    <Search className="h-12 w-12 mx-auto mb-3 opacity-30" />
                    <p>Start typing to search across your knowledge base</p>
                    <p className="text-xs mt-1">Powered by pgvector semantic search</p>
                </CardContent>
            </Card>
        </div>
    );
}
