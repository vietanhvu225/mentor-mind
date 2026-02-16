"""
Hardcoded test article for end-to-end pipeline testing.
"""

SAMPLE_ARTICLE = {
    "title": "Retrieval-Augmented Generation (RAG) in Production: Lessons Learned",
    "source_url": "https://example.com/rag-production-lessons",
    "raindrop_id": "test_article_001",
    "collection_name": "AI Research",
    "raw_content": """
Retrieval-Augmented Generation (RAG) in Production: Lessons Learned

After deploying RAG systems in production for the past year, here are the key lessons
we've learned about building reliable, scalable retrieval-augmented generation pipelines.

1. Chunking Strategy Matters More Than You Think

The most common mistake teams make is using fixed-size chunking without considering
document structure. We found that semantic chunking — splitting documents at natural
boundaries like paragraphs, sections, and topic shifts — improved retrieval accuracy
by 23% compared to naive 512-token chunks.

For technical documentation, we recommend:
- Respect heading hierarchy (H1, H2, H3 boundaries)
- Keep code blocks intact
- Maintain context windows of 256-1024 tokens
- Add metadata (source, section title, page number) to each chunk

2. Embedding Model Selection

We benchmarked 5 embedding models across our corpus:
- OpenAI text-embedding-3-large: Best overall quality, highest cost
- Cohere embed-v3: Good balance of quality and speed
- BGE-large-en-v1.5: Best open-source option
- E5-large-v2: Good for multilingual use cases
- all-MiniLM-L6-v2: Fastest, acceptable quality for prototyping

For production, we settled on Cohere embed-v3 with a fallback to BGE-large.
The key insight: embedding quality plateaus after a certain model size, but
retrieval pipeline design (chunking, reranking, filtering) has much more impact.

3. The Reranking Layer is Essential

Adding a cross-encoder reranker (like Cohere Rerank or a fine-tuned BERT model)
between retrieval and generation improved answer quality by 31%. This is because
bi-encoder embeddings optimize for recall, while cross-encoders optimize for
precision — you need both.

Our pipeline: Query → Bi-encoder retrieval (top 20) → Cross-encoder rerank (top 5)
→ LLM generation with top 5 contexts.

4. Evaluation is Hard But Necessary

We built a custom evaluation framework with 3 metrics:
- Faithfulness: Does the answer only use information from retrieved contexts?
- Relevance: Does the answer address the user's question?
- Completeness: Does the answer cover all relevant information?

Using LLM-as-judge (GPT-4) for automated evaluation saved us hundreds of hours
compared to manual annotation, with 89% agreement with human judges.

5. Production Considerations

- Cache embeddings aggressively (Redis) — embedding computation is expensive
- Monitor retrieval quality with A/B testing
- Implement graceful degradation: if retrieval fails, fall back to pure LLM
- Version your vector indices alongside your code
- Set up alerts for embedding drift (when new documents don't cluster well)

Conclusion: RAG is not just "plug in a vector database." It requires careful
engineering across the entire pipeline — from document processing to evaluation.
The teams that invest in each stage systematically outperform those that focus
only on the LLM component.
""".strip(),
}
