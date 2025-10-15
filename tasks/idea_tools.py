"""
Tools for AI Model to Spawn and Manage Ideas

These are the tools that will be available to the trained model
to create and evolve possible futures.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import os
from .possible_futures import (
    PossibleFuturesEngine,
    WaterfallStage,
    GoalValidator,
    ValidatorResult
)


# ============================================================================
# Global Engine Instance
# ============================================================================

_engine: Optional[PossibleFuturesEngine] = None


def get_engine() -> PossibleFuturesEngine:
    """Get or create the global engine instance"""
    global _engine
    if _engine is None:
        data_dir = os.path.join(os.getcwd(), "data", "possible_futures")
        os.makedirs(data_dir, exist_ok=True)
        _engine = PossibleFuturesEngine(base_db_path=data_dir)
        _register_default_validators(_engine.validator)
    return _engine


# ============================================================================
# Model Tools - These are exposed to the AI
# ============================================================================

def create_idea(
    name: str,
    description: str,
    parent_idea_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Tool: Create a new possible future idea
    
    Args:
        name: Short name for the idea
        description: Detailed description of what this future looks like
        parent_idea_id: Optional ID of parent idea (for branching futures)
    
    Returns:
        Dictionary with idea details including ID
    """
    engine = get_engine()
    idea = engine.spawn_idea(name, description, parent_idea_id)
    
    return {
        "id": idea.id,
        "name": idea.name,
        "description": idea.description,
        "created_at": idea.created_at.isoformat(),
        "current_stage": idea.current_stage.value,
        "uncertainty_level": idea.uncertainty_level.value,
        "parent_idea_id": idea.parent_idea_id
    }


def add_system_component(
    idea_id: str,
    component_name: str,
    component_type: str,
    specification: Dict[str, Any],
    confidence: float = 0.8
) -> Dict[str, Any]:
    """
    Tool: Add a known component to the system
    
    Args:
        idea_id: ID of the idea
        component_name: Name of the component (e.g., "user_auth_api")
        component_type: Type of component ("api", "database", "ui", "business_logic", "integration")
        specification: Detailed spec as a dictionary
        confidence: Confidence level 0.0-1.0 in this knowledge
    
    Returns:
        Dictionary with component details
    """
    engine = get_engine()
    idea = engine.active_ideas.get(idea_id)
    
    if not idea:
        raise ValueError(f"Idea {idea_id} not found")
    
    knowledge = engine.add_knowledge_to_idea(
        idea_id=idea_id,
        stage=idea.current_stage,
        component_name=component_name,
        component_type=component_type,
        specification=specification,
        confidence=confidence
    )
    
    return {
        "idea_id": knowledge.idea_id,
        "stage": knowledge.stage.value,
        "component_name": knowledge.component_name,
        "component_type": knowledge.component_type,
        "specification": knowledge.specification,
        "confidence": knowledge.confidence
    }


def add_world_assumption(
    idea_id: str,
    assumption_text: str,
    category: str,
    criticality: float = 0.5
) -> Dict[str, Any]:
    """
    Tool: Add an assumption about the world
    
    Args:
        idea_id: ID of the idea
        assumption_text: The assumption (e.g., "Users will adopt OAuth2 authentication")
        category: Category ("user_behavior", "market", "technology", "regulations", "resources")
        criticality: How critical is this assumption (0.0-1.0)
    
    Returns:
        Dictionary with assumption details
    """
    engine = get_engine()
    
    assumption = engine.add_assumption_to_idea(
        idea_id=idea_id,
        assumption_text=assumption_text,
        category=category,
        criticality=criticality
    )
    
    return {
        "idea_id": assumption.idea_id,
        "assumption_text": assumption.assumption_text,
        "category": assumption.category,
        "criticality": assumption.criticality,
        "validated": assumption.validated
    }


def add_goal(
    idea_id: str,
    goal_text: str,
    metric_name: str,
    target_value: Any,
    validator_function: str
) -> Dict[str, Any]:
    """
    Tool: Add a goal to achieve
    
    Args:
        idea_id: ID of the idea
        goal_text: Description of the goal
        metric_name: Name of the metric to measure
        target_value: Target value for the metric
        validator_function: Name of the validator function to use
    
    Returns:
        Dictionary with goal details
    """
    engine = get_engine()
    
    goal = engine.add_goal_to_idea(
        idea_id=idea_id,
        goal_text=goal_text,
        metric_name=metric_name,
        target_value=target_value,
        validator_function=validator_function
    )
    
    return {
        "idea_id": goal.idea_id,
        "goal_text": goal.goal_text,
        "metric_name": goal.metric_name,
        "target_value": goal.target_value,
        "validator_function": goal.validator_function,
        "status": goal.status.value
    }


def check_goals(idea_id: str, current_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool: Validate if goals are being achieved
    
    Args:
        idea_id: ID of the idea
        current_metrics: Dictionary of current metric values
    
    Returns:
        Dictionary with validation results for each goal
    """
    engine = get_engine()
    
    # Get goals to add metric_name to context
    idea = engine.active_ideas.get(idea_id)
    if not idea:
        raise ValueError(f"Idea {idea_id} not found")
    
    stage_db = engine.stage_dbs[idea_id][idea.current_stage]
    goals = stage_db.get_all_goals()
    
    results_dict = {}
    for goal in goals:
        # Add metric_name to context for each goal
        context = {**current_metrics, "metric_name": goal.metric_name}
        result = engine.validator.validate(goal, context)
        results_dict[goal.goal_text] = {
            "passed": result.passed,
            "actual_value": result.actual_value,
            "message": result.message
        }
    
    return results_dict


def get_idea_status(idea_id: str) -> Dict[str, Any]:
    """
    Tool: Get current status and health of an idea
    
    Args:
        idea_id: ID of the idea
    
    Returns:
        Dictionary with comprehensive status information
    """
    engine = get_engine()
    
    idea = engine.active_ideas.get(idea_id)
    if not idea:
        raise ValueError(f"Idea {idea_id} not found")
    
    health = engine.get_idea_health(idea_id)
    
    return {
        "idea": {
            "id": idea.id,
            "name": idea.name,
            "description": idea.description,
            "current_stage": idea.current_stage.value,
            "uncertainty_level": idea.uncertainty_level.value
        },
        "health": health
    }


def advance_idea_stage(idea_id: str) -> Dict[str, Any]:
    """
    Tool: Try to advance idea to next waterfall stage
    
    Args:
        idea_id: ID of the idea
    
    Returns:
        Dictionary indicating success and new stage
    """
    engine = get_engine()
    
    idea = engine.active_ideas.get(idea_id)
    if not idea:
        raise ValueError(f"Idea {idea_id} not found")
    
    old_stage = idea.current_stage
    success = engine.advance_stage(idea_id)
    
    return {
        "success": success,
        "previous_stage": old_stage.value,
        "current_stage": idea.current_stage.value if success else old_stage.value,
        "message": "Advanced to next stage" if success else "Cannot advance yet - requirements not met"
    }


def list_all_ideas() -> List[Dict[str, Any]]:
    """
    Tool: List all active ideas
    
    Returns:
        List of idea summaries
    """
    engine = get_engine()
    
    return [
        {
            "id": idea.id,
            "name": idea.name,
            "description": idea.description,
            "current_stage": idea.current_stage.value,
            "uncertainty_level": idea.uncertainty_level.value,
            "parent_idea_id": idea.parent_idea_id
        }
        for idea in engine.active_ideas.values()
    ]


def get_stage_history(idea_id: str, stage: str) -> Dict[str, Any]:
    """
    Tool: Get complete history of a stage (event sourcing)
    
    Args:
        idea_id: ID of the idea
        stage: Name of the stage ("requirements", "analysis", etc.)
    
    Returns:
        Dictionary with initial state and all changes
    """
    engine = get_engine()
    
    stage_enum = WaterfallStage(stage)
    stage_db = engine.stage_dbs[idea_id][stage_enum]
    
    cursor = stage_db.conn.cursor()
    
    # Get initial state
    cursor.execute("SELECT state_data, created_at FROM initial_state WHERE idea_id = ?", (idea_id,))
    initial_row = cursor.fetchone()
    
    # Get all changes
    cursor.execute("""
        SELECT change_id, timestamp, change_type, change_data
        FROM state_changes
        WHERE idea_id = ? AND stage = ?
        ORDER BY timestamp ASC
    """, (idea_id, stage))
    
    changes = []
    for row in cursor.fetchall():
        import json
        changes.append({
            "change_id": row[0],
            "timestamp": row[1],
            "change_type": row[2],
            "change_data": json.loads(row[3])
        })
    
    # Get current state
    current_state = stage_db.compute_current_state()
    
    return {
        "initial_state": json.loads(initial_row[0]) if initial_row else {},
        "initial_state_created": initial_row[1] if initial_row else None,
        "changes": changes,
        "current_state": current_state
    }


# ============================================================================
# Default Validators
# ============================================================================

def _register_default_validators(validator: GoalValidator):
    """Register default validator functions"""
    
    def numeric_threshold_validator(target_value: float, context: Dict[str, Any]) -> ValidatorResult:
        """Check if a numeric metric meets or exceeds threshold"""
        metric_name = context.get("metric_name")
        if not metric_name:
            return ValidatorResult(False, None, "No metric_name in context")
        
        actual = context.get(metric_name)
        if actual is None:
            return ValidatorResult(False, None, f"Metric {metric_name} not found in context")
        
        passed = actual >= target_value
        message = f"{metric_name}: {actual} {'>='}= {target_value}" if passed else f"{metric_name}: {actual} < {target_value}"
        return ValidatorResult(passed, actual, message)
    
    def percentage_validator(target_value: float, context: Dict[str, Any]) -> ValidatorResult:
        """Check if a percentage metric meets threshold (0-100)"""
        metric_name = context.get("metric_name")
        if not metric_name:
            return ValidatorResult(False, None, "No metric_name in context")
        
        actual = context.get(metric_name)
        if actual is None:
            return ValidatorResult(False, None, f"Metric {metric_name} not found in context")
        
        passed = actual >= target_value
        message = f"{metric_name}: {actual}% {'>='}= {target_value}%" if passed else f"{metric_name}: {actual}% < {target_value}%"
        return ValidatorResult(passed, actual, message)
    
    def boolean_validator(target_value: bool, context: Dict[str, Any]) -> ValidatorResult:
        """Check if a boolean condition is met"""
        metric_name = context.get("metric_name")
        if not metric_name:
            return ValidatorResult(False, None, "No metric_name in context")
        
        actual = context.get(metric_name)
        if actual is None:
            return ValidatorResult(False, None, f"Metric {metric_name} not found in context")
        
        passed = actual == target_value
        message = f"{metric_name}: {actual} == {target_value}" if passed else f"{metric_name}: {actual} != {target_value}"
        return ValidatorResult(passed, actual, message)
    
    def list_length_validator(target_value: int, context: Dict[str, Any]) -> ValidatorResult:
        """Check if a list has at least N items"""
        metric_name = context.get("metric_name")
        if not metric_name:
            return ValidatorResult(False, None, "No metric_name in context")
        
        actual_list = context.get(metric_name)
        if actual_list is None:
            return ValidatorResult(False, None, f"Metric {metric_name} not found in context")
        
        actual = len(actual_list)
        passed = actual >= target_value
        message = f"{metric_name} length: {actual} {'>='}= {target_value}" if passed else f"{metric_name} length: {actual} < {target_value}"
        return ValidatorResult(passed, actual, message)
    
    # Register validators
    validator.register("numeric_threshold", numeric_threshold_validator)
    validator.register("percentage", percentage_validator)
    validator.register("boolean", boolean_validator)
    validator.register("list_length", list_length_validator)


# ============================================================================
# Tool Manifest for Model
# ============================================================================

TOOL_MANIFEST = {
    "create_idea": {
        "description": "Create a new possible future idea to explore",
        "parameters": {
            "name": "string - short name for the idea",
            "description": "string - detailed description",
            "parent_idea_id": "optional string - ID of parent idea for branching"
        }
    },
    "add_system_component": {
        "description": "Add a known component/part to the system being built",
        "parameters": {
            "idea_id": "string - ID of the idea",
            "component_name": "string - name of component",
            "component_type": "string - type: api/database/ui/business_logic/integration",
            "specification": "dict - detailed specification",
            "confidence": "float 0-1 - confidence in this knowledge"
        }
    },
    "add_world_assumption": {
        "description": "Add an assumption about the world/environment",
        "parameters": {
            "idea_id": "string - ID of the idea",
            "assumption_text": "string - the assumption",
            "category": "string - user_behavior/market/technology/regulations/resources",
            "criticality": "float 0-1 - how critical is this assumption"
        }
    },
    "add_goal": {
        "description": "Add a measurable goal to achieve",
        "parameters": {
            "idea_id": "string - ID of the idea",
            "goal_text": "string - description of goal",
            "metric_name": "string - name of metric to measure",
            "target_value": "any - target value for metric",
            "validator_function": "string - validator name (numeric_threshold/percentage/boolean/list_length)"
        }
    },
    "check_goals": {
        "description": "Validate if goals are being achieved",
        "parameters": {
            "idea_id": "string - ID of the idea",
            "current_metrics": "dict - current metric values"
        }
    },
    "get_idea_status": {
        "description": "Get comprehensive status and health of an idea",
        "parameters": {
            "idea_id": "string - ID of the idea"
        }
    },
    "advance_idea_stage": {
        "description": "Try to advance idea to next waterfall stage",
        "parameters": {
            "idea_id": "string - ID of the idea"
        }
    },
    "list_all_ideas": {
        "description": "List all active ideas",
        "parameters": {}
    },
    "get_stage_history": {
        "description": "Get complete event-sourced history of a stage",
        "parameters": {
            "idea_id": "string - ID of the idea",
            "stage": "string - stage name (requirements/analysis/design/implementation/testing/validation/deployment)"
        }
    }
}

