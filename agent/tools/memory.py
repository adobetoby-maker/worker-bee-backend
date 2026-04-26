import chromadb, os, json, pathlib
from datetime import datetime

DB_PATH = str(pathlib.Path.home() / "worker-bee" / ".chromadb")

class MemoryTool:
    def __init__(self, tab_id: str = "default"):
        self.tab_id  = tab_id
        self.client  = chromadb.PersistentClient(path=DB_PATH)

        # Three collections — conversations, actions, knowledge
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            metadata={"hnsw:space": "cosine"}
        )
        self.actions = self.client.get_or_create_collection(
            name="actions",
            metadata={"hnsw:space": "cosine"}
        )
        self.knowledge = self.client.get_or_create_collection(
            name="knowledge",
            metadata={"hnsw:space": "cosine"}
        )

    def _ts(self) -> str:
        return datetime.now().isoformat()

    def _id(self, prefix: str) -> str:
        import uuid
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    # ── Store ──────────────────────────────────────────────────

    def store_message(self, role: str, content: str,
                      model: str = "") -> str:
        """Store a conversation message."""
        doc_id = self._id("msg")
        self.conversations.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[{
                "role":    role,
                "model":   model,
                "tab_id":  self.tab_id,
                "ts":      self._ts(),
                "type":    "message"
            }]
        )
        return doc_id

    def store_action(self, action: str, target: str,
                     result: str, success: bool) -> str:
        """Store an agent action — browser, shell, login etc."""
        doc_id = self._id("act")
        content = f"{action} → {target}: {result[:500]}"
        self.actions.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[{
                "action":  action,
                "target":  target,
                "success": str(success),
                "tab_id":  self.tab_id,
                "ts":      self._ts(),
                "type":    "action"
            }]
        )
        return doc_id

    def store_knowledge(self, topic: str, content: str,
                        source: str = "") -> str:
        """Store a piece of knowledge — a fix, a pattern, a fact."""
        doc_id = self._id("knw")
        self.knowledge.add(
            ids=[doc_id],
            documents=[f"{topic}: {content}"],
            metadatas=[{
                "topic":   topic,
                "source":  source,
                "tab_id":  self.tab_id,
                "ts":      self._ts(),
                "type":    "knowledge"
            }]
        )
        return doc_id

    # ── Search ─────────────────────────────────────────────────

    def search(self, query: str, n: int = 5) -> list:
        """Search across all collections."""
        results = []

        for collection in [self.conversations,
                           self.actions,
                           self.knowledge]:
            try:
                r = collection.query(
                    query_texts=[query],
                    n_results=min(n, collection.count())
                )
                if r and r["documents"] and r["documents"][0]:
                    for doc, meta, dist in zip(
                        r["documents"][0],
                        r["metadatas"][0],
                        r["distances"][0]
                    ):
                        results.append({
                            "content":   doc,
                            "metadata":  meta,
                            "relevance": round(1 - dist, 3)
                        })
            except Exception:
                pass

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:n]

    def search_actions(self, query: str, n: int = 3) -> list:
        """Search only past actions — useful for 'how did I fix X'."""
        try:
            r = self.actions.query(
                query_texts=[query],
                n_results=min(n, self.actions.count())
            )
            if r and r["documents"] and r["documents"][0]:
                return [
                    {"content": doc, "metadata": meta}
                    for doc, meta in zip(
                        r["documents"][0],
                        r["metadatas"][0]
                    )
                ]
        except Exception:
            pass
        return []

    def search_knowledge(self, query: str, n: int = 3) -> list:
        """Search stored knowledge and patterns."""
        try:
            r = self.knowledge.query(
                query_texts=[query],
                n_results=min(n, self.knowledge.count())
            )
            if r and r["documents"] and r["documents"][0]:
                return [
                    {"content": doc, "metadata": meta}
                    for doc, meta in zip(
                        r["documents"][0],
                        r["metadatas"][0]
                    )
                ]
        except Exception:
            pass
        return []

    # ── Context builder ────────────────────────────────────────

    def build_context(self, query: str) -> str:
        """
        Build a memory context string to prepend to 
        the system prompt. Searches all collections 
        and formats relevant memories.
        """
        results = self.search(query, n=5)
        if not results:
            return ""

        lines = ["[RELEVANT MEMORIES]"]
        for r in results:
            meta = r["metadata"]
            ts   = meta.get("ts", "")[:10]
            typ  = meta.get("type", "")

            if typ == "message":
                role = meta.get("role", "")
                lines.append(
                    f"• [{ts}] {role}: {r['content'][:200]}")
            elif typ == "action":
                action  = meta.get("action", "")
                success = meta.get("success", "")
                lines.append(
                    f"• [{ts}] {action} "
                    f"({'✓' if success=='True' else '✗'}): "
                    f"{r['content'][:200]}")
            elif typ == "knowledge":
                lines.append(
                    f"• [{ts}] KNOWN: {r['content'][:200]}")

        lines.append("[END MEMORIES]\n")
        return "\n".join(lines)

    # ── Stats ──────────────────────────────────────────────────

    def stats(self) -> dict:
        return {
            "conversations": self.conversations.count(),
            "actions":       self.actions.count(),
            "knowledge":     self.knowledge.count(),
            "db_path":       DB_PATH
        }

    def clear_tab(self):
        """Clear all memories for this tab."""
        for collection in [self.conversations,
                           self.actions,
                           self.knowledge]:
            try:
                results = collection.get(
                    where={"tab_id": self.tab_id})
                if results["ids"]:
                    collection.delete(ids=results["ids"])
            except Exception:
                pass
