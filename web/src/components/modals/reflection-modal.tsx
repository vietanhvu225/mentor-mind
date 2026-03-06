"use client";

import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { ConfidenceDot } from "@/components/shared/confidence-dot";
import { MessageSquare, X } from "lucide-react";
import { useState } from "react";

interface ReflectionModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    articleTitle?: string;
}

export function ReflectionModal({
    open,
    onOpenChange,
    articleTitle,
}: ReflectionModalProps) {
    const [confidence, setConfidence] = useState([5]);
    const [tags, setTags] = useState<string[]>([]);
    const [tagInput, setTagInput] = useState("");

    const addTag = () => {
        const tag = tagInput.trim();
        if (tag && !tags.includes(tag)) {
            setTags([...tags, tag]);
            setTagInput("");
        }
    };

    const removeTag = (tagToRemove: string) => {
        setTags(tags.filter((t) => t !== tagToRemove));
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-lg">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <MessageSquare className="h-5 w-5 text-primary" />
                        Reflect
                    </DialogTitle>
                    {articleTitle && (
                        <DialogDescription className="truncate">
                            On: {articleTitle}
                        </DialogDescription>
                    )}
                </DialogHeader>

                <div className="space-y-4 pt-2">
                    {/* Key Insight */}
                    <div className="space-y-2">
                        <Label htmlFor="insight">Key Insight</Label>
                        <Textarea
                            id="insight"
                            placeholder="What was the most important takeaway?"
                            rows={3}
                        />
                    </div>

                    {/* Action Item */}
                    <div className="space-y-2">
                        <Label htmlFor="action">Action Item</Label>
                        <Input
                            id="action"
                            placeholder="What will you do differently?"
                        />
                    </div>

                    {/* Confidence */}
                    <div className="space-y-2">
                        <div className="flex items-center justify-between">
                            <Label>Confidence Level</Label>
                            <span className="flex items-center gap-1.5 text-sm">
                                <ConfidenceDot score={confidence[0]} />
                                {confidence[0]}/10
                            </span>
                        </div>
                        <Slider
                            value={confidence}
                            onValueChange={setConfidence}
                            min={1}
                            max={10}
                            step={1}
                            className="py-1"
                        />
                    </div>

                    {/* Tags */}
                    <div className="space-y-2">
                        <Label>Tags</Label>
                        <div className="flex gap-2">
                            <Input
                                placeholder="Add tag..."
                                value={tagInput}
                                onChange={(e) => setTagInput(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addTag())}
                                className="flex-1"
                            />
                            <Button variant="outline" size="sm" onClick={addTag}>
                                Add
                            </Button>
                        </div>
                        {tags.length > 0 && (
                            <div className="flex flex-wrap gap-1.5 mt-2">
                                {tags.map((tag) => (
                                    <Badge key={tag} variant="secondary" className="gap-1 pr-1">
                                        {tag}
                                        <button
                                            type="button"
                                            onClick={() => removeTag(tag)}
                                            className="ml-0.5 rounded-full hover:bg-muted-foreground/20 p-0.5"
                                        >
                                            <X className="h-3 w-3" />
                                        </button>
                                    </Badge>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="flex justify-end gap-2 pt-2">
                        <Button variant="outline" onClick={() => onOpenChange(false)}>
                            Cancel
                        </Button>
                        <Button>Save Reflection</Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}
