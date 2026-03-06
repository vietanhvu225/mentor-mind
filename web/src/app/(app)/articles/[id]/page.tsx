"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { PersonaTab } from "@/components/shared/persona-tab";
import { ReflectionModal } from "@/components/modals/reflection-modal";
import { MessageSquare, ExternalLink } from "lucide-react";
import { useState } from "react";
import type { PersonaType } from "@/components/shared/persona-tab";

const mockArticle = {
    title: "Understanding Transformer Architecture",
    source: "arxiv.org",
    url: "https://arxiv.org/example",
    content: `## Abstract\n\nThe Transformer model architecture has revolutionized natural language processing...\n\n## Key Concepts\n\n### Self-Attention Mechanism\nSelf-attention allows each position in a sequence to attend to all other positions...\n\n### Multi-Head Attention\nMulti-head attention extends self-attention by running multiple attention operations in parallel...`,
};

const mockAnalyses: Record<PersonaType, string> = {
    scout: "**Key findings:**\n\n1. Transformer eliminates recurrence entirely\n2. Attention mechanism scales O(n²) with sequence length\n3. Positional encoding preserves sequence order\n\n**Relevance:** High — foundational for understanding LLMs used in MentorMind.",
    builder: "**Architecture notes:**\n\n- Could implement attention visualization in our reader\n- Token limit awareness needed for chunking strategy\n- Consider Flash Attention for long articles",
    debater: "**Challenges:**\n\n1. O(n²) complexity = problematic for long documents\n2. Paper doesn't address multilingual well\n3. Training cost not discussed — significant barrier",
    chief: "**Summary:**\n\nTransformer is essential knowledge. Focus on attention mechanism understanding. Applicable to our AI pipeline design.",
};

export default function ArticleReaderPage() {
    const [activePersona, setActivePersona] = useState<PersonaType>("scout");
    const [reflectOpen, setReflectOpen] = useState(false);

    return (
        <>
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h1 className="text-xl font-bold">{mockArticle.title}</h1>
                    <a
                        href={mockArticle.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-muted-foreground hover:text-primary inline-flex items-center gap-1"
                    >
                        {mockArticle.source} <ExternalLink className="h-3 w-3" />
                    </a>
                </div>
                <Button variant="outline" onClick={() => setReflectOpen(true)} className="gap-2">
                    <MessageSquare className="h-4 w-4" />
                    Reflect
                </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-[calc(100vh-180px)]">
                {/* Left: Article content */}
                <Card className="overflow-auto">
                    <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-muted-foreground">Article Content</CardTitle>
                    </CardHeader>
                    <CardContent className="prose prose-invert prose-sm max-w-none">
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                            {mockArticle.content}
                        </div>
                    </CardContent>
                </Card>

                {/* Right: Analysis */}
                <Card className="overflow-auto">
                    <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-muted-foreground">AI Analysis</CardTitle>
                        <div className="flex gap-1 mt-2">
                            {(["scout", "builder", "debater", "chief"] as PersonaType[]).map(
                                (persona) => (
                                    <PersonaTab
                                        key={persona}
                                        persona={persona}
                                        isActive={activePersona === persona}
                                        onClick={() => setActivePersona(persona)}
                                        count={1}
                                    />
                                )
                            )}
                        </div>
                    </CardHeader>
                    <Separator />
                    <CardContent className="pt-4">
                        <div className="whitespace-pre-wrap text-sm leading-relaxed">
                            {mockAnalyses[activePersona]}
                        </div>
                    </CardContent>
                </Card>
            </div>

            <ReflectionModal
                open={reflectOpen}
                onOpenChange={setReflectOpen}
                articleTitle={mockArticle.title}
            />
        </>
    );
}
