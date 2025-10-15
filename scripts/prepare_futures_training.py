#!/usr/bin/env python3
"""
Prepare training data combining your content with Possible Futures tools

This script:
1. Ingests your existing content into the knowledge base
2. Generates training examples
3. Adds tool usage examples
4. Exports combined dataset for training
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tasks.knowledge_base import (
    setup_knowledge_base,
    ContentIngester,
    ContentType,
    ContentItem
)
from tasks.idea_tools import TOOL_MANIFEST
from datetime import datetime
import json


def ingest_project_content():
    """Ingest all your existing content"""
    print("=" * 80)
    print("STEP 1: Ingesting Existing Content")
    print("=" * 80)
    
    # Initialize knowledge base
    db_path = "./data/knowledge_base.db"
    os.makedirs("./data", exist_ok=True)
    store = setup_knowledge_base(db_path)
    ingester = ContentIngester(store)
    
    items_ingested = []
    
    # 1. Ingest markdown documentation
    print("\n1. Ingesting markdown documentation...")
    markdown_files = [
        ("./CONSCIOUS_ECONOMICS.md", ContentType.FRAMEWORK),
        ("./SALES_PITCH.md", ContentType.FRAMEWORK),
        ("./VALIDATION_DATASET.md", ContentType.VALIDATION_DATA),
        ("./README.md", ContentType.FRAMEWORK),
    ]
    
    for file_path, content_type in markdown_files:
        if Path(file_path).exists():
            try:
                item = ingester.ingest_markdown_file(file_path, content_type)
                items_ingested.append(item)
                print(f"  ✓ {file_path}")
            except Exception as e:
                print(f"  ✗ {file_path}: {e}")
    
    # 2. Ingest validation data
    print("\n2. Ingesting validation data...")
    validation_items = ingester.ingest_existing_validation_data()
    items_ingested.extend(validation_items)
    print(f"  ✓ Ingested {len(validation_items)} validation items")
    
    # 3. Add tool documentation as content
    print("\n3. Adding tool documentation...")
    tools_content = ContentItem(
        id="",
        title="Possible Futures Tools API",
        content=json.dumps(TOOL_MANIFEST, indent=2),
        content_type=ContentType.FRAMEWORK,
        topics=["tools", "possible futures", "ideas", "validation"],
        created_at=datetime.now(),
        source="internal:tool_manifest",
        metadata={"type": "tool_documentation"}
    )
    store.add_content(tools_content)
    
    # Generate training examples from tools
    from tasks.knowledge_base import TrainingExample
    
    for tool_name, tool_spec in TOOL_MANIFEST.items():
        # Create example of tool usage
        example = TrainingExample(
            prompt=f"How do I use the {tool_name} tool?",
            completion=f"The {tool_name} tool {tool_spec['description']}.\n\nParameters:\n" + 
                      "\n".join(f"- {k}: {v}" for k, v in tool_spec['parameters'].items()),
            metadata={"strategy": "tool_documentation", "tool": tool_name},
            source_content_id=tools_content.id
        )
        store.add_training_example(example)
    
    print(f"  ✓ Added {len(TOOL_MANIFEST)} tool examples")
    
    print(f"\n✓ Total content items: {len(store.get_all_content())}")
    print(f"✓ Total training examples: {len(store.get_all_training_examples())}")
    
    return store


def add_synthetic_examples(store):
    """Add synthetic examples of tool usage"""
    print("\n" + "=" * 80)
    print("STEP 2: Generating Synthetic Tool Usage Examples")
    print("=" * 80)
    
    from tasks.knowledge_base import TrainingExample, ContentItem
    
    # Create synthetic content for examples
    synthetic_content = ContentItem(
        id="",
        title="Synthetic Tool Usage Examples",
        content="Examples of how to use Possible Futures tools",
        content_type=ContentType.EXAMPLE,
        topics=["tools", "examples", "possible futures"],
        created_at=datetime.now(),
        source="synthetic:tool_examples",
        metadata={"type": "synthetic"}
    )
    store.add_content(synthetic_content)
    
    # Example conversations
    examples = [
        {
            "prompt": "I want to build a platform for freelance designers. How should I start?",
            "completion": """Let me help you explore this as a possible future. First, I'll create an idea:

```python
idea = create_idea(
    name="Freelance Designer Platform",
    description="Platform connecting freelance designers with clients, featuring portfolio hosting and project management"
)
```

Now let's add what we know about the system:

```python
# Core components
add_system_component(
    idea_id=idea['id'],
    component_name="portfolio_hosting",
    component_type="ui",
    specification={"features": ["image_upload", "project_showcase", "custom_themes"]},
    confidence=0.85
)

add_system_component(
    idea_id=idea['id'],
    component_name="project_management",
    component_type="business_logic",
    specification={"features": ["milestones", "file_sharing", "invoicing"]},
    confidence=0.75
)
```

Let's identify critical assumptions:

```python
add_world_assumption(
    idea_id=idea['id'],
    assumption_text="Freelance designers will pay $20/month for premium features",
    category="market",
    criticality=0.9
)
```

And set measurable goals:

```python
add_goal(
    idea_id=idea['id'],
    goal_text="Onboard 1000 designers in first 3 months",
    metric_name="designer_signups_3mo",
    target_value=1000,
    validator_function="numeric_threshold"
)
```

You can check the status anytime with `get_idea_status(idea['id'])` to see health metrics and what needs validation."""
        },
        {
            "prompt": "Show me how to validate if my goals are being met",
            "completion": """To validate goals, use the `check_goals` tool with current metrics:

```python
# Provide current metric values
results = check_goals(
    idea_id="your_idea_id",
    current_metrics={
        "designer_signups_3mo": 850,  # Current value
        "client_satisfaction_pct": 92.0,
        "active_projects": 120
    }
)

# Results show pass/fail for each goal
for goal_text, result in results.items():
    if result['passed']:
        print(f"✓ {goal_text}")
        print(f"  Actual: {result['actual_value']}, {result['message']}")
    else:
        print(f"✗ {goal_text}")
        print(f"  Actual: {result['actual_value']}, {result['message']}")
```

This tells you exactly which goals are achieved and which need more work."""
        },
        {
            "prompt": "What if I want to explore two different approaches to the same idea?",
            "completion": """Use branching to explore alternative futures:

```python
# Create base idea
base = create_idea(
    name="Food Delivery Platform",
    description="Platform for local food delivery"
)

# Branch 1: Restaurant-focused
branch1 = create_idea(
    name="Food Delivery - Restaurant Model",
    description="Partner with restaurants, they handle food prep",
    parent_idea_id=base['id']
)

# Branch 2: Dark kitchen model
branch2 = create_idea(
    name="Food Delivery - Dark Kitchen Model",
    description="Own kitchen facilities, control quality end-to-end",
    parent_idea_id=base['id']
)
```

Now you can develop each branch independently, add different components and assumptions, and compare their health scores to decide which approach is stronger."""
        },
        {
            "prompt": "How do I know when an idea is ready to move to the next stage?",
            "completion": """Use `advance_idea_stage()` to try progressing:

```python
result = advance_idea_stage(idea_id)

if result['success']:
    print(f"✓ Advanced from {result['previous_stage']} to {result['current_stage']}")
else:
    print(f"✗ Cannot advance yet: {result['message']}")
    
    # Check what's blocking advancement
    status = get_idea_status(idea_id)
    health = status['health']
    
    print(f"Critical assumptions: {health['critical_assumptions_count']}")
    print(f"Validated: {health['critical_assumptions_validated']}")
    print(f"Need to validate: {health['critical_assumptions_count'] - health['critical_assumptions_validated']}")
```

An idea can advance when:
1. It has at least 1 knowledge component
2. 80%+ of critical assumptions (criticality > 0.7) are validated

This forces proper validation before moving forward."""
        }
    ]
    
    for i, example in enumerate(examples, 1):
        training_example = TrainingExample(
            prompt=example['prompt'],
            completion=example['completion'],
            metadata={"strategy": "synthetic_conversation", "example_number": i},
            source_content_id=synthetic_content.id
        )
        store.add_training_example(training_example)
        print(f"  ✓ Added synthetic example {i}")
    
    print(f"\n✓ Added {len(examples)} synthetic examples")


def export_training_data(store):
    """Export combined training data"""
    print("\n" + "=" * 80)
    print("STEP 3: Exporting Training Data")
    print("=" * 80)
    
    # Export as JSONL for fine-tuning
    jsonl_path = "./data/possible_futures_training.jsonl"
    store.export_training_data(jsonl_path, format="jsonl")
    print(f"\n✓ Exported JSONL: {jsonl_path}")
    
    # Export as JSON for inspection
    json_path = "./data/possible_futures_training.json"
    store.export_training_data(json_path, format="json")
    print(f"✓ Exported JSON: {json_path}")
    
    # Show statistics
    examples = store.get_all_training_examples()
    print(f"\n📊 Training Data Statistics:")
    print(f"  Total examples: {len(examples)}")
    
    # Count by strategy
    strategies = {}
    for ex in examples:
        strategy = ex.metadata.get('strategy', 'unknown')
        strategies[strategy] = strategies.get(strategy, 0) + 1
    
    print(f"  By strategy:")
    for strategy, count in sorted(strategies.items()):
        print(f"    - {strategy}: {count}")
    
    return jsonl_path, json_path


def generate_skippy_examples(store):
    """Generate examples in Skippy's voice for the Apprentice Guild"""
    print("\n" + "=" * 80)
    print("STEP 4: Generating Skippy's Apprentice Training Examples")
    print("=" * 80)
    
    from tasks.knowledge_base import TrainingExample, ContentItem
    
    # Create Skippy content
    skippy_content = ContentItem(
        id="",
        title="Skippy's Apprentice Training with Possible Futures",
        content="How Skippy uses Possible Futures tools to train apprentices",
        content_type=ContentType.FRAMEWORK,
        topics=["skippy", "apprentice", "training", "possible futures"],
        created_at=datetime.now(),
        source="synthetic:skippy_training",
        metadata={"character": "skippy", "guild": "apprentice"}
    )
    store.add_content(skippy_content)
    
    skippy_examples = [
        {
            "prompt": "Skippy, I have this amazing idea for a social network for cats!",
            "completion": """Oh WONDERFUL. Another monkey with a "revolutionary" idea that's definitely not just Instagram for a different demographic.

But fine. Let's make you THINK about this properly. I'm spawning your idea into the system:

```python
idea = create_idea(
    name="Social Network for Cats",
    description="Monkey's probably-not-thought-through idea for cats to share photos"
)
```

Now. Before you get all excited, let's add what you're ASSUMING:

```python
add_world_assumption(
    idea_id=idea['id'],
    assumption_text="Cat owners will create accounts for their cats",
    category="user_behavior",
    criticality=0.95  # CRITICAL - your whole idea depends on this
)

add_world_assumption(
    idea_id=idea['id'],
    assumption_text="Cat owners will pay subscription for premium features",
    category="market",
    criticality=0.90  # Also CRITICAL - you need revenue
)
```

See those criticality scores? Both over 0.7. That means you need to VALIDATE them before you can advance past requirements. 

And let me guess - you haven't validated EITHER of them, have you? You just "feel" like it would work?

Here's your assignment: Talk to 50 cat owners. Real people. Not your cat-loving roommate. PROVE these assumptions or come back and spawn a different idea.

The system won't let you advance until you do. That's not me being mean - that's REALITY protecting you from your own enthusiasm.

Check your status:
```python
status = get_idea_status(idea['id'])
# Health score: probably 0.2 because you have zero validated assumptions
# Uncertainty: VERY_HIGH because you're just guessing
```

Git gud requires EVIDENCE, not excitement. Now go validate or go home."""
        },
        {
            "prompt": "I validated my assumptions! Can I build now?",
            "completion": """Hold up there, monkey. "Validated" means you have EVIDENCE, not that your mom said it's a good idea.

Let's check:

```python
status = get_idea_status(idea['id'])
health = status['health']

print(f"Validated assumptions: {health['validated_assumptions']}/{health['total_assumptions']}")
print(f"Validation rate: {health['assumption_validation_rate']*100}%")
```

If that validation rate is below 80% for CRITICAL assumptions, you're not ready.

But let's say you actually did the work (I'm skeptical, but let's pretend). You'd update the assumptions:

```python
# You'd need to mark them validated with evidence
# The system tracks this
```

THEN you can try to advance:

```python
result = advance_idea_stage(idea['id'])
if result['success']:
    print("Fine. You advanced to ANALYSIS. Don't get cocky.")
else:
    print(f"Nope. {result['message']}")
    print("Back to validation, monkey. Do the actual work.")
```

See how the system forces you to be HONEST? That's by design. It won't let you advance on vibes and good feelings.

Now what GOALS did you set for this thing? Because "build a cool social network" isn't a goal. It's a dream.

This should be a goal:
```python
add_goal(
    idea_id=idea['id'],
    goal_text="1000 active cat accounts within 3 months of launch",
    metric_name="active_cat_accounts_3mo",
    target_value=1000,
    validator_function="numeric_threshold"
)
```

MEASURABLE. SPECIFIC. FALSIFIABLE.

Not "be successful" or "get users" - ACTUAL NUMBERS that the system can check.

That's the difference between monkeys and builders. Builders have numbers. Monkeys have hopes.

Which one are you?"""
        }
    ]
    
    for i, example in enumerate(skippy_examples, 1):
        training_example = TrainingExample(
            prompt=example['prompt'],
            completion=example['completion'],
            metadata={
                "strategy": "skippy_character",
                "character": "skippy",
                "guild": "apprentice",
                "example_number": i
            },
            source_content_id=skippy_content.id
        )
        store.add_training_example(training_example)
        print(f"  ✓ Added Skippy example {i}")
    
    print(f"\n✓ Added {len(skippy_examples)} Skippy examples")


def main():
    """Main preparation pipeline"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "POSSIBLE FUTURES - TRAINING DATA PREPARATION" + " " * 18 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Step 1: Ingest existing content
    store = ingest_project_content()
    
    # Step 2: Add synthetic examples
    add_synthetic_examples(store)
    
    # Step 3: Add Skippy examples
    generate_skippy_examples(store)
    
    # Step 4: Export
    jsonl_path, json_path = export_training_data(store)
    
    # Summary
    print("\n" + "=" * 80)
    print("✨ PREPARATION COMPLETE!")
    print("=" * 80)
    print(f"""
Next steps:

1. Review the exported data:
   - JSONL (for training): {jsonl_path}
   - JSON (for inspection): {json_path}

2. Add to your training configuration:
   ```python
   # In your training script
   from tasks.idea_tools import TOOL_MANIFEST
   
   # Make tools available to model during training
   tools = TOOL_MANIFEST
   ```

3. After training, test the model:
   ```python
   # The model should now be able to:
   - Spawn ideas with create_idea()
   - Add components with add_system_component()
   - Identify assumptions with add_world_assumption()
   - Set goals with add_goal()
   - Validate progress with check_goals()
   ```

4. Run the examples:
   ```bash
   python tasks/example_possible_futures.py
   ```

The trained model will use these tools to help users explore possible
futures systematically, with proper uncertainty management and validation.
    """)
    
    store.close()


if __name__ == "__main__":
    main()

