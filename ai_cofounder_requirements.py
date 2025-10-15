#!/usr/bin/env python3
"""
AI Cofounder App - Initial Requirements

Using the Possible Futures system to define the AI Cofounder app.
This becomes both the requirements AND a demonstration of the system.
"""

from tasks.idea_tools import (
    create_idea,
    add_system_component,
    add_world_assumption,
    add_goal,
    get_idea_status,
    advance_idea_stage
)


def spawn_ai_cofounder_idea():
    """
    Spawn the AI Cofounder app as a possible future
    
    This is meta: the AI Cofounder helps users explore possible futures,
    and we're using that same system to define the AI Cofounder itself.
    """
    
    print("=" * 80)
    print("AI COFOUNDER APP - REQUIREMENTS SPECIFICATION")
    print("=" * 80)
    print()
    
    # ========================================================================
    # STEP 1: Spawn the Idea
    # ========================================================================
    
    print("1. SPAWNING IDEA...")
    print("-" * 80)
    
    idea = create_idea(
        name="AI Cofounder App",
        description="""
An AI-powered cofounder that helps entrepreneurs navigate business complexity.

The AI Cofounder:
- Learns from the user's content to understand their thinking
- Adapts to their established systems and workflows
- Helps them make money as early as possible
- Monitors current and possible future business states
- Provides conversational guidance through chat
- Enables rapid capture of ideas/attention items

The app itself is built BY the AI Cofounder as one of its first tasks,
demonstrating its ability to create software systems.

Philosophy: Conscious Economics meets FRP architecture.
Skippy's spirit: Force clarity, validate assumptions, measure outcomes.
        """.strip()
    )
    
    idea_id = idea['id']
    print(f"✓ Created idea: {idea_id}")
    print(f"  Name: {idea['name']}")
    print(f"  Stage: {idea['current_stage']}")
    print(f"  Uncertainty: {idea['uncertainty_level']}")
    print()
    
    # ========================================================================
    # STEP 2: Define System Knowledge (What We KNOW)
    # ========================================================================
    
    print("2. ADDING SYSTEM KNOWLEDGE (The Knowns)...")
    print("-" * 80)
    
    # Component 1: Content Ingestion Engine
    add_system_component(
        idea_id=idea_id,
        component_name="content_ingestion_engine",
        component_type="business_logic",
        specification={
            "purpose": "Learn from user's existing content",
            "inputs": [
                "URLs (blog posts, videos, podcasts, tweets)",
                "Documents (PDFs, markdown, text)",
                "Code repositories",
                "Chat history",
                "Notes/Roam/Obsidian exports"
            ],
            "processing": [
                "Extract text/transcripts",
                "Identify topics and frameworks",
                "Build knowledge graph of user's thinking",
                "Extract patterns in decision-making",
                "Identify user's 'Fragments' (Whale, Researcher, Builder, etc.)"
            ],
            "outputs": [
                "User mental model",
                "Topic expertise map",
                "Communication style profile",
                "Decision pattern database"
            ],
            "technology": "Uses knowledge_base.py from Possible Futures system"
        },
        confidence=0.9  # We know we can build this - already have foundation
    )
    print("  ✓ content_ingestion_engine (business_logic, confidence: 0.9)")
    
    # Component 2: Business State Monitor
    add_system_component(
        idea_id=idea_id,
        component_name="business_state_monitor",
        component_type="business_logic",
        specification={
            "purpose": "Track current state of user's business",
            "metrics_tracked": [
                "Revenue (daily, weekly, monthly)",
                "Expenses",
                "Active customers",
                "Churn rate",
                "Time violence score (complexity burden)",
                "Momentum indicators",
                "Goal progress"
            ],
            "data_sources": [
                "User input (manual entry)",
                "API integrations (Stripe, bank, analytics)",
                "Chat mentions ('made $500 today')",
                "Email parsing (receipts, invoices)"
            ],
            "architecture": "Event-sourced using FRP principles",
            "storage": "SQLite with state = f(initial, changes)"
        },
        confidence=0.85  # High confidence - we have the architecture
    )
    print("  ✓ business_state_monitor (business_logic, confidence: 0.85)")
    
    # Component 3: Possible Futures Engine (already built!)
    add_system_component(
        idea_id=idea_id,
        component_name="possible_futures_engine",
        component_type="business_logic",
        specification={
            "purpose": "Help user explore alternative business futures",
            "capabilities": [
                "Spawn ideas for products/features/pivots",
                "Track assumptions that need validation",
                "Set measurable goals with validators",
                "Monitor idea health and uncertainty",
                "Compare multiple futures side-by-side",
                "Event-sourced history of all ideas"
            ],
            "implementation": "tasks/possible_futures.py (already complete)",
            "tools_api": "tasks/idea_tools.py (9 tools)",
            "architecture": "FRP following 'Out of the Tar Pit'"
        },
        confidence=1.0  # Already built and tested!
    )
    print("  ✓ possible_futures_engine (business_logic, confidence: 1.0)")
    
    # Component 4: AI Cofounder Chat Interface
    add_system_component(
        idea_id=idea_id,
        component_name="ai_cofounder_chat",
        component_type="ui",
        specification={
            "purpose": "Conversational interface with AI Cofounder",
            "features": [
                "Chat with context from user's content",
                "Access to Possible Futures tools",
                "Can spawn/manage ideas mid-conversation",
                "Shows business metrics inline",
                "Suggests next actions based on goals",
                "Skippy-style coaching when needed"
            ],
            "technology_stack": [
                "Frontend: React/Next.js or htmx (simple)",
                "Backend: Python FastAPI",
                "LLM: Your trained model with tools",
                "Real-time: WebSocket or SSE"
            ],
            "interface_modes": [
                "Coach mode (Skippy-style tough love)",
                "Advisor mode (strategic guidance)",
                "Assistant mode (tactical help)",
                "Debug mode (show reasoning)"
            ]
        },
        confidence=0.8  # Standard webapp - we know how to build
    )
    print("  ✓ ai_cofounder_chat (ui, confidence: 0.8)")
    
    # Component 5: Quick Capture System
    add_system_component(
        idea_id=idea_id,
        component_name="quick_capture",
        component_type="integration",
        specification={
            "purpose": "Capture anything in user's attention for processing",
            "capture_methods": [
                "Web clipper (browser extension)",
                "Email forwarding (forward@yourcofounder.ai)",
                "Mobile quick-add (iOS/Android)",
                "API endpoint (for custom integrations)",
                "Telegram/SMS bot",
                "Voice memos (Whisper transcription)"
            ],
            "processing": [
                "Extract intent (is this an idea? task? insight?)",
                "Route to appropriate system (Futures, Tasks, Notes)",
                "Notify user of next steps",
                "Learn capture patterns over time"
            ],
            "storage": "Queue in SQLite, process async"
        },
        confidence=0.7  # Multiple integrations - more complex
    )
    print("  ✓ quick_capture (integration, confidence: 0.7)")
    
    # Component 6: Self-Building Webapp Generator
    add_system_component(
        idea_id=idea_id,
        component_name="self_building_webapp",
        component_type="business_logic",
        specification={
            "purpose": "AI Cofounder builds its own webapp as first task",
            "approach": [
                "AI Cofounder uses Possible Futures to design webapp",
                "Generates code using its own tools",
                "Creates requirements → analysis → design → implementation",
                "Validates each stage before advancing",
                "Deploys and iterates based on user feedback"
            ],
            "demonstration_value": [
                "Shows AI Cofounder can build software",
                "Validates the Possible Futures methodology",
                "Builds trust with user",
                "Creates working product from day 1"
            ],
            "opinionated_defaults": [
                "htmx for simplicity (no heavy JS framework)",
                "SQLite for data (simple, event-sourced)",
                "FastAPI for backend (Python, async)",
                "Tailwind for styling (utility-first)",
                "Deploy to fly.io (simple, fast)"
            ],
            "customization_later": [
                "User can swap technologies",
                "User can modify UI/UX",
                "User can add/remove features",
                "But start opinionated for speed"
            ]
        },
        confidence=0.6  # Novel - never been done, but possible
    )
    print("  ✓ self_building_webapp (business_logic, confidence: 0.6)")
    
    # Component 7: Dashboard (Opinionated Default UI)
    add_system_component(
        idea_id=idea_id,
        component_name="dashboard",
        component_type="ui",
        specification={
            "purpose": "Single-page view of business reality and possibilities",
            "sections": [
                {
                    "name": "Current State",
                    "shows": [
                        "Revenue today/this week/this month",
                        "Active goals and progress",
                        "Time violence score",
                        "Momentum indicators",
                        "Recent captures"
                    ]
                },
                {
                    "name": "Possible Futures",
                    "shows": [
                        "Active ideas being explored",
                        "Health scores",
                        "Critical assumptions needing validation",
                        "Next actions per idea"
                    ]
                },
                {
                    "name": "AI Cofounder Chat",
                    "shows": [
                        "Inline chat interface",
                        "Recent suggestions",
                        "Context-aware based on current view"
                    ]
                }
            ],
            "design_philosophy": [
                "Brutally simple",
                "Information-dense but readable",
                "Fast (< 100ms load)",
                "Works on mobile",
                "No unnecessary decoration",
                "Skippy aesthetic: function over form"
            ],
            "technology": "htmx + Tailwind + FastAPI templates"
        },
        confidence=0.85  # Standard UI - we know this pattern
    )
    print("  ✓ dashboard (ui, confidence: 0.85)")
    
    print()
    
    # ========================================================================
    # STEP 3: Define World Assumptions (What We're ASSUMING - The Unknowns)
    # ========================================================================
    
    print("3. ADDING WORLD ASSUMPTIONS (The Unknowns - Need Validation)...")
    print("-" * 80)
    
    # CRITICAL ASSUMPTION 1: User Behavior - Content Sharing
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
Users will willingly share their content (blog posts, videos, notes, code) with the AI Cofounder 
to help it understand their thinking. They'll see this as valuable rather than invasive.
        """.strip(),
        category="user_behavior",
        criticality=0.95  # VERY CRITICAL - entire value prop depends on this
    )
    print("  ✓ [CRITICAL 0.95] User will share their content")
    
    # CRITICAL ASSUMPTION 2: User Behavior - AI Cofounder Relationship
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
Users will develop a working relationship with an AI "cofounder" and take its advice seriously.
They won't dismiss it as "just a chatbot" but will engage with it as a thinking partner.
        """.strip(),
        category="user_behavior",
        criticality=0.90  # CRITICAL - defines the product category
    )
    print("  ✓ [CRITICAL 0.90] Users will engage as true cofounder relationship")
    
    # CRITICAL ASSUMPTION 3: Market - Willingness to Pay
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
Solo entrepreneurs and small teams will pay $50-200/month for an AI Cofounder that helps them 
make better decisions and move faster. The time saved and revenue generated justifies the cost.
        """.strip(),
        category="market",
        criticality=0.85  # CRITICAL - business model
    )
    print("  ✓ [CRITICAL 0.85] Market will pay $50-200/mo")
    
    # CRITICAL ASSUMPTION 4: Technology - Self-Building Works
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
An AI can successfully build its own webapp using the Possible Futures methodology. It can move 
through requirements → design → implementation and create working software without human coding.
        """.strip(),
        category="technology",
        criticality=0.75  # CRITICAL - core demo/differentiator
    )
    print("  ✓ [CRITICAL 0.75] AI can build its own webapp")
    
    # ASSUMPTION 5: User Behavior - Early Monetization Focus
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
Users will appreciate being pushed toward monetization early rather than perfecting products.
They'll see "make money now" pressure as helpful rather than premature.
        """.strip(),
        category="user_behavior",
        criticality=0.70  # CRITICAL threshold - this is borderline
    )
    print("  ✓ [CRITICAL 0.70] Users appreciate early monetization push")
    
    # ASSUMPTION 6: Technology - Adaptation to User Systems
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
The AI can successfully learn and adapt to each user's unique systems (workflows, tools, 
decision frameworks) rather than forcing them into a standard process.
        """.strip(),
        category="technology",
        criticality=0.65  # Important but not critical - can start with standard process
    )
    print("  ✓ [0.65] AI can adapt to unique user systems")
    
    # ASSUMPTION 7: Market - Competition
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
Generic AI assistants (ChatGPT, Claude, etc.) won't solve this problem well enough to prevent 
need for specialized AI Cofounder. Context + business focus = defensible moat.
        """.strip(),
        category="market",
        criticality=0.60  # Important for long-term but not immediate launch blocker
    )
    print("  ✓ [0.60] Generic AI won't be good enough competitor")
    
    # ASSUMPTION 8: User Behavior - Quick Capture Usage
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
Users will develop habit of capturing ideas/insights through quick-capture mechanisms 
(email, extension, mobile) rather than just using the webapp directly.
        """.strip(),
        category="user_behavior",
        criticality=0.50  # Nice to have, not critical
    )
    print("  ✓ [0.50] Users will develop capture habits")
    
    # ASSUMPTION 9: Regulations - AI Liability
    add_world_assumption(
        idea_id=idea_id,
        assumption_text="""
No new regulations will prevent marketing an AI as a "cofounder" or make the creator liable 
for business decisions made based on AI advice.
        """.strip(),
        category="regulations",
        criticality=0.40  # Low - unlikely to be blocked
    )
    print("  ✓ [0.40] No regulatory blockers for AI cofounder positioning")
    
    print()
    
    # ========================================================================
    # STEP 4: Define Goals (Measurable Outcomes)
    # ========================================================================
    
    print("4. ADDING MEASURABLE GOALS...")
    print("-" * 80)
    
    # GOAL 1: Build the MVP
    add_goal(
        idea_id=idea_id,
        goal_text="AI Cofounder builds its own working webapp within 7 days of project start",
        metric_name="webapp_build_days",
        target_value=7,
        validator_function="numeric_threshold"  # actual_days <= 7
    )
    print("  ✓ Build MVP in 7 days")
    
    # GOAL 2: User Acquisition
    add_goal(
        idea_id=idea_id,
        goal_text="Acquire 100 users willing to try the AI Cofounder within 30 days of launch",
        metric_name="users_30_days",
        target_value=100,
        validator_function="numeric_threshold"
    )
    print("  ✓ 100 users in 30 days")
    
    # GOAL 3: Engagement
    add_goal(
        idea_id=idea_id,
        goal_text="70% of users chat with AI Cofounder at least 3x per week",
        metric_name="weekly_active_engagement_pct",
        target_value=70.0,
        validator_function="percentage"
    )
    print("  ✓ 70% engage 3x/week")
    
    # GOAL 4: Value Delivery
    add_goal(
        idea_id=idea_id,
        goal_text="Users spawn average of 5+ possible futures per month using the tools",
        metric_name="avg_futures_per_user_per_month",
        target_value=5,
        validator_function="numeric_threshold"
    )
    print("  ✓ 5 futures per user per month")
    
    # GOAL 5: Revenue
    add_goal(
        idea_id=idea_id,
        goal_text="At least 20% of users convert to paid within 60 days",
        metric_name="paid_conversion_rate_pct",
        target_value=20.0,
        validator_function="percentage"
    )
    print("  ✓ 20% paid conversion")
    
    # GOAL 6: User Outcomes
    add_goal(
        idea_id=idea_id,
        goal_text="50% of active users report making money from something AI Cofounder helped with",
        metric_name="revenue_attribution_pct",
        target_value=50.0,
        validator_function="percentage"
    )
    print("  ✓ 50% make money from AI help")
    
    # GOAL 7: Retention
    add_goal(
        idea_id=idea_id,
        goal_text="Month-2 retention rate above 60% for paid users",
        metric_name="month_2_retention_pct",
        target_value=60.0,
        validator_function="percentage"
    )
    print("  ✓ 60% retention at month 2")
    
    print()
    
    # ========================================================================
    # STEP 5: Check Status
    # ========================================================================
    
    print("5. CHECKING IDEA STATUS...")
    print("-" * 80)
    
    status = get_idea_status(idea_id)
    health = status['health']
    
    print(f"Current Stage: {status['idea']['current_stage']}")
    print(f"Uncertainty Level: {status['idea']['uncertainty_level']}")
    print()
    print(f"Health Metrics:")
    print(f"  Overall Health Score: {health['overall_health_score']:.2f}")
    print(f"  Knowledge Items: {health['total_knowledge_items']}")
    print(f"  Avg Confidence: {health['average_confidence']:.2f}")
    print(f"  Total Assumptions: {health['total_assumptions']}")
    print(f"  Validated Assumptions: {health['validated_assumptions']}")
    print(f"  Critical Assumptions: {health['critical_assumptions_count']}")
    print(f"  Critical Validated: {health['critical_assumptions_validated']}")
    print(f"  Goals Defined: {health['total_goals']}")
    print(f"  Goals Achieved: {health['achieved_goals']}")
    print()
    
    # ========================================================================
    # STEP 6: Attempt to Advance (Will Fail - Need Validation)
    # ========================================================================
    
    print("6. ATTEMPTING TO ADVANCE TO ANALYSIS STAGE...")
    print("-" * 80)
    
    result = advance_idea_stage(idea_id)
    print(f"Result: {'SUCCESS' if result['success'] else 'BLOCKED'}")
    print(f"Message: {result['message']}")
    print()
    
    if not result['success']:
        print("NEXT ACTIONS REQUIRED:")
        print("-" * 80)
        print()
        print("To advance past REQUIREMENTS, you must validate critical assumptions:")
        print()
        print("1. [CRITICAL 0.95] Will users share their content?")
        print("   → Test: Build simple content ingestion form")
        print("   → Survey 20 target users about privacy comfort")
        print("   → Check: Do they have shareable content?")
        print()
        print("2. [CRITICAL 0.90] Will users engage as cofounder relationship?")
        print("   → Test: Wizard-of-Oz prototype (you play AI Cofounder)")
        print("   → Measure: Do they take advice? How often do they return?")
        print("   → Interview: How do they describe the relationship?")
        print()
        print("3. [CRITICAL 0.85] Will market pay $50-200/mo?")
        print("   → Test: Pricing survey with 50 target users")
        print("   → Validate: Show mock product, ask 'would you pay?'")
        print("   → Benchmark: What do they currently pay for similar value?")
        print()
        print("4. [CRITICAL 0.75] Can AI build its own webapp?")
        print("   → Test: Have AI Cofounder prototype this with you")
        print("   → Start: Use Possible Futures tools to design this app")
        print("   → Validate: Does generated code work? How much human intervention?")
        print()
        print("5. [CRITICAL 0.70] Do users want early monetization push?")
        print("   → Test: Interview users about current pain")
        print("   → Ask: 'Should I help you perfect or monetize first?'")
        print("   → Validate: Observe behavior in early version")
        print()
        print("MINIMUM TO ADVANCE: Validate 80% of critical assumptions (4 out of 5)")
        print()
    
    # ========================================================================
    # STEP 7: Export Requirements
    # ========================================================================
    
    print("7. REQUIREMENTS SUMMARY")
    print("=" * 80)
    print()
    print("KNOWN COMPONENTS (High Confidence):")
    print("  ✓ Possible Futures Engine (1.0) - Already built!")
    print("  ✓ Content Ingestion (0.9) - Have foundation")
    print("  ✓ Business State Monitor (0.85) - Have architecture")
    print("  ✓ Dashboard UI (0.85) - Standard patterns")
    print("  ✓ Chat Interface (0.8) - Known tech")
    print()
    print("UNKNOWN COMPONENTS (Lower Confidence - Need R&D):")
    print("  ? Quick Capture (0.7) - Multiple integrations complex")
    print("  ? Self-Building Webapp (0.6) - Novel, unproven")
    print()
    print("CRITICAL UNKNOWNS (Need Validation Before Building):")
    print("  ! Will users share content? (0.95)")
    print("  ! Will users engage as cofounder? (0.90)")
    print("  ! Will market pay $50-200/mo? (0.85)")
    print("  ! Can AI build own webapp? (0.75)")
    print("  ! Do users want monetization push? (0.70)")
    print()
    print("MEASURABLE SUCCESS CRITERIA:")
    print("  → Build MVP in 7 days")
    print("  → 100 users in 30 days")
    print("  → 70% engage 3x/week")
    print("  → 5 futures/user/month")
    print("  → 20% paid conversion")
    print("  → 50% make money from AI help")
    print("  → 60% retention at month 2")
    print()
    print("CURRENT STATUS:")
    print(f"  Stage: REQUIREMENTS")
    print(f"  Uncertainty: VERY_HIGH")
    print(f"  Health: {health['overall_health_score']:.2f}")
    print(f"  Blockers: {health['critical_assumptions_count']} critical assumptions unvalidated")
    print()
    print("=" * 80)
    print("Requirements saved to Possible Futures database.")
    print(f"Idea ID: {idea_id}")
    print()
    print("Next: Validate critical assumptions, then advance to ANALYSIS stage.")
    print("=" * 80)
    
    return idea_id


if __name__ == "__main__":
    print()
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 23 + "AI COFOUNDER APP REQUIREMENTS" + " " * 25 + "║")
    print("║" + " " * 78 + "║")
    print("║" + " " * 15 + "Using Possible Futures to Define Itself" + " " * 23 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    idea_id = spawn_ai_cofounder_idea()
    
    print()
    print("✨ Requirements specification complete!")
    print()
    print("This idea is now tracked in the Possible Futures system.")
    print(f"Database: ./data/possible_futures/{idea_id}_requirements.db")
    print()
    print("To view the complete specification:")
    print(f"  python -c \"from tasks.idea_tools import get_idea_status; print(get_idea_status('{idea_id}'))\"")
    print()

