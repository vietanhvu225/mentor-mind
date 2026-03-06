"use client";

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Sparkles, Loader2 } from "lucide-react";
import { useState } from "react";

interface AnalyzeModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
}

export function AnalyzeModal({ open, onOpenChange }: AnalyzeModalProps) {
    const [url, setUrl] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleAnalyze = () => {
        if (!url.trim()) return;
        setIsLoading(true);
        // TODO: Wire to actual analyze API
        setTimeout(() => setIsLoading(false), 2000);
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <Sparkles className="h-5 w-5 text-primary" />
                        Analyze Article
                    </DialogTitle>
                    <DialogDescription>
                        Paste an article URL to analyze it with our AI multi-persona pipeline.
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-4 pt-2">
                    <div className="space-y-2">
                        <Label htmlFor="article-url">Article URL</Label>
                        <Input
                            id="article-url"
                            placeholder="https://example.com/article"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            disabled={isLoading}
                        />
                    </div>

                    <div className="rounded-lg bg-muted/50 p-3 text-sm text-muted-foreground">
                        <p className="font-medium text-foreground mb-1">Analysis Pipeline:</p>
                        <p>🔍 Scout → 🔧 Builder → ⚖️ Debater → 🎯 Chief</p>
                        <p className="mt-1 text-xs">Takes ~2-4 minutes depending on article length.</p>
                    </div>

                    {isLoading && (
                        <div className="flex items-center gap-3 rounded-lg bg-primary/5 border border-primary/20 p-3">
                            <Loader2 className="h-4 w-4 animate-spin text-primary" />
                            <div className="text-sm">
                                <p className="font-medium">Analyzing...</p>
                                <p className="text-muted-foreground text-xs">Scout is exploring the article</p>
                            </div>
                        </div>
                    )}

                    <div className="flex justify-end gap-2">
                        <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isLoading}>
                            Cancel
                        </Button>
                        <Button onClick={handleAnalyze} disabled={!url.trim() || isLoading}>
                            {isLoading ? (
                                <>
                                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="h-4 w-4 mr-2" />
                                    Start Analysis
                                </>
                            )}
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}
