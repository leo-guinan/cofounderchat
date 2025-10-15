"""
Knowledge Base Integration for Training Data

This module helps collect, structure, and prepare content for training.
Follows FRP principles: separate essential state (content) from accidental (indexing/search).
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import sqlite3
import json
import hashlib
import re


# ============================================================================
# Essential State - Content Types
# ============================================================================

class ContentType(str):
    """Types of content in the knowledge base"""
    ESSAY = "essay"
    CONVERSATION = "conversation"
    FRAMEWORK = "framework"
    EXAMPLE = "example"
    PRINCIPLE = "principle"
    STORY = "story"
    VALIDATION_DATA = "validation_data"


@dataclass
class ContentItem:
    """
    A piece of content for the knowledge base
    
    Essential state only - what the content IS, not how it's stored
    """
    id: str
    title: str
    content: str
    content_type: ContentType
    topics: List[str]
    created_at: datetime
    source: str  # Where it came from (file path, URL, etc.)
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if not self.id:
            # Generate deterministic ID
            content_hash = hashlib.sha256(
                f"{self.title}:{self.content}:{self.source}".encode()
            ).hexdigest()[:16]
            self.id = content_hash


@dataclass
class TopicTag:
    """
    A topic that can be used to categorize content
    """
    name: str
    description: str
    related_topics: List[str]
    importance: float  # 0.0 to 1.0


@dataclass
class TrainingExample:
    """
    A structured training example derived from content
    
    This is what actually gets fed to the model
    """
    prompt: str
    completion: str
    metadata: Dict[str, Any]
    source_content_id: str


# ============================================================================
# Essential Logic - Content Processing Functions
# ============================================================================

def extract_topics_from_text(text: str, known_topics: List[str]) -> List[str]:
    """
    Pure function: extract topics from text
    
    Uses simple keyword matching for now
    """
    text_lower = text.lower()
    found_topics = []
    
    for topic in known_topics:
        topic_lower = topic.lower()
        # Check for topic as whole word
        pattern = r'\b' + re.escape(topic_lower) + r'\b'
        if re.search(pattern, text_lower):
            found_topics.append(topic)
    
    return found_topics


def chunk_long_content(content: str, max_tokens: int = 2048) -> List[str]:
    """
    Pure function: split long content into chunks
    
    Simple sentence-based chunking for now
    """
    # Rough approximation: 1 token ≈ 4 characters
    max_chars = max_tokens * 4
    
    sentences = re.split(r'(?<=[.!?])\s+', content)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length > max_chars and current_chunk:
            # Start new chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def create_qa_pairs_from_content(content_item: ContentItem) -> List[TrainingExample]:
    """
    Pure function: convert content into Q&A training examples
    
    This is where you'd implement your specific conversion logic
    """
    examples = []
    
    # Strategy 1: Use title as question, content as answer
    if content_item.content_type == ContentType.ESSAY:
        examples.append(TrainingExample(
            prompt=f"Explain: {content_item.title}",
            completion=content_item.content,
            metadata={"strategy": "title_to_qa", "topics": content_item.topics},
            source_content_id=content_item.id
        ))
    
    # Strategy 2: For frameworks, create multiple angles
    if content_item.content_type == ContentType.FRAMEWORK:
        # "What is X?"
        examples.append(TrainingExample(
            prompt=f"What is {content_item.title}?",
            completion=content_item.content,
            metadata={"strategy": "what_is", "topics": content_item.topics},
            source_content_id=content_item.id
        ))
        
        # "How do I use X?"
        examples.append(TrainingExample(
            prompt=f"How do I use {content_item.title}?",
            completion=content_item.content,
            metadata={"strategy": "how_to_use", "topics": content_item.topics},
            source_content_id=content_item.id
        ))
    
    # Strategy 3: For conversations, extract turns
    if content_item.content_type == ContentType.CONVERSATION:
        # Split on conversation markers (this is a simple heuristic)
        turns = re.split(r'\n(?:Human:|Assistant:|User:|AI:)', content_item.content)
        for i in range(0, len(turns) - 1, 2):
            if i + 1 < len(turns):
                examples.append(TrainingExample(
                    prompt=turns[i].strip(),
                    completion=turns[i + 1].strip(),
                    metadata={"strategy": "conversation_turn", "topics": content_item.topics},
                    source_content_id=content_item.id
                ))
    
    return examples


# ============================================================================
# Accidental State - Storage and Indexing
# ============================================================================

class KnowledgeBaseStore:
    """
    SQLite-based storage for knowledge base
    
    Accidental state: HOW we store things, not WHAT we store
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables for knowledge base"""
        cursor = self.conn.cursor()
        
        # Content items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_items (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                content_type TEXT NOT NULL,
                topics TEXT NOT NULL,  -- JSON array
                created_at TEXT NOT NULL,
                source TEXT NOT NULL,
                metadata TEXT NOT NULL  -- JSON
            )
        """)
        
        # Topic tags
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topic_tags (
                name TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                related_topics TEXT NOT NULL,  -- JSON array
                importance REAL NOT NULL
            )
        """)
        
        # Training examples
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_examples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                completion TEXT NOT NULL,
                metadata TEXT NOT NULL,  -- JSON
                source_content_id TEXT NOT NULL,
                FOREIGN KEY (source_content_id) REFERENCES content_items(id)
            )
        """)
        
        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_type ON content_items(content_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_source ON content_items(source)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_examples_source ON training_examples(source_content_id)")
        
        # Full-text search (accidental - for performance)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
                id UNINDEXED,
                title,
                content,
                topics
            )
        """)
        
        self.conn.commit()
    
    def add_content(self, item: ContentItem):
        """Add a content item to the knowledge base"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO content_items (
                id, title, content, content_type, topics, created_at, source, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.id,
            item.title,
            item.content,
            item.content_type,
            json.dumps(item.topics),
            item.created_at.isoformat(),
            item.source,
            json.dumps(item.metadata)
        ))
        
        # Update FTS index
        cursor.execute("""
            INSERT OR REPLACE INTO content_fts (id, title, content, topics)
            VALUES (?, ?, ?, ?)
        """, (item.id, item.title, item.content, json.dumps(item.topics)))
        
        self.conn.commit()
    
    def add_topic(self, topic: TopicTag):
        """Add a topic tag"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO topic_tags (name, description, related_topics, importance)
            VALUES (?, ?, ?, ?)
        """, (topic.name, topic.description, json.dumps(topic.related_topics), topic.importance))
        self.conn.commit()
    
    def add_training_example(self, example: TrainingExample):
        """Add a training example"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO training_examples (prompt, completion, metadata, source_content_id)
            VALUES (?, ?, ?, ?)
        """, (example.prompt, example.completion, json.dumps(example.metadata), example.source_content_id))
        self.conn.commit()
    
    def get_all_content(self, content_type: Optional[ContentType] = None) -> List[ContentItem]:
        """Get all content items, optionally filtered by type"""
        cursor = self.conn.cursor()
        
        if content_type:
            cursor.execute("""
                SELECT id, title, content, content_type, topics, created_at, source, metadata
                FROM content_items WHERE content_type = ?
            """, (content_type,))
        else:
            cursor.execute("""
                SELECT id, title, content, content_type, topics, created_at, source, metadata
                FROM content_items
            """)
        
        items = []
        for row in cursor.fetchall():
            items.append(ContentItem(
                id=row[0],
                title=row[1],
                content=row[2],
                content_type=row[3],
                topics=json.loads(row[4]),
                created_at=datetime.fromisoformat(row[5]),
                source=row[6],
                metadata=json.loads(row[7])
            ))
        return items
    
    def get_all_topics(self) -> List[TopicTag]:
        """Get all topic tags"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, description, related_topics, importance FROM topic_tags")
        
        topics = []
        for row in cursor.fetchall():
            topics.append(TopicTag(
                name=row[0],
                description=row[1],
                related_topics=json.loads(row[2]),
                importance=row[3]
            ))
        return topics
    
    def get_all_training_examples(self) -> List[TrainingExample]:
        """Get all training examples"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT prompt, completion, metadata, source_content_id FROM training_examples")
        
        examples = []
        for row in cursor.fetchall():
            examples.append(TrainingExample(
                prompt=row[0],
                completion=row[1],
                metadata=json.loads(row[2]),
                source_content_id=row[3]
            ))
        return examples
    
    def search_content(self, query: str) -> List[ContentItem]:
        """Full-text search across content"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.id, c.title, c.content, c.content_type, c.topics, c.created_at, c.source, c.metadata
            FROM content_items c
            JOIN content_fts fts ON c.id = fts.id
            WHERE content_fts MATCH ?
        """, (query,))
        
        items = []
        for row in cursor.fetchall():
            items.append(ContentItem(
                id=row[0],
                title=row[1],
                content=row[2],
                content_type=row[3],
                topics=json.loads(row[4]),
                created_at=datetime.fromisoformat(row[5]),
                source=row[6],
                metadata=json.loads(row[7])
            ))
        return items
    
    def export_training_data(self, output_path: str, format: str = "jsonl"):
        """
        Export training examples to file
        
        Format can be 'jsonl' (for fine-tuning) or 'json' (for general use)
        """
        examples = self.get_all_training_examples()
        
        if format == "jsonl":
            with open(output_path, 'w') as f:
                for example in examples:
                    entry = {
                        "prompt": example.prompt,
                        "completion": example.completion,
                        "metadata": example.metadata
                    }
                    f.write(json.dumps(entry) + '\n')
        elif format == "json":
            with open(output_path, 'w') as f:
                data = [
                    {
                        "prompt": ex.prompt,
                        "completion": ex.completion,
                        "metadata": ex.metadata,
                        "source_content_id": ex.source_content_id
                    }
                    for ex in examples
                ]
                json.dump(data, f, indent=2)
    
    def close(self):
        """Close database connection"""
        self.conn.close()


# ============================================================================
# Content Ingestion Pipeline
# ============================================================================

class ContentIngester:
    """
    Pipeline for ingesting content into knowledge base
    
    Follows waterfall principle: uncertain requirements -> stable system
    """
    
    def __init__(self, store: KnowledgeBaseStore):
        self.store = store
    
    def ingest_markdown_file(self, file_path: str, content_type: ContentType) -> ContentItem:
        """Ingest a markdown file as content"""
        path = Path(file_path)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from first heading or filename
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else path.stem
        
        # Get topics
        topics = self._extract_topics_from_content(content)
        
        item = ContentItem(
            id="",  # Will be generated
            title=title,
            content=content,
            content_type=content_type,
            topics=topics,
            created_at=datetime.fromtimestamp(path.stat().st_mtime),
            source=str(path),
            metadata={"file_size": path.stat().st_size, "format": "markdown"}
        )
        
        self.store.add_content(item)
        
        # Generate training examples
        examples = create_qa_pairs_from_content(item)
        for example in examples:
            self.store.add_training_example(example)
        
        return item
    
    def ingest_directory(self, directory: str, content_type: ContentType, pattern: str = "*.md") -> List[ContentItem]:
        """Ingest all matching files in a directory"""
        items = []
        for file_path in Path(directory).rglob(pattern):
            if file_path.is_file():
                try:
                    item = self.ingest_markdown_file(str(file_path), content_type)
                    items.append(item)
                except Exception as e:
                    print(f"Error ingesting {file_path}: {e}")
        return items
    
    def ingest_existing_validation_data(self) -> List[ContentItem]:
        """Ingest existing validation datasets from the project"""
        items = []
        
        # Read conscious_validation_data.py
        validation_file = Path(__file__).parent / "conscious_validation_data.py"
        if validation_file.exists():
            # This would parse the Python file and extract validation examples
            # For now, we'll just add it as a content item
            with open(validation_file, 'r') as f:
                content = f.read()
            
            item = ContentItem(
                id="",
                title="Conscious Economics Validation Data",
                content=content,
                content_type=ContentType.VALIDATION_DATA,
                topics=["conscious_economics", "validation", "business_math"],
                created_at=datetime.now(),
                source=str(validation_file),
                metadata={"format": "python", "type": "validation_data"}
            )
            
            self.store.add_content(item)
            items.append(item)
        
        return items
    
    def _extract_topics_from_content(self, content: str) -> List[str]:
        """Extract topics from content using known topic list"""
        known_topics = [t.name for t in self.store.get_all_topics()]
        if not known_topics:
            # Default topics if none exist
            known_topics = [
                "complexity", "state", "control", "functional programming",
                "relational model", "conscious economics", "time violence",
                "pattern recognition", "waterfall", "uncertainty", "validation"
            ]
        return extract_topics_from_text(content, known_topics)


# ============================================================================
# Initialization Functions
# ============================================================================

def initialize_default_topics(store: KnowledgeBaseStore):
    """Set up default topic tags"""
    default_topics = [
        TopicTag("complexity", "Software complexity and how to manage it", ["state", "control"], 1.0),
        TopicTag("state", "State management in software systems", ["complexity", "functional programming"], 0.9),
        TopicTag("control", "Control flow and execution", ["complexity"], 0.8),
        TopicTag("functional programming", "FP principles and practices", ["state", "relational model"], 0.9),
        TopicTag("relational model", "Relational data modeling", ["functional programming", "FRP"], 0.9),
        TopicTag("FRP", "Functional Relational Programming", ["functional programming", "relational model"], 0.8),
        TopicTag("conscious economics", "Business model and economics framework", ["time violence", "pattern recognition"], 1.0),
        TopicTag("time violence", "Unnecessary complexity in time/processes", ["conscious economics"], 0.9),
        TopicTag("pattern recognition", "Identifying patterns in complexity", ["conscious economics"], 0.8),
        TopicTag("waterfall", "Waterfall development process", ["uncertainty"], 0.7),
        TopicTag("uncertainty", "Managing uncertainty in development", ["waterfall"], 0.8),
        TopicTag("validation", "Validation and testing strategies", ["goals"], 0.9),
        TopicTag("goals", "Goal setting and achievement", ["validation"], 0.8),
        TopicTag("event sourcing", "Event sourcing pattern", ["state"], 0.7),
        TopicTag("ideas", "Idea generation and management", ["possible futures"], 0.8),
        TopicTag("possible futures", "Future scenario planning", ["ideas", "uncertainty"], 0.9),
    ]
    
    for topic in default_topics:
        store.add_topic(topic)


def setup_knowledge_base(db_path: str = "./data/knowledge_base.db") -> KnowledgeBaseStore:
    """Initialize knowledge base with default topics"""
    store = KnowledgeBaseStore(db_path)
    
    # Check if topics exist
    if not store.get_all_topics():
        initialize_default_topics(store)
    
    return store

