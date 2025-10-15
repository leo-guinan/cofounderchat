# Possible Futures System

## Overview

The Possible Futures system allows an AI model to spawn, explore, and validate "ideas" - hypothetical future states of systems that might be built. Each idea evolves through a structured waterfall process while maintaining uncertainty in requirements.

## Architecture

Based on "Out of the Tar Pit" paper principles:

### Core Principles

1. **Separation of Concerns**
   - **Essential State**: What the system IS (ideas, components, assumptions, goals)
   - **Essential Logic**: Pure functions that derive new knowledge from state
   - **Accidental State**: How we store and index (SQLite, FTS, etc.)

2. **Event Sourcing**
   - Each waterfall stage has its own SQLite database
   - State = f(initial_state, changes)
   - All changes are immutable events
   - Can reconstruct any historical state

3. **Relational Model**
   - All data stored as relations (tables)
   - No hidden state or access paths
   - Clear integrity constraints

## Components

### 1. Ideas (Possible Futures)

```python
@dataclass
class Idea:
    id: str
    name: str
    description: str
    current_stage: WaterfallStage  # requirements → deployment
    uncertainty_level: UncertaintyLevel  # decreases as validation happens
    parent_idea_id: Optional[str]  # for branching futures
```

**Idea Properties:**
- Can branch from other ideas (exploring alternatives)
- Progress through waterfall stages
- Uncertainty decreases as assumptions are validated
- Health score computed from knowledge, assumptions, goals

### 2. System Knowledge

Known parts of the system being built:

```python
@dataclass
class SystemKnowledge:
    component_name: str  # e.g., "user_auth_api"
    component_type: str  # api, database, ui, business_logic
    specification: Dict[str, Any]  # Detailed spec
    confidence: float  # 0.0 to 1.0
```

### 3. World Assumptions

Hypotheses about the environment that need validation:

```python
@dataclass
class WorldAssumption:
    assumption_text: str
    category: str  # user_behavior, market, technology, regulations, resources
    criticality: float  # 0.0 to 1.0
    validated: bool
    validation_evidence: Optional[str]
```

**Critical Assumptions:**
- Criticality > 0.7 must be validated before stage advancement
- At least 80% of critical assumptions must be validated
- Drives uncertainty calculation

### 4. Goals

Measurable outcomes to achieve:

```python
@dataclass
class Goal:
    goal_text: str
    metric_name: str
    target_value: Any
    current_value: Optional[Any]
    status: GoalStatus  # not_started, in_progress, achieved, failed
    validator_function: str  # Name of validator
```

**Built-in Validators:**
- `numeric_threshold`: Check if metric >= target
- `percentage`: Check if percentage >= target
- `boolean`: Check if condition is true
- `list_length`: Check if list has >= N items

### 5. Waterfall Stages

```
REQUIREMENTS → ANALYSIS → DESIGN → IMPLEMENTATION → TESTING → VALIDATION → DEPLOYMENT
```

Each stage has:
- Its own SQLite database
- Event-sourced state management
- Initial state + changes = current state
- Can be queried for full history

## Tools API for AI Models

### Creating Ideas

```python
create_idea(
    name="Sustainable Fashion Marketplace",
    description="Marketplace connecting conscious consumers...",
    parent_idea_id=None  # Optional: branch from existing idea
)
# Returns: {"id": "abc123", "name": "...", "current_stage": "requirements", ...}
```

### Adding System Components

```python
add_system_component(
    idea_id="abc123",
    component_name="product_catalog",
    component_type="database",
    specification={
        "type": "PostgreSQL",
        "schema": {...}
    },
    confidence=0.9
)
```

### Adding Assumptions

```python
add_world_assumption(
    idea_id="abc123",
    assumption_text="Users will pay 20% premium for sustainable products",
    category="market",
    criticality=0.9  # CRITICAL assumption
)
```

### Adding Goals

```python
add_goal(
    idea_id="abc123",
    goal_text="Achieve 10,000 active users within 6 months",
    metric_name="active_users_6mo",
    target_value=10000,
    validator_function="numeric_threshold"
)
```

### Validating Goals

```python
check_goals(
    idea_id="abc123",
    current_metrics={
        "active_users_6mo": 8500,
        "customer_satisfaction_pct": 87.5
    }
)
# Returns: {"goal_text": {"passed": False, "actual_value": 8500, "message": "..."}}
```

### Getting Idea Status

```python
get_idea_status(idea_id="abc123")
# Returns:
# {
#   "idea": {...},
#   "health": {
#     "total_knowledge_items": 5,
#     "average_confidence": 0.85,
#     "total_assumptions": 4,
#     "validated_assumptions": 2,
#     "assumption_validation_rate": 0.5,
#     "total_goals": 3,
#     "achieved_goals": 1,
#     "overall_health_score": 0.72
#   }
# }
```

### Advancing Stages

```python
advance_idea_stage(idea_id="abc123")
# Returns: {"success": False, "message": "Cannot advance - critical assumptions not validated"}
```

**Stage Advancement Requirements:**
- Must have at least 1 knowledge component
- 80%+ of critical assumptions must be validated
- Automatically updates uncertainty level

### Viewing History (Event Sourcing)

```python
get_stage_history(idea_id="abc123", stage="requirements")
# Returns:
# {
#   "initial_state": {...},
#   "changes": [
#     {"change_id": "...", "timestamp": "...", "change_type": "knowledge_added", "change_data": {...}},
#     ...
#   ],
#   "current_state": {...}  # Computed from initial + changes
# }
```

## Database Schema

Each idea has 7 SQLite databases (one per waterfall stage):

```
./data/possible_futures/
  {idea_id}_requirements.db
  {idea_id}_analysis.db
  {idea_id}_design.db
  {idea_id}_implementation.db
  {idea_id}_testing.db
  {idea_id}_validation.db
  {idea_id}_deployment.db
```

**Tables in each stage DB:**

```sql
-- Initial state snapshot
CREATE TABLE initial_state (
    idea_id TEXT PRIMARY KEY,
    stage TEXT NOT NULL,
    state_data TEXT NOT NULL,  -- JSON
    state_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

-- All changes (events)
CREATE TABLE state_changes (
    change_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    change_type TEXT NOT NULL,
    change_data TEXT NOT NULL,  -- JSON
    previous_state_hash TEXT NOT NULL,
    new_state_hash TEXT NOT NULL
);

-- Current stage data
CREATE TABLE system_knowledge (...);
CREATE TABLE world_assumptions (...);
CREATE TABLE goals (...);
```

## Knowledge Base Integration

System for collecting your content for training:

### Content Types

- **Essays**: Long-form writing
- **Conversations**: Chat/dialogue examples
- **Frameworks**: Structured methodologies
- **Examples**: Code/implementation examples
- **Principles**: Core concepts
- **Stories**: Narratives and case studies
- **Validation Data**: Test/validation datasets

### Ingesting Content

```python
from tasks.knowledge_base import setup_knowledge_base, ContentIngester, ContentType

# Initialize
store = setup_knowledge_base("./data/knowledge_base.db")
ingester = ContentIngester(store)

# Ingest markdown files
ingester.ingest_markdown_file("essay.md", ContentType.ESSAY)

# Ingest directory
ingester.ingest_directory("./content", ContentType.FRAMEWORK, pattern="*.md")

# Ingest existing validation data
ingester.ingest_existing_validation_data()
```

### Training Data Export

```python
# Export as JSONL for fine-tuning
store.export_training_data("training.jsonl", format="jsonl")

# Export as JSON for general use
store.export_training_data("training.json", format="json")
```

**Output Format (JSONL):**
```json
{"prompt": "Explain: Managing Complexity", "completion": "...", "metadata": {...}}
{"prompt": "What is FRP?", "completion": "...", "metadata": {...}}
```

## Usage Examples

### Example 1: E-Commerce Platform

See `tasks/example_possible_futures.py` for complete example:

```python
# 1. Spawn idea
idea = create_idea(
    name="Sustainable Fashion Marketplace",
    description="..."
)

# 2. Add system components
add_system_component(idea_id, "product_catalog", "database", {...})
add_system_component(idea_id, "user_profiles", "api", {...})
add_system_component(idea_id, "sustainability_scoring", "business_logic", {...})

# 3. Add assumptions
add_world_assumption(idea_id, "Consumers will pay premium", "market", 0.9)
add_world_assumption(idea_id, "Brands will integrate via API", "technology", 0.7)

# 4. Add goals
add_goal(idea_id, "10K users in 6mo", "active_users_6mo", 10000, "numeric_threshold")
add_goal(idea_id, "85% satisfaction", "satisfaction_pct", 85.0, "percentage")

# 5. Check status
status = get_idea_status(idea_id)
# Health score: 0.72, Uncertainty: VERY_HIGH

# 6. Try to advance (will fail - need validation)
advance_idea_stage(idea_id)
# "Cannot advance - critical assumptions not validated"
```

### Example 2: Branching Ideas

```python
# Base idea
base = create_idea("SaaS Analytics Platform", "...")

# Branch 1: Self-hosted version
branch1 = create_idea(
    "SaaS Analytics - Self-Hosted",
    "For enterprises with strict data requirements",
    parent_idea_id=base['id']
)

# Branch 2: Fully managed
branch2 = create_idea(
    "SaaS Analytics - Fully Managed",
    "Cloud service with AI insights",
    parent_idea_id=base['id']
)

# Now you have 3 parallel futures to explore
```

## Integration with Training

### During Training

Add these tools to your model's tool set:

```python
from tasks.idea_tools import TOOL_MANIFEST

tools = TOOL_MANIFEST  # All available tools for the model
```

### Post-Training Usage

The trained model can:

1. **Spawn ideas** in response to user problems
2. **Decompose** ideas into system components
3. **Identify assumptions** that need validation
4. **Set measurable goals** for success
5. **Track progress** through waterfall stages
6. **Branch ideas** to explore alternatives
7. **Validate** using built-in validators

### Prompt Template

```
You have access to tools for spawning and managing "possible future" ideas.

When a user describes a problem or opportunity:
1. Use create_idea() to spawn a possible future
2. Use add_system_component() to define known parts
3. Use add_world_assumption() to identify critical hypotheses
4. Use add_goal() to set measurable success criteria
5. Use get_idea_status() to check health
6. Use advance_idea_stage() to progress through waterfall

Remember:
- Uncertainty is GOOD early on - don't over-specify
- Critical assumptions (>0.7) MUST be validated before advancing
- Goals should be MEASURABLE with clear validators
- Branch ideas to explore alternative approaches
```

## Benefits

### For the AI Model

- **Structured thinking**: Forces decomposition of vague ideas into components
- **Uncertainty management**: Explicit tracking of what's known vs. assumed
- **Goal orientation**: Every idea has measurable success criteria
- **Exploration**: Can spawn multiple alternatives and compare
- **Memory**: Full event history preserved for learning

### For Users

- **Transparency**: See exactly what assumptions the AI is making
- **Validation**: Know which assumptions need real-world testing
- **Progress tracking**: Clear view of idea maturity
- **Risk management**: Understand uncertainty at each stage
- **Decision support**: Compare multiple possible futures

### For the System

- **Simplicity**: FRP architecture minimizes complexity
- **Auditability**: Every change is logged
- **Reproducibility**: Can replay any idea's evolution
- **Testability**: Pure functions, no hidden state
- **Scalability**: SQLite per idea, no single bottleneck

## Advanced Features

### Custom Validators

Register your own goal validators:

```python
from tasks.possible_futures import get_engine

def custom_validator(target_value, context):
    # Your validation logic
    actual = context.get("my_metric")
    passed = actual >= target_value
    return ValidatorResult(passed, actual, "...")

engine = get_engine()
engine.validator.register("custom_validator", custom_validator)
```

### Querying State

Direct SQL access to any stage:

```python
import sqlite3
conn = sqlite3.connect("./data/possible_futures/{idea_id}_requirements.db")
cursor = conn.cursor()

# Get all critical assumptions
cursor.execute("""
    SELECT assumption_text, validated
    FROM world_assumptions
    WHERE criticality > 0.7
""")
```

### Exporting Ideas

```python
# Get complete idea as JSON
status = get_idea_status(idea_id)
history = get_stage_history(idea_id, "requirements")

export_data = {
    "idea": status['idea'],
    "health": status['health'],
    "history": history
}

import json
with open("idea_export.json", "w") as f:
    json.dump(export_data, f, indent=2)
```

## File Structure

```
tasks/
  possible_futures.py        # Core data models and engine
  idea_tools.py              # Tools API for AI models
  knowledge_base.py          # Content ingestion for training
  example_possible_futures.py  # Usage examples

data/
  possible_futures/          # Idea databases
    {idea_id}_requirements.db
    {idea_id}_analysis.db
    ...
  knowledge_base.db          # Training content database
```

## Next Steps

1. **Ingest your content** into knowledge base
2. **Export training data** in JSONL format
3. **Train model** with idea tools available
4. **Test model** spawning and managing ideas
5. **Integrate** into your application workflow

## Philosophy

This system embodies "Out of the Tar Pit" principles:

- **Avoid complexity** by separating essential from accidental
- **Avoid state** by using pure functions where possible
- **Separate** state, logic, and control completely
- **Use relations** for all data (no hidden structures)
- **Event source** for perfect auditability
- **Maintain uncertainty** explicitly rather than pretending certainty

The goal: **Let the AI think clearly about messy, uncertain futures without drowning in accidental complexity.**

