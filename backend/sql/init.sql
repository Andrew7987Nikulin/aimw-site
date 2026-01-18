-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table for embeddings + metadata
CREATE TABLE IF NOT EXISTS documents (
  id TEXT PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  namespace TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding vector(384)
);

CREATE INDEX IF NOT EXISTS documents_namespace_idx ON documents(namespace);
