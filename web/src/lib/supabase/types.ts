export type Json =
    | string
    | number
    | boolean
    | null
    | { [key: string]: Json | undefined }
    | Json[]

export type Database = {
    public: {
        Tables: {
            article_analyses: {
                Row: {
                    article_id: string
                    content: string
                    created_at: string | null
                    id: string
                    model: string | null
                    persona: string
                    tokens_used: number | null
                }
                Insert: {
                    article_id: string
                    content: string
                    created_at?: string | null
                    id?: string
                    model?: string | null
                    persona: string
                    tokens_used?: number | null
                }
                Update: {
                    article_id?: string
                    content?: string
                    created_at?: string | null
                    id?: string
                    model?: string | null
                    persona?: string
                    tokens_used?: number | null
                }
                Relationships: [
                    {
                        foreignKeyName: "article_analyses_article_id_fkey"
                        columns: ["article_id"]
                        isOneToOne: false
                        referencedRelation: "articles"
                        referencedColumns: ["id"]
                    },
                ]
            }
            article_embeddings: {
                Row: {
                    article_id: string
                    created_at: string | null
                    embedding: string | null
                    id: string
                    model: string | null
                }
                Insert: {
                    article_id: string
                    created_at?: string | null
                    embedding?: string | null
                    id?: string
                    model?: string | null
                }
                Update: {
                    article_id?: string
                    created_at?: string | null
                    embedding?: string | null
                    id?: string
                    model?: string | null
                }
                Relationships: [
                    {
                        foreignKeyName: "article_embeddings_article_id_fkey"
                        columns: ["article_id"]
                        isOneToOne: false
                        referencedRelation: "articles"
                        referencedColumns: ["id"]
                    },
                ]
            }
            article_tags: {
                Row: {
                    article_id: string
                    tag_id: string
                }
                Insert: {
                    article_id: string
                    tag_id: string
                }
                Update: {
                    article_id?: string
                    tag_id?: string
                }
                Relationships: [
                    {
                        foreignKeyName: "article_tags_article_id_fkey"
                        columns: ["article_id"]
                        isOneToOne: false
                        referencedRelation: "articles"
                        referencedColumns: ["id"]
                    },
                    {
                        foreignKeyName: "article_tags_tag_id_fkey"
                        columns: ["tag_id"]
                        isOneToOne: false
                        referencedRelation: "tags"
                        referencedColumns: ["id"]
                    },
                ]
            }
            articles: {
                Row: {
                    content: string | null
                    created_at: string | null
                    id: string
                    raindrop_id: number | null
                    source: string | null
                    status: string | null
                    title: string
                    updated_at: string | null
                    url: string | null
                    user_id: string
                }
                Insert: {
                    content?: string | null
                    created_at?: string | null
                    id?: string
                    raindrop_id?: number | null
                    source?: string | null
                    status?: string | null
                    title: string
                    updated_at?: string | null
                    url?: string | null
                    user_id: string
                }
                Update: {
                    content?: string | null
                    created_at?: string | null
                    id?: string
                    raindrop_id?: number | null
                    source?: string | null
                    status?: string | null
                    title?: string
                    updated_at?: string | null
                    url?: string | null
                    user_id?: string
                }
                Relationships: []
            }
            reflections: {
                Row: {
                    action_item: string | null
                    article_id: string
                    confidence: number | null
                    created_at: string | null
                    id: string
                    key_insight: string | null
                    tags: string[] | null
                    user_id: string
                    voice_used: boolean | null
                }
                Insert: {
                    action_item?: string | null
                    article_id: string
                    confidence?: number | null
                    created_at?: string | null
                    id?: string
                    key_insight?: string | null
                    tags?: string[] | null
                    user_id: string
                    voice_used?: boolean | null
                }
                Update: {
                    action_item?: string | null
                    article_id?: string
                    confidence?: number | null
                    created_at?: string | null
                    id?: string
                    key_insight?: string | null
                    tags?: string[] | null
                    user_id?: string
                    voice_used?: boolean | null
                }
                Relationships: [
                    {
                        foreignKeyName: "reflections_article_id_fkey"
                        columns: ["article_id"]
                        isOneToOne: false
                        referencedRelation: "articles"
                        referencedColumns: ["id"]
                    },
                ]
            }
            tags: {
                Row: {
                    color: string | null
                    id: string
                    name: string
                    user_id: string
                }
                Insert: {
                    color?: string | null
                    id?: string
                    name: string
                    user_id: string
                }
                Update: {
                    color?: string | null
                    id?: string
                    name?: string
                    user_id?: string
                }
                Relationships: []
            }
            user_settings: {
                Row: {
                    auth_provider: string | null
                    backup_enabled: boolean | null
                    backup_frequency: string | null
                    notification_browser: boolean | null
                    notification_email: boolean | null
                    notification_telegram: boolean | null
                    quiet_hours_enabled: boolean | null
                    quiet_hours_end: string | null
                    quiet_hours_start: string | null
                    raindrop_sync_enabled: boolean | null
                    raindrop_sync_mode: string | null
                    settings_json: Json | null
                    updated_at: string | null
                    user_id: string
                }
                Insert: {
                    auth_provider?: string | null
                    backup_enabled?: boolean | null
                    backup_frequency?: string | null
                    notification_browser?: boolean | null
                    notification_email?: boolean | null
                    notification_telegram?: boolean | null
                    quiet_hours_enabled?: boolean | null
                    quiet_hours_end?: string | null
                    quiet_hours_start?: string | null
                    raindrop_sync_enabled?: boolean | null
                    raindrop_sync_mode?: string | null
                    settings_json?: Json | null
                    updated_at?: string | null
                    user_id: string
                }
                Update: {
                    auth_provider?: string | null
                    backup_enabled?: boolean | null
                    backup_frequency?: string | null
                    notification_browser?: boolean | null
                    notification_email?: boolean | null
                    notification_telegram?: boolean | null
                    quiet_hours_enabled?: boolean | null
                    quiet_hours_end?: string | null
                    quiet_hours_start?: string | null
                    raindrop_sync_enabled?: boolean | null
                    raindrop_sync_mode?: string | null
                    settings_json?: Json | null
                    updated_at?: string | null
                    user_id?: string
                }
                Relationships: []
            }
            users_profile: {
                Row: {
                    avatar_url: string | null
                    created_at: string | null
                    display_name: string | null
                    id: string
                    language: string | null
                    timezone: string | null
                    updated_at: string | null
                }
                Insert: {
                    avatar_url?: string | null
                    created_at?: string | null
                    display_name?: string | null
                    id: string
                    language?: string | null
                    timezone?: string | null
                    updated_at?: string | null
                }
                Update: {
                    avatar_url?: string | null
                    created_at?: string | null
                    display_name?: string | null
                    id?: string
                    language?: string | null
                    timezone?: string | null
                    updated_at?: string | null
                }
                Relationships: []
            }
        }
        Views: {
            [_ in never]: never
        }
        Functions: {
            [_ in never]: never
        }
        Enums: {
            [_ in never]: never
        }
        CompositeTypes: {
            [_ in never]: never
        }
    }
}

// ── Convenience type aliases ──────────────────────────────────
type PublicSchema = Database["public"]

export type Tables<T extends keyof PublicSchema["Tables"]> =
    PublicSchema["Tables"][T]["Row"]

export type TablesInsert<T extends keyof PublicSchema["Tables"]> =
    PublicSchema["Tables"][T]["Insert"]

export type TablesUpdate<T extends keyof PublicSchema["Tables"]> =
    PublicSchema["Tables"][T]["Update"]

// ── Domain shortcuts ──────────────────────────────────────────
export type Article = Tables<"articles">
export type ArticleAnalysis = Tables<"article_analyses">
export type Reflection = Tables<"reflections">
export type Tag = Tables<"tags">
export type UserProfile = Tables<"users_profile">
export type UserSettings = Tables<"user_settings">
export type ArticleEmbedding = Tables<"article_embeddings">
export type PersonaType = "scout" | "builder" | "debater" | "chief"
export type ArticleStatus = "new" | "analyzing" | "analyzed" | "reflected"
