# Quick Start: Possible Futures System

## What You Just Got

A complete system for your AI model to spawn, explore, and validate "possible futures" - hypothetical systems that might be built. Based on "Out of the Tar Pit" principles for managing complexity.

## File Structure

```
tasks/
  possible_futures.py         # Core: Data models, engine, event sourcing
  idea_tools.py               # Tools API for your trained model
  knowledge_base.py           # Content ingestion for training data
  example_possible_futures.py # Working examples

scripts/
  prepare_futures_training.py # Script to prepare training data

data/
  possible_futures/           # SQLite DBs (one per idea, per stage)
  knowledge_base.db           # Training content database

POSSIBLE_FUTURES.md           # Complete documentation
QUICKSTART_FUTURES.md         # This file
```

## Test It Now

```bash
# Run the examples
python -m tasks.example_possible_futures

# This will:
# - Spawn an e-commerce idea
# - Add components, assumptions, goals
# - Try to advance through waterfall (will fail - needs validation)
# - Create branching ideas
# - Show event-sourced history
```

## Prepare Training Data

```bash
# Ingest your content and generate training examples
python scripts/prepare_futures_training.py

# This creates:
# - data/possible_futures_training.jsonl (for fine-tuning)
# - data/possible_futures_training.json (for inspection)
```

## Key Concepts

### 1. Ideas Are Possible Futures

```python
idea = create_idea(
    name="Freelance Designer Platform",
    description="Platform connecting designers with clients"
)
```

Each idea:
- Has a unique ID
- Progresses through waterfall stages (requirements → deployment)
- Tracks uncertainty (decreases as assumptions validated)
- Can branch to explore alternatives

### 2. Three Types of Content

**System Knowledge** - What we KNOW about the system:
```python
add_system_component(
    idea_id, 
    "portfolio_hosting", 
    "ui",
    {"features": ["image_upload", "showcase"]},
    confidence=0.85
)
```

**World Assumptions** - What we're ASSUMING (needs validation):
```python
add_world_assumption(
    idea_id,
    "Designers will pay $20/mo for premium",
    category="market",
    criticality=0.9  # Must validate before advancing!
)
```

**Goals** - What we want to ACHIEVE (measurable):
```python
add_goal(
    idea_id,
    "1000 designers in 3 months",
    metric_name="designer_signups_3mo",
    target_value=1000,
    validator_function="numeric_threshold"
)
```

### 3. Waterfall With Explicit Uncertainty

```
REQUIREMENTS (uncertainty: very_high)
    ↓ [80% critical assumptions validated]
ANALYSIS (uncertainty: high)
    ↓
DESIGN (uncertainty: medium)
    ↓
... → DEPLOYMENT (uncertainty: minimal)
```

Can't advance until assumptions are validated. Forces real validation, not just optimism.

### 4. Event Sourcing

Every change is recorded:
```
State = f(initial_state, all_changes)
```

You can query complete history:
```python
history = get_stage_history(idea_id, "requirements")
# Shows: initial state, all changes, current state
```

### 5. Health Metrics (Derived, Not Stored)

```python
status = get_idea_status(idea_id)
# Returns:
# - Knowledge items count
# - Average confidence
# - Assumption validation rate
# - Goal achievement rate
# - Overall health score (0-1)
```

## Integration With Your Training

### Option A: Add to Existing Training

```python
# In your training script
from tasks.idea_tools import TOOL_MANIFEST

# Make tools available to model
tools = TOOL_MANIFEST

# Train with tool-augmented examples from:
# data/possible_futures_training.jsonl
```

### Option B: Fine-Tune Specifically

```python
# Use the generated training data
training_data = "data/possible_futures_training.jsonl"

# Each example shows tool usage:
# {"prompt": "I want to build X", "completion": "Let me spawn an idea..."}
```

### After Training

Your model can now:

1. **Listen** to user problems
2. **Spawn** ideas with `create_idea()`
3. **Decompose** into components with `add_system_component()`
4. **Identify** critical assumptions with `add_world_assumption()`
5. **Set** measurable goals with `add_goal()`
6. **Validate** progress with `check_goals()`
7. **Branch** to explore alternatives
8. **Track** health with `get_idea_status()`

## Example Interaction

**User:** "I want to build a platform for sustainable fashion"

**AI Model:**
```python
# Spawn the idea
idea = create_idea(
    name="Sustainable Fashion Marketplace",
    description="..."
)

# Add what we know
add_system_component(idea_id, "product_catalog", "database", {...}, 0.9)

# Identify critical assumptions
add_world_assumption(
    idea_id,
    "Consumers will pay 20% premium for sustainability",
    "market",
    0.95  # CRITICAL
)

# Set measurable goals
add_goal(
    idea_id,
    "10K users in 6 months",
    "active_users_6mo",
    10000,
    "numeric_threshold"
)

# Check status
status = get_idea_status(idea_id)
```

**AI to User:** "I've created a possible future for your platform. Current health: 0.25 (low because assumptions aren't validated yet). You have 1 CRITICAL assumption that needs validation: 'Consumers will pay 20% premium'. Before we can progress past requirements, you need to validate this with real data."

## Advanced Features

### Branching Ideas

```python
base = create_idea("Food Delivery", "...")

# Explore two approaches
restaurant_model = create_idea(
    "Food Delivery - Restaurant Partnership",
    "...",
    parent_idea_id=base['id']
)

dark_kitchen_model = create_idea(
    "Food Delivery - Dark Kitchen",
    "...",
    parent_idea_id=base['id']
)

# Compare health scores
status1 = get_idea_status(restaurant_model['id'])
status2 = get_idea_status(dark_kitchen_model['id'])
```

### Custom Validators

```python
from tasks.possible_futures import get_engine, ValidatorResult

def roi_validator(target_roi, context):
    revenue = context.get("revenue")
    cost = context.get("cost")
    roi = (revenue - cost) / cost if cost > 0 else 0
    passed = roi >= target_roi
    return ValidatorResult(passed, roi, f"ROI: {roi:.2%}")

engine = get_engine()
engine.validator.register("roi", roi_validator)

# Now use it
add_goal(idea_id, "Achieve 300% ROI", "roi", 3.0, "roi")
```

### Query Event History

```python
import sqlite3

# Direct SQL access
conn = sqlite3.connect(f"data/possible_futures/{idea_id}_requirements.db")
cursor = conn.cursor()

# All critical unvalidated assumptions
cursor.execute("""
    SELECT assumption_text, category
    FROM world_assumptions
    WHERE criticality > 0.7 AND validated = 0
""")

for text, category in cursor.fetchall():
    print(f"Need to validate ({category}): {text}")
```

## Why This Matters

### Problem: Vague Ideas Fail

Users say "I want to build X" but have:
- No clear components
- Unvalidated assumptions
- No measurable goals
- False certainty

### Solution: Explicit Uncertainty

This system forces:
- ✓ Decomposition into components
- ✓ Identification of assumptions
- ✓ Measurable success criteria
- ✓ Can't advance without validation
- ✓ Uncertainty tracked explicitly

### Result: Better Outcomes

- Ideas that advance are stronger (assumptions validated)
- Users know what to test (critical assumptions flagged)
- Progress is measurable (goal validators)
- Can explore alternatives (branching)
- Full audit trail (event sourcing)

## Next Steps

1. **Run the examples** to see it work
   ```bash
   python -m tasks.example_possible_futures
   ```

2. **Prepare your training data**
   ```bash
   python scripts/prepare_futures_training.py
   ```

3. **Review the generated data**
   ```bash
   cat data/possible_futures_training.json | jq '.[0]'
   ```

4. **Integrate with your training**
   - Add tools to model context
   - Include generated training examples
   - Test with new prompts

5. **Read full docs**
   - `POSSIBLE_FUTURES.md` - Complete documentation
   - `tasks/possible_futures.py` - Core implementation
   - `tasks/idea_tools.py` - Tools API

## Architecture Principles (From "Out of the Tar Pit")

✓ **Separation**: Essential state | Essential logic | Accidental state
✓ **Relational**: All data as relations (SQLite tables)
✓ **Event Sourcing**: State = f(initial, changes)
✓ **Pure Functions**: Logic is referentially transparent
✓ **No Hidden State**: Everything queryable
✓ **Avoid Complexity**: Only essential complexity remains

The system embodies the paper's principles perfectly.

## Questions?

See `POSSIBLE_FUTURES.md` for complete documentation, or explore the code:
- Core engine: `tasks/possible_futures.py`
- Tools API: `tasks/idea_tools.py`
- Examples: `tasks/example_possible_futures.py`

All TODOs complete! The system is ready to use.

