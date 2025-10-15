"""
Possible Futures System - Based on "Out of the Tar Pit" FRP Architecture

This system allows spawning "ideas" (possible futures) that evolve through
a waterfall process with event-sourced state management.

Core Principles (from Out of the Tar Pit):
1. Separate Essential State, Essential Logic, and Accidental State/Control
2. Use relational model for all state
3. Event sourcing: state = f(initial_state, changes)
4. Each waterfall stage has independent SQLite DB
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
from datetime import datetime
import sqlite3
import json
import hashlib


# ============================================================================
# ESSENTIAL STATE - Core Types and Relations
# ============================================================================

class WaterfallStage(Enum):
    """The stages of the waterfall process for system development"""
    REQUIREMENTS = "requirements"
    ANALYSIS = "analysis"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"


class UncertaintyLevel(Enum):
    """Uncertainty decreases as we move through waterfall stages"""
    VERY_HIGH = "very_high"  # Requirements stage
    HIGH = "high"             # Analysis stage
    MEDIUM = "medium"         # Design stage
    LOW = "low"               # Implementation stage
    VERY_LOW = "very_low"     # Testing stage
    MINIMAL = "minimal"       # Validation/Deployment


class GoalStatus(Enum):
    """Status of goal achievement"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Idea:
    """
    A Possible Future - a hypothesis about a future state of a system
    
    Essential State only - no accidental complexity
    """
    id: str  # Unique identifier
    name: str
    description: str
    created_at: datetime
    current_stage: WaterfallStage
    uncertainty_level: UncertaintyLevel
    parent_idea_id: Optional[str] = None  # Ideas can branch from other ideas
    
    def __post_init__(self):
        if not self.id:
            # Generate deterministic ID from content
            content = f"{self.name}:{self.description}:{self.created_at.isoformat()}"
            self.id = hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class SystemKnowledge:
    """
    Known parts of the system being built
    
    Represents what we KNOW (as opposed to assumptions about unknowns)
    """
    idea_id: str
    stage: WaterfallStage
    component_name: str
    component_type: str  # e.g., "api", "database", "ui", "business_logic"
    specification: Dict[str, Any]  # JSON-serializable spec
    confidence: float  # 0.0 to 1.0 - how confident are we in this knowledge
    created_at: datetime
    updated_at: datetime


@dataclass
class WorldAssumption:
    """
    Assumptions about the world containing the system
    
    These are HYPOTHESES that need validation
    """
    idea_id: str
    assumption_text: str
    category: str  # e.g., "user_behavior", "market", "technology", "regulations"
    criticality: float  # 0.0 to 1.0 - how critical is this assumption
    validated: bool = False
    validation_evidence: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Goal:
    """
    Goals for the system to achieve
    
    These are MEASURABLE outcomes we want
    """
    idea_id: str
    goal_text: str
    metric_name: str
    target_value: Any  # The target we're trying to hit
    current_value: Optional[Any] = None
    status: GoalStatus = GoalStatus.NOT_STARTED
    validator_function: Optional[str] = None  # Name of validator function
    created_at: Optional[datetime] = None
    achieved_at: Optional[datetime] = None


@dataclass
class StateChange:
    """
    Event sourcing: Each change to state is recorded as an event
    
    New state = f(initial_state, all_changes)
    """
    change_id: str
    idea_id: str
    stage: WaterfallStage
    timestamp: datetime
    change_type: str  # e.g., "requirement_added", "assumption_validated", "goal_achieved"
    change_data: Dict[str, Any]  # JSON payload of the change
    previous_state_hash: str  # Hash of state before this change
    new_state_hash: str  # Hash of state after this change
    
    def __post_init__(self):
        if not self.change_id:
            content = f"{self.idea_id}:{self.timestamp.isoformat()}:{self.change_type}"
            self.change_id = hashlib.sha256(content.encode()).hexdigest()[:16]


# ============================================================================
# ESSENTIAL LOGIC - Functions and Relations
# ============================================================================

class ValidatorResult:
    """Result of running a validator function"""
    def __init__(self, passed: bool, actual_value: Any, message: str):
        self.passed = passed
        self.actual_value = actual_value
        self.message = message


class GoalValidator:
    """
    Validator system for checking if goals are achieved
    
    Pure functions only - no side effects
    """
    
    def __init__(self):
        self.validators: Dict[str, Callable] = {}
    
    def register(self, name: str, validator_fn: Callable[[Any, Any], ValidatorResult]):
        """Register a validator function"""
        self.validators[name] = validator_fn
    
    def validate(self, goal: Goal, context: Dict[str, Any]) -> ValidatorResult:
        """
        Validate if a goal is achieved
        
        Pure function: same inputs always give same output
        """
        if not goal.validator_function:
            return ValidatorResult(False, None, "No validator function specified")
        
        if goal.validator_function not in self.validators:
            return ValidatorResult(False, None, f"Validator '{goal.validator_function}' not found")
        
        validator_fn = self.validators[goal.validator_function]
        return validator_fn(goal.target_value, context)


def compute_uncertainty(stage: WaterfallStage, validated_assumptions: int, total_assumptions: int) -> UncertaintyLevel:
    """
    Pure function: compute uncertainty level based on stage and assumption validation
    
    Uncertainty decreases as:
    1. We progress through waterfall stages
    2. We validate more assumptions
    """
    base_uncertainty = {
        WaterfallStage.REQUIREMENTS: 5,
        WaterfallStage.ANALYSIS: 4,
        WaterfallStage.DESIGN: 3,
        WaterfallStage.IMPLEMENTATION: 2,
        WaterfallStage.TESTING: 1,
        WaterfallStage.VALIDATION: 0,
        WaterfallStage.DEPLOYMENT: 0,
    }[stage]
    
    # Reduce uncertainty based on validated assumptions
    if total_assumptions > 0:
        validation_ratio = validated_assumptions / total_assumptions
        adjustment = int((1 - validation_ratio) * 2)
    else:
        adjustment = 0
    
    uncertainty_score = base_uncertainty + adjustment
    
    if uncertainty_score >= 5:
        return UncertaintyLevel.VERY_HIGH
    elif uncertainty_score >= 4:
        return UncertaintyLevel.HIGH
    elif uncertainty_score >= 3:
        return UncertaintyLevel.MEDIUM
    elif uncertainty_score >= 2:
        return UncertaintyLevel.LOW
    elif uncertainty_score >= 1:
        return UncertaintyLevel.VERY_LOW
    else:
        return UncertaintyLevel.MINIMAL


def compute_state_hash(state_data: Dict[str, Any]) -> str:
    """
    Pure function: compute deterministic hash of state
    
    Used for event sourcing to track state changes
    """
    # Sort keys for deterministic hashing
    canonical = json.dumps(state_data, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def derive_system_health(
    knowledge_items: List[SystemKnowledge],
    assumptions: List[WorldAssumption],
    goals: List[Goal]
) -> Dict[str, Any]:
    """
    Pure function: derive overall health metrics of a possible future
    
    This is a DERIVED RELATION in FRP terms - computed from essential state
    """
    total_knowledge = len(knowledge_items)
    avg_confidence = sum(k.confidence for k in knowledge_items) / total_knowledge if total_knowledge > 0 else 0.0
    
    total_assumptions = len(assumptions)
    validated_assumptions = sum(1 for a in assumptions if a.validated)
    critical_assumptions = [a for a in assumptions if a.criticality > 0.7]
    critical_validated = sum(1 for a in critical_assumptions if a.validated)
    
    total_goals = len(goals)
    achieved_goals = sum(1 for g in goals if g.status == GoalStatus.ACHIEVED)
    failed_goals = sum(1 for g in goals if g.status == GoalStatus.FAILED)
    
    return {
        "total_knowledge_items": total_knowledge,
        "average_confidence": avg_confidence,
        "total_assumptions": total_assumptions,
        "validated_assumptions": validated_assumptions,
        "assumption_validation_rate": validated_assumptions / total_assumptions if total_assumptions > 0 else 0.0,
        "critical_assumptions_count": len(critical_assumptions),
        "critical_assumptions_validated": critical_validated,
        "total_goals": total_goals,
        "achieved_goals": achieved_goals,
        "failed_goals": failed_goals,
        "goal_achievement_rate": achieved_goals / total_goals if total_goals > 0 else 0.0,
        "overall_health_score": (
            (avg_confidence * 0.3) +
            ((validated_assumptions / total_assumptions if total_assumptions > 0 else 0) * 0.4) +
            ((achieved_goals / total_goals if total_goals > 0 else 0) * 0.3)
        )
    }


# ============================================================================
# ACCIDENTAL STATE AND CONTROL - Performance Hints and Storage
# ============================================================================

class StageDatabase:
    """
    SQLite database for a single waterfall stage
    
    Event-sourced: stores initial state + all changes
    New state computed as function of (initial_state, changes)
    """
    
    def __init__(self, idea_id: str, stage: WaterfallStage, db_path: str):
        self.idea_id = idea_id
        self.stage = stage
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._initialize_schema()
    
    def _initialize_schema(self):
        """
        Create tables for event sourcing
        
        Following relational model from "Out of the Tar Pit"
        """
        cursor = self.conn.cursor()
        
        # Initial state snapshot
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS initial_state (
                idea_id TEXT PRIMARY KEY,
                stage TEXT NOT NULL,
                state_data TEXT NOT NULL,  -- JSON
                state_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # All changes (events)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS state_changes (
                change_id TEXT PRIMARY KEY,
                idea_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                change_type TEXT NOT NULL,
                change_data TEXT NOT NULL,  -- JSON
                previous_state_hash TEXT NOT NULL,
                new_state_hash TEXT NOT NULL,
                FOREIGN KEY (idea_id) REFERENCES initial_state(idea_id)
            )
        """)
        
        # Knowledge items for this stage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id TEXT NOT NULL,
                stage TEXT NOT NULL,
                component_name TEXT NOT NULL,
                component_type TEXT NOT NULL,
                specification TEXT NOT NULL,  -- JSON
                confidence REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Assumptions for this stage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS world_assumptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id TEXT NOT NULL,
                assumption_text TEXT NOT NULL,
                category TEXT NOT NULL,
                criticality REAL NOT NULL,
                validated INTEGER NOT NULL DEFAULT 0,
                validation_evidence TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Goals for this stage
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id TEXT NOT NULL,
                goal_text TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                target_value TEXT NOT NULL,  -- JSON
                current_value TEXT,  -- JSON
                status TEXT NOT NULL,
                validator_function TEXT,
                created_at TEXT NOT NULL,
                achieved_at TEXT
            )
        """)
        
        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_changes_idea ON state_changes(idea_id, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_idea ON system_knowledge(idea_id, stage)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assumptions_idea ON world_assumptions(idea_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_goals_idea ON goals(idea_id, status)")
        
        self.conn.commit()
    
    def record_initial_state(self, state_data: Dict[str, Any]):
        """Record the initial state for this stage"""
        state_hash = compute_state_hash(state_data)
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO initial_state (idea_id, stage, state_data, state_hash, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.idea_id,
            self.stage.value,
            json.dumps(state_data),
            state_hash,
            datetime.now().isoformat()
        ))
        self.conn.commit()
        return state_hash
    
    def record_change(self, change: StateChange):
        """Record a state change event"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO state_changes (
                change_id, idea_id, stage, timestamp, change_type,
                change_data, previous_state_hash, new_state_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            change.change_id,
            change.idea_id,
            change.stage.value,
            change.timestamp.isoformat(),
            change.change_type,
            json.dumps(change.change_data),
            change.previous_state_hash,
            change.new_state_hash
        ))
        self.conn.commit()
    
    def compute_current_state(self) -> Dict[str, Any]:
        """
        Compute current state as function of initial state + all changes
        
        Pure function: state = f(initial_state, changes)
        """
        cursor = self.conn.cursor()
        
        # Get initial state
        cursor.execute("""
            SELECT state_data FROM initial_state WHERE idea_id = ?
        """, (self.idea_id,))
        row = cursor.fetchone()
        
        if not row:
            return {}
        
        state = json.loads(row[0])
        
        # Apply all changes in order
        cursor.execute("""
            SELECT change_data FROM state_changes
            WHERE idea_id = ? AND stage = ?
            ORDER BY timestamp ASC
        """, (self.idea_id, self.stage.value))
        
        for (change_data_json,) in cursor.fetchall():
            change_data = json.loads(change_data_json)
            state = self._apply_change(state, change_data)
        
        return state
    
    def _apply_change(self, state: Dict[str, Any], change: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply a change to state
        
        Pure function - does not mutate state
        """
        new_state = state.copy()
        
        # Deep merge change into state
        for key, value in change.items():
            if key in new_state and isinstance(new_state[key], dict) and isinstance(value, dict):
                # Recursive merge for nested dicts
                new_state[key] = {**new_state[key], **value}
            else:
                new_state[key] = value
        
        return new_state
    
    def add_knowledge(self, knowledge: SystemKnowledge):
        """Add a knowledge item"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO system_knowledge (
                idea_id, stage, component_name, component_type,
                specification, confidence, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            knowledge.idea_id,
            knowledge.stage.value,
            knowledge.component_name,
            knowledge.component_type,
            json.dumps(knowledge.specification),
            knowledge.confidence,
            knowledge.created_at.isoformat(),
            knowledge.updated_at.isoformat()
        ))
        self.conn.commit()
    
    def add_assumption(self, assumption: WorldAssumption):
        """Add a world assumption"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO world_assumptions (
                idea_id, assumption_text, category, criticality,
                validated, validation_evidence, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            assumption.idea_id,
            assumption.assumption_text,
            assumption.category,
            assumption.criticality,
            1 if assumption.validated else 0,
            assumption.validation_evidence,
            (assumption.created_at or datetime.now()).isoformat()
        ))
        self.conn.commit()
    
    def add_goal(self, goal: Goal):
        """Add a goal"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO goals (
                idea_id, goal_text, metric_name, target_value,
                current_value, status, validator_function, created_at, achieved_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            goal.idea_id,
            goal.goal_text,
            goal.metric_name,
            json.dumps(goal.target_value),
            json.dumps(goal.current_value) if goal.current_value is not None else None,
            goal.status.value,
            goal.validator_function,
            (goal.created_at or datetime.now()).isoformat(),
            goal.achieved_at.isoformat() if goal.achieved_at else None
        ))
        self.conn.commit()
    
    def get_all_knowledge(self) -> List[SystemKnowledge]:
        """Retrieve all knowledge items"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT idea_id, stage, component_name, component_type,
                   specification, confidence, created_at, updated_at
            FROM system_knowledge WHERE idea_id = ?
        """, (self.idea_id,))
        
        items = []
        for row in cursor.fetchall():
            items.append(SystemKnowledge(
                idea_id=row[0],
                stage=WaterfallStage(row[1]),
                component_name=row[2],
                component_type=row[3],
                specification=json.loads(row[4]),
                confidence=row[5],
                created_at=datetime.fromisoformat(row[6]),
                updated_at=datetime.fromisoformat(row[7])
            ))
        return items
    
    def get_all_assumptions(self) -> List[WorldAssumption]:
        """Retrieve all assumptions"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT idea_id, assumption_text, category, criticality,
                   validated, validation_evidence, created_at
            FROM world_assumptions WHERE idea_id = ?
        """, (self.idea_id,))
        
        items = []
        for row in cursor.fetchall():
            items.append(WorldAssumption(
                idea_id=row[0],
                assumption_text=row[1],
                category=row[2],
                criticality=row[3],
                validated=bool(row[4]),
                validation_evidence=row[5],
                created_at=datetime.fromisoformat(row[6])
            ))
        return items
    
    def get_all_goals(self) -> List[Goal]:
        """Retrieve all goals"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT idea_id, goal_text, metric_name, target_value,
                   current_value, status, validator_function, created_at, achieved_at
            FROM goals WHERE idea_id = ?
        """, (self.idea_id,))
        
        items = []
        for row in cursor.fetchall():
            items.append(Goal(
                idea_id=row[0],
                goal_text=row[1],
                metric_name=row[2],
                target_value=json.loads(row[3]),
                current_value=json.loads(row[4]) if row[4] else None,
                status=GoalStatus(row[5]),
                validator_function=row[6],
                created_at=datetime.fromisoformat(row[7]) if row[7] else None,
                achieved_at=datetime.fromisoformat(row[8]) if row[8] else None
            ))
        return items
    
    def close(self):
        """Close database connection"""
        self.conn.close()


# ============================================================================
# TOOLS API - For Model to Spawn and Manage Ideas
# ============================================================================

class PossibleFuturesEngine:
    """
    Main engine for creating and managing possible futures
    
    This is what the trained model will interact with
    """
    
    def __init__(self, base_db_path: str = "./data/possible_futures"):
        self.base_db_path = base_db_path
        self.validator = GoalValidator()
        self.active_ideas: Dict[str, Idea] = {}
        self.stage_dbs: Dict[str, Dict[WaterfallStage, StageDatabase]] = {}
    
    def spawn_idea(
        self,
        name: str,
        description: str,
        parent_idea_id: Optional[str] = None
    ) -> Idea:
        """
        Spawn a new possible future
        
        This is the primary tool for the model to create new ideas
        """
        idea = Idea(
            id="",  # Will be generated
            name=name,
            description=description,
            created_at=datetime.now(),
            current_stage=WaterfallStage.REQUIREMENTS,
            uncertainty_level=UncertaintyLevel.VERY_HIGH,
            parent_idea_id=parent_idea_id
        )
        
        self.active_ideas[idea.id] = idea
        
        # Initialize databases for all stages
        self.stage_dbs[idea.id] = {}
        for stage in WaterfallStage:
            db_path = f"{self.base_db_path}/{idea.id}_{stage.value}.db"
            stage_db = StageDatabase(idea.id, stage, db_path)
            
            # Record initial empty state
            stage_db.record_initial_state({
                "idea_id": idea.id,
                "stage": stage.value,
                "knowledge": [],
                "assumptions": [],
                "goals": []
            })
            
            self.stage_dbs[idea.id][stage] = stage_db
        
        return idea
    
    def add_knowledge_to_idea(
        self,
        idea_id: str,
        stage: WaterfallStage,
        component_name: str,
        component_type: str,
        specification: Dict[str, Any],
        confidence: float
    ) -> SystemKnowledge:
        """Add knowledge about the system to an idea"""
        knowledge = SystemKnowledge(
            idea_id=idea_id,
            stage=stage,
            component_name=component_name,
            component_type=component_type,
            specification=specification,
            confidence=confidence,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        stage_db = self.stage_dbs[idea_id][stage]
        stage_db.add_knowledge(knowledge)
        
        # Record as state change
        self._record_change(idea_id, stage, "knowledge_added", {
            "component_name": component_name,
            "component_type": component_type,
            "confidence": confidence
        })
        
        return knowledge
    
    def add_assumption_to_idea(
        self,
        idea_id: str,
        assumption_text: str,
        category: str,
        criticality: float
    ) -> WorldAssumption:
        """Add an assumption about the world to an idea"""
        assumption = WorldAssumption(
            idea_id=idea_id,
            assumption_text=assumption_text,
            category=category,
            criticality=criticality,
            validated=False,
            created_at=datetime.now()
        )
        
        # Add to current stage
        idea = self.active_ideas[idea_id]
        stage_db = self.stage_dbs[idea_id][idea.current_stage]
        stage_db.add_assumption(assumption)
        
        # Record as state change
        self._record_change(idea_id, idea.current_stage, "assumption_added", {
            "assumption_text": assumption_text,
            "category": category,
            "criticality": criticality
        })
        
        return assumption
    
    def add_goal_to_idea(
        self,
        idea_id: str,
        goal_text: str,
        metric_name: str,
        target_value: Any,
        validator_function: str
    ) -> Goal:
        """Add a goal to an idea"""
        goal = Goal(
            idea_id=idea_id,
            goal_text=goal_text,
            metric_name=metric_name,
            target_value=target_value,
            validator_function=validator_function,
            created_at=datetime.now()
        )
        
        # Add to current stage
        idea = self.active_ideas[idea_id]
        stage_db = self.stage_dbs[idea_id][idea.current_stage]
        stage_db.add_goal(goal)
        
        # Record as state change
        self._record_change(idea_id, idea.current_stage, "goal_added", {
            "goal_text": goal_text,
            "metric_name": metric_name,
            "target_value": target_value
        })
        
        return goal
    
    def advance_stage(self, idea_id: str) -> bool:
        """
        Move idea to next waterfall stage
        
        Only allowed if current stage is sufficiently complete
        """
        idea = self.active_ideas[idea_id]
        
        # Check if can advance
        if not self._can_advance_stage(idea):
            return False
        
        # Advance to next stage
        stages = list(WaterfallStage)
        current_idx = stages.index(idea.current_stage)
        
        if current_idx < len(stages) - 1:
            new_stage = stages[current_idx + 1]
            idea.current_stage = new_stage
            
            # Update uncertainty
            stage_db = self.stage_dbs[idea_id][new_stage]
            assumptions = stage_db.get_all_assumptions()
            validated = sum(1 for a in assumptions if a.validated)
            idea.uncertainty_level = compute_uncertainty(new_stage, validated, len(assumptions))
            
            # Record change
            self._record_change(idea_id, new_stage, "stage_advanced", {
                "new_stage": new_stage.value,
                "uncertainty_level": idea.uncertainty_level.value
            })
            
            return True
        
        return False
    
    def validate_goals(self, idea_id: str, context: Dict[str, Any]) -> Dict[str, ValidatorResult]:
        """
        Run validators on all goals for an idea
        
        Returns dict of goal_text -> ValidatorResult
        """
        idea = self.active_ideas[idea_id]
        stage_db = self.stage_dbs[idea_id][idea.current_stage]
        goals = stage_db.get_all_goals()
        
        results = {}
        for goal in goals:
            result = self.validator.validate(goal, context)
            results[goal.goal_text] = result
            
            # Update goal status if needed
            if result.passed and goal.status != GoalStatus.ACHIEVED:
                # Record achievement
                self._record_change(idea_id, idea.current_stage, "goal_achieved", {
                    "goal_text": goal.goal_text,
                    "metric_name": goal.metric_name,
                    "actual_value": result.actual_value
                })
        
        return results
    
    def get_idea_health(self, idea_id: str) -> Dict[str, Any]:
        """
        Get health metrics for an idea
        
        This is a derived relation - computed from essential state
        """
        idea = self.active_ideas[idea_id]
        stage_db = self.stage_dbs[idea_id][idea.current_stage]
        
        knowledge = stage_db.get_all_knowledge()
        assumptions = stage_db.get_all_assumptions()
        goals = stage_db.get_all_goals()
        
        return derive_system_health(knowledge, assumptions, goals)
    
    def _can_advance_stage(self, idea: Idea) -> bool:
        """Check if idea can advance to next stage"""
        stage_db = self.stage_dbs[idea.id][idea.current_stage]
        
        # Must have at least some knowledge
        knowledge = stage_db.get_all_knowledge()
        if not knowledge:
            return False
        
        # Critical assumptions must be validated
        assumptions = stage_db.get_all_assumptions()
        critical_assumptions = [a for a in assumptions if a.criticality > 0.7]
        critical_validated = sum(1 for a in critical_assumptions if a.validated)
        
        if critical_assumptions and critical_validated < len(critical_assumptions) * 0.8:
            return False
        
        return True
    
    def _record_change(self, idea_id: str, stage: WaterfallStage, change_type: str, change_data: Dict[str, Any]):
        """Record a state change event"""
        stage_db = self.stage_dbs[idea_id][stage]
        current_state = stage_db.compute_current_state()
        prev_hash = compute_state_hash(current_state)
        
        # Apply change
        new_state = stage_db._apply_change(current_state, change_data)
        new_hash = compute_state_hash(new_state)
        
        change = StateChange(
            change_id="",  # Will be generated
            idea_id=idea_id,
            stage=stage,
            timestamp=datetime.now(),
            change_type=change_type,
            change_data=change_data,
            previous_state_hash=prev_hash,
            new_state_hash=new_hash
        )
        
        stage_db.record_change(change)
    
    def close_all(self):
        """Close all database connections"""
        for idea_dbs in self.stage_dbs.values():
            for stage_db in idea_dbs.values():
                stage_db.close()

