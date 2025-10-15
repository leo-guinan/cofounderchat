"""
Example usage of the Possible Futures system

This demonstrates how a trained model would use the tools to:
1. Spawn ideas (possible futures)
2. Add system components and assumptions
3. Set goals and validate them
4. Progress through waterfall stages
"""

from .idea_tools import (
    create_idea,
    add_system_component,
    add_world_assumption,
    add_goal,
    check_goals,
    get_idea_status,
    advance_idea_stage,
    list_all_ideas,
    get_stage_history
)


def example_ecommerce_platform():
    """
    Example: AI model spawning an idea for an e-commerce platform
    """
    
    print("=" * 80)
    print("EXAMPLE: E-Commerce Platform Possible Future")
    print("=" * 80)
    
    # Step 1: Spawn the idea
    print("\n1. Spawning idea...")
    idea = create_idea(
        name="Sustainable Fashion Marketplace",
        description="A marketplace connecting conscious consumers with sustainable fashion brands, "
                   "emphasizing transparency, fair trade, and circular economy principles."
    )
    print(f"Created idea: {idea['id']}")
    print(f"  Name: {idea['name']}")
    print(f"  Stage: {idea['current_stage']}")
    print(f"  Uncertainty: {idea['uncertainty_level']}")
    
    idea_id = idea['id']
    
    # Step 2: Add system components (REQUIREMENTS stage)
    print("\n2. Adding known system components...")
    
    add_system_component(
        idea_id=idea_id,
        component_name="product_catalog",
        component_type="database",
        specification={
            "type": "PostgreSQL",
            "schema": {
                "products": ["id", "name", "brand_id", "sustainability_score", "materials", "price"],
                "brands": ["id", "name", "certifications", "practices"],
                "certifications": ["id", "name", "issuing_body", "criteria"]
            }
        },
        confidence=0.9
    )
    print("  ✓ Added product catalog database")
    
    add_system_component(
        idea_id=idea_id,
        component_name="user_profiles",
        component_type="api",
        specification={
            "endpoints": [
                {"path": "/users", "methods": ["GET", "POST", "PUT"]},
                {"path": "/users/{id}/preferences", "methods": ["GET", "PUT"]},
                {"path": "/users/{id}/purchase-history", "methods": ["GET"]}
            ],
            "auth": "OAuth2"
        },
        confidence=0.85
    )
    print("  ✓ Added user profiles API")
    
    add_system_component(
        idea_id=idea_id,
        component_name="sustainability_scoring_engine",
        component_type="business_logic",
        specification={
            "inputs": ["materials", "manufacturing_location", "certifications", "packaging", "shipping"],
            "algorithm": "weighted_average",
            "weights": {
                "materials": 0.3,
                "manufacturing": 0.25,
                "certifications": 0.25,
                "packaging": 0.1,
                "shipping": 0.1
            },
            "output_range": [0, 100]
        },
        confidence=0.7  # Lower confidence - this is complex
    )
    print("  ✓ Added sustainability scoring engine")
    
    # Step 3: Add assumptions about the world
    print("\n3. Adding world assumptions...")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Consumers aged 18-35 will pay 10-20% premium for sustainable products",
        category="market",
        criticality=0.9  # This is critical to the business model
    )
    print("  ✓ Added market assumption (CRITICAL)")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Brands will adopt API-based integration for real-time inventory",
        category="technology",
        criticality=0.7
    )
    print("  ✓ Added technology assumption")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Third-party certification data will be available via open APIs",
        category="resources",
        criticality=0.8
    )
    print("  ✓ Added resources assumption")
    
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="Users will trust platform's sustainability scoring methodology",
        category="user_behavior",
        criticality=0.95  # VERY critical
    )
    print("  ✓ Added user behavior assumption (VERY CRITICAL)")
    
    # Step 4: Add goals
    print("\n4. Adding measurable goals...")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Achieve 10,000 active users within 6 months of launch",
        metric_name="active_users_6mo",
        target_value=10000,
        validator_function="numeric_threshold"
    )
    print("  ✓ Added user growth goal")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Maintain 85% or higher customer satisfaction rating",
        metric_name="customer_satisfaction_pct",
        target_value=85.0,
        validator_function="percentage"
    )
    print("  ✓ Added satisfaction goal")
    
    add_goal(
        idea_id=idea_id,
        goal_text="Onboard at least 50 sustainable brands",
        metric_name="partner_brands",
        target_value=50,
        validator_function="numeric_threshold"
    )
    print("  ✓ Added brand partnership goal")
    
    # Step 5: Check current status
    print("\n5. Checking idea health...")
    status = get_idea_status(idea_id)
    print(f"  Stage: {status['idea']['current_stage']}")
    print(f"  Uncertainty: {status['idea']['uncertainty_level']}")
    print(f"  Health Score: {status['health']['overall_health_score']:.2f}")
    print(f"  Knowledge Items: {status['health']['total_knowledge_items']}")
    print(f"  Assumptions: {status['health']['total_assumptions']}")
    print(f"  Validated Assumptions: {status['health']['validated_assumptions']}")
    print(f"  Goals: {status['health']['total_goals']}")
    print(f"  Achieved Goals: {status['health']['achieved_goals']}")
    
    # Step 6: Try to advance stage (will fail - critical assumptions not validated)
    print("\n6. Attempting to advance to ANALYSIS stage...")
    result = advance_idea_stage(idea_id)
    print(f"  Success: {result['success']}")
    print(f"  Message: {result['message']}")
    
    if not result['success']:
        print("\n  → Cannot advance yet! Critical assumptions need validation.")
        print("  → In a real system, this would trigger research/validation tasks.")
    
    # Step 7: Simulate some goal checking
    print("\n7. Simulating goal validation (with mock metrics)...")
    mock_metrics = {
        "active_users_6mo": 8500,  # Not quite there yet
        "customer_satisfaction_pct": 87.5,  # Exceeds target!
        "partner_brands": 45  # Close to target
    }
    
    goal_results = check_goals(idea_id, mock_metrics)
    for goal_text, result in goal_results.items():
        status_icon = "✓" if result['passed'] else "✗"
        print(f"  {status_icon} {goal_text}")
        print(f"     {result['message']}")
    
    # Step 8: Get event history
    print("\n8. Viewing event history for REQUIREMENTS stage...")
    history = get_stage_history(idea_id, "requirements")
    print(f"  Initial state created: {history['initial_state_created']}")
    print(f"  Total changes: {len(history['changes'])}")
    print("\n  Recent changes:")
    for change in history['changes'][-3:]:  # Last 3 changes
        print(f"    - {change['change_type']} at {change['timestamp']}")
    
    print("\n" + "=" * 80)
    print("Example complete! The idea is now tracked in the SQLite databases.")
    print("=" * 80)
    
    return idea_id


def example_branching_ideas():
    """
    Example: Creating a branch from an existing idea
    """
    
    print("\n" + "=" * 80)
    print("EXAMPLE: Branching Ideas (Exploring Alternative Futures)")
    print("=" * 80)
    
    # Create base idea
    base_idea = create_idea(
        name="SaaS Analytics Platform",
        description="Real-time analytics platform for SaaS businesses"
    )
    base_id = base_idea['id']
    print(f"\n1. Created base idea: {base_idea['name']}")
    
    # Create two branches exploring different approaches
    branch_1 = create_idea(
        name="SaaS Analytics - Self-Hosted",
        description="Self-hosted version for enterprises with strict data requirements",
        parent_idea_id=base_id
    )
    print(f"2. Created branch 1: {branch_1['name']}")
    
    branch_2 = create_idea(
        name="SaaS Analytics - Fully Managed",
        description="Fully managed cloud service with AI-powered insights",
        parent_idea_id=base_id
    )
    print(f"3. Created branch 2: {branch_2['name']}")
    
    # List all ideas
    print("\n4. All active ideas:")
    all_ideas = list_all_ideas()
    for idea in all_ideas:
        parent_marker = f" (branch of {idea['parent_idea_id'][:8]}...)" if idea['parent_idea_id'] else ""
        print(f"   - {idea['name']}{parent_marker}")
        print(f"     ID: {idea['id']}")
        print(f"     Stage: {idea['current_stage']}")
    
    print("\n" + "=" * 80)
    print("Branching example complete!")
    print("=" * 80)


if __name__ == "__main__":
    # Run examples
    print("\n\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "POSSIBLE FUTURES SYSTEM - EXAMPLES" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # Example 1: E-commerce platform
    idea_id = example_ecommerce_platform()
    
    # Example 2: Branching ideas
    example_branching_ideas()
    
    print("\n\n✨ All examples completed successfully!")
    print("\nNext steps:")
    print("  - Check the SQLite databases in ./data/possible_futures/")
    print("  - Each idea has separate DBs for each waterfall stage")
    print("  - All state changes are event-sourced and queryable")
    print("  - Integrate these tools into your trained model for idea generation\n")

