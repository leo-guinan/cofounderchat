"""
Conscious Economics Calculation Tools

Implements Time Violence metrics, Consciousness Index, Time Dividends,
and Conscious ROI calculations based on the Conscious Economics framework.

These functions are designed to be called by the AI model during inference,
similar to the calculator tool in engine.py, to provide auditable computations
of time-based value and system consciousness.

Reference: Conscious Economics whitepaper (Time Violence formalization)
"""

import math
from typing import Dict, Union, Optional


# =============================================================================
# Time Violence Calculations
# =============================================================================

def tv_ops(
    arr_rate: float,
    svc_rate: float,
    var_arr: float,
    var_svc: float,
    tau: float
) -> float:
    """
    Calculate Operational Time Violence Score.
    
    Operational TV measures the time cost of uncertainty and mismatch
    between arrival and service in a system (queue theory applied to human time).
    
    Formula:
        TV_ops = (λ/μ) × √(σ²_arr + σ²_svc) × τ
    
    Where:
        λ (arr_rate): arrival rate (requests/tasks per unit time)
        μ (svc_rate): service rate (capacity to handle requests per unit time)
        σ²_arr (var_arr): variance in arrival rate
        σ²_svc (var_svc): variance in service rate
        τ (tau): time horizon (how long the system runs)
    
    Args:
        arr_rate: Arrival rate of requests/tasks (e.g., 10 requests/hour)
        svc_rate: Service rate / processing capacity (e.g., 12 requests/hour)
        var_arr: Variance in arrival rate
        var_svc: Variance in service rate
        tau: Time horizon for measurement (e.g., hours, days)
    
    Returns:
        Operational Time Violence score (in time units matching tau)
    
    Example:
        >>> tv_ops(arr_rate=10, svc_rate=12, var_arr=4, var_svc=2, tau=8)
        >>> # 10 requests/hr, 12 capacity/hr, over 8 hours
        >>> # Returns: ~17.4 hours of operational time violence
    """
    if svc_rate <= 0:
        raise ValueError("Service rate must be positive")
    if arr_rate < 0 or var_arr < 0 or var_svc < 0 or tau < 0:
        raise ValueError("Rates, variances, and time must be non-negative")
    
    utilization = arr_rate / svc_rate
    variance_term = math.sqrt(var_arr + var_svc)
    ops_score = utilization * variance_term * tau
    
    return ops_score


def tv_info(
    dkl: float,
    decision_entropy: float,
    redundancy_mi: float
) -> float:
    """
    Calculate Informational Time Violence Score.
    
    Informational TV measures the cognitive time cost of:
    - Information asymmetry (KL divergence from ideal knowledge)
    - Decision complexity (entropy of decision space)
    - Redundant communication (mutual information waste)
    
    Formula:
        TV_info = D_KL + H(decision) + MI(redundancy)
    
    Where:
        D_KL: KL divergence between actual and ideal information state
        H(decision): Shannon entropy of the decision space
        MI(redundancy): Mutual information of redundant/duplicate info exchanges
    
    Args:
        dkl: KL divergence (information asymmetry cost, in bits or nats)
        decision_entropy: Shannon entropy of decision space
        redundancy_mi: Mutual information from redundant communications
    
    Returns:
        Informational Time Violence score (cognitive load metric)
    
    Example:
        >>> tv_info(dkl=2.5, decision_entropy=3.2, redundancy_mi=1.1)
        >>> # Returns: 6.8 (units of information-theoretic complexity)
    """
    if dkl < 0 or decision_entropy < 0 or redundancy_mi < 0:
        raise ValueError("Information metrics must be non-negative")
    
    info_score = dkl + decision_entropy + redundancy_mi
    
    return info_score


def tv_total(ops_score: float, info_score: float) -> float:
    """
    Calculate Total Time Violence.
    
    Formula:
        TV = TV_ops + TV_info
    
    Args:
        ops_score: Operational Time Violence (from tv_ops)
        info_score: Informational Time Violence (from tv_info)
    
    Returns:
        Total Time Violence score
    
    Example:
        >>> ops = tv_ops(10, 12, 4, 2, 8)
        >>> info = tv_info(2.5, 3.2, 1.1)
        >>> tv_total(ops, info)
        >>> # Returns: ops + info = total system time violence
    """
    return ops_score + info_score


# =============================================================================
# Consciousness Index
# =============================================================================

def conscious_index(tv_human: float, tv_total: float) -> float:
    """
    Calculate Consciousness Index of a system.
    
    The Consciousness Index measures how much of the total time violence
    is handled by humans vs. automated/delegated to systems.
    
    Higher consciousness = less human time violence (more automation/delegation).
    
    Formula:
        C(S) = 1 - (TVH / TV)
    
    Where:
        TVH: Time Violence experienced by humans
        TV: Total Time Violence in the system
    
    Returns value in [0, 1]:
        - C(S) = 0: All time violence falls on humans (unconscious system)
        - C(S) = 1: No time violence falls on humans (fully conscious system)
        - C(S) = 0.8: 80% of time violence is automated/delegated
    
    Args:
        tv_human: Time Violence experienced by human participants
        tv_total: Total Time Violence in the system
    
    Returns:
        Consciousness Index between 0 and 1
    
    Example:
        >>> conscious_index(tv_human=20, tv_total=100)
        >>> # Returns: 0.8 (80% of TV is automated/handled by systems)
    """
    if tv_human < 0 or tv_total < 0:
        raise ValueError("Time Violence values must be non-negative")
    
    if tv_total == 0:
        # Edge case: no time violence means perfect system
        return 1.0
    
    if tv_human > tv_total:
        # Edge case: human TV exceeds total (measurement error or amplification)
        # Cap at 0 (worst consciousness state)
        return 0.0
    
    c_index = 1.0 - (tv_human / tv_total)
    
    # Ensure result is in [0, 1] due to floating point errors
    return max(0.0, min(1.0, c_index))


# =============================================================================
# Time Dividends
# =============================================================================

def time_dividends(
    hours_saved: float,
    distribution: Optional[Dict[str, float]] = None
) -> Dict[str, float]:
    """
    Calculate Time Dividend distribution across stakeholders.
    
    Time Dividends (TD) are the auditable, tokenized hours returned to
    participants when a system reduces Time Violence. They represent
    ownership of saved time, not extraction of it.
    
    Default distribution (if not specified):
        - Users: 60% (those who experience the time savings directly)
        - Navigators: 20% (those who built/maintain the system)
        - Company: 20% (reinvestment in further time violence reduction)
    
    Args:
        hours_saved: Total hours of time violence reduced (ΔTVH)
        distribution: Optional custom distribution dict with keys:
            'users', 'navigators', 'company' (must sum to 1.0)
    
    Returns:
        Dict with keys ['users', 'navigators', 'company', 'total']
        showing hours allocated to each stakeholder
    
    Example:
        >>> time_dividends(hours_saved=100)
        >>> # Returns: {'users': 60.0, 'navigators': 20.0, 'company': 20.0, 'total': 100.0}
        
        >>> time_dividends(hours_saved=100, distribution={'users': 0.7, 'navigators': 0.2, 'company': 0.1})
        >>> # Returns: {'users': 70.0, 'navigators': 20.0, 'company': 10.0, 'total': 100.0}
    """
    if hours_saved < 0:
        raise ValueError("Hours saved must be non-negative")
    
    # Default distribution: Users (60%), Navigators (20%), Company (20%)
    if distribution is None:
        distribution = {
            'users': 0.60,
            'navigators': 0.20,
            'company': 0.20,
        }
    
    # Validate distribution
    required_keys = {'users', 'navigators', 'company'}
    if set(distribution.keys()) != required_keys:
        raise ValueError(f"Distribution must have keys: {required_keys}")
    
    total_pct = sum(distribution.values())
    if not math.isclose(total_pct, 1.0, abs_tol=1e-6):
        raise ValueError(f"Distribution must sum to 1.0, got {total_pct}")
    
    # Calculate allocation
    td = {
        'users': hours_saved * distribution['users'],
        'navigators': hours_saved * distribution['navigators'],
        'company': hours_saved * distribution['company'],
        'total': hours_saved,
    }
    
    return td


# =============================================================================
# Conscious ROI
# =============================================================================

def roi_conscious(
    rev: float,
    dtvh: float,
    v_t: float = 35.0,
    td: Optional[float] = None,
    delta_c: float = 0.0,
    trust: float = 0.0,
    compliance: float = 0.0,
    quality: float = 0.0,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Calculate Conscious ROI (C-ROI*).
    
    C-ROI extends traditional ROI by including:
    - Revenue impact (traditional)
    - Time value returned (conscious economics)
    - Time Dividends minted (stakeholder value)
    - Consciousness improvement (system evolution)
    - Trust, Compliance, Quality (MetaSPN factors)
    
    Formula:
        C-ROI* = α·Rev + β·(vₜ·ΔTVH) + γ·TD + δ·ΔC(S) + ε·T + ζ·X + η·Q
    
    Where:
        Rev: Revenue/profit impact ($)
        ΔTVH: Reduction in human Time Violence (hours)
        vₜ: Shadow price of time ($/hour)
        TD: Time Dividends minted (hours or $ equivalent)
        ΔC(S): Change in Consciousness Index
        T: Trust factor (evidence, reproducibility)
        X: Constraint compliance (ethics, safety)
        Q: Quality factor
        α, β, γ, δ, ε, ζ, η: Weights (default all 1.0)
    
    Args:
        rev: Revenue impact in dollars
        dtvh: Reduction in human Time Violence (hours saved)
        v_t: Shadow price of time ($/hour), default $35/hr
        td: Time Dividends (hours), defaults to dtvh if not specified
        delta_c: Change in Consciousness Index (dimensionless)
        trust: Trust factor (0-1 scale, or custom metric)
        compliance: Compliance factor (0-1 scale, or custom metric)
        quality: Quality factor (0-1 scale, or custom metric)
        weights: Optional dict with keys [alpha, beta, gamma, delta, epsilon, zeta, eta]
            Default: all weights = 1.0 (equal consideration)
    
    Returns:
        Dict containing:
            'c_roi': Total Conscious ROI value
            'components': Breakdown of each component
            'weights': Weights used in calculation
            'time_value': vₜ × ΔTVH (dollar value of time saved)
    
    Example:
        >>> roi_conscious(
        ...     rev=1000,
        ...     dtvh=50,
        ...     v_t=35,
        ...     delta_c=0.1,
        ...     trust=0.8,
        ...     compliance=1.0,
        ...     quality=0.9
        ... )
        >>> # Returns breakdown of C-ROI* calculation
    """
    # Default weights: all components equally weighted
    if weights is None:
        weights = {
            'alpha': 1.0,   # Revenue
            'beta': 1.0,    # Time value
            'gamma': 1.0,   # Time Dividends
            'delta': 1.0,   # Consciousness change
            'epsilon': 1.0, # Trust
            'zeta': 1.0,    # Compliance
            'eta': 1.0,     # Quality
        }
    
    # Validate weights
    required_weight_keys = {'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta'}
    if set(weights.keys()) != required_weight_keys:
        raise ValueError(f"Weights must have keys: {required_weight_keys}")
    
    # Default TD to hours saved if not specified
    if td is None:
        td = dtvh
    
    # Calculate time value
    time_value = v_t * dtvh
    
    # Calculate each component
    components = {
        'revenue': weights['alpha'] * rev,
        'time_value': weights['beta'] * time_value,
        'time_dividends': weights['gamma'] * td,
        'consciousness_delta': weights['delta'] * delta_c,
        'trust': weights['epsilon'] * trust,
        'compliance': weights['zeta'] * compliance,
        'quality': weights['eta'] * quality,
    }
    
    # Total C-ROI*
    c_roi_total = sum(components.values())
    
    return {
        'c_roi': c_roi_total,
        'components': components,
        'weights': weights,
        'time_value': time_value,
        'shadow_price_of_time': v_t,
    }


# =============================================================================
# Utility Functions
# =============================================================================

def format_time_violence_report(
    ops_score: float,
    info_score: float,
    tv_human: float,
    hours_saved: float = 0.0
) -> str:
    """
    Format a human-readable Time Violence report.
    
    Args:
        ops_score: Operational Time Violence score
        info_score: Informational Time Violence score
        tv_human: Human Time Violence
        hours_saved: Hours of TV reduced (ΔTVH)
    
    Returns:
        Formatted string report
    """
    total = tv_total(ops_score, info_score)
    c_index = conscious_index(tv_human, total)
    
    report = f"""Time Violence Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Operational TV:     {ops_score:>10.2f} hours
Informational TV:   {info_score:>10.2f} hours
─────────────────────────────────────────
Total TV:           {total:>10.2f} hours
Human TV:           {tv_human:>10.2f} hours
Consciousness C(S): {c_index:>10.2%}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if hours_saved > 0:
        reduction_pct = (hours_saved / tv_human * 100) if tv_human > 0 else 0
        report += f"Time Saved (ΔTVH):  {hours_saved:>10.2f} hours ({reduction_pct:.1f}% reduction)\n"
    
    return report


def format_c_roi_report(roi_result: Dict) -> str:
    """
    Format a human-readable Conscious ROI report.
    
    Args:
        roi_result: Result dict from roi_conscious()
    
    Returns:
        Formatted string report
    """
    components = roi_result['components']
    weights = roi_result['weights']
    
    report = f"""Conscious ROI (C-ROI*) Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Component                Weight    Value
─────────────────────────────────────────
Revenue                  {weights['alpha']:>5.2f}   {components['revenue']:>10.2f}
Time Value (vₜ·ΔTVH)     {weights['beta']:>5.2f}   {components['time_value']:>10.2f}
Time Dividends           {weights['gamma']:>5.2f}   {components['time_dividends']:>10.2f}
Consciousness ΔC(S)      {weights['delta']:>5.2f}   {components['consciousness_delta']:>10.2f}
Trust (T)                {weights['epsilon']:>5.2f}   {components['trust']:>10.2f}
Compliance (X)           {weights['zeta']:>5.2f}   {components['compliance']:>10.2f}
Quality (Q)              {weights['eta']:>5.2f}   {components['quality']:>10.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total C-ROI*:                      {roi_result['c_roi']:>10.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Shadow Price of Time: ${roi_result['shadow_price_of_time']:.2f}/hour
"""
    return report


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    # Example: Calculate Time Violence for a customer support system
    print("Example 1: Customer Support System Time Violence")
    print("=" * 60)
    
    # Operational TV: 10 tickets/hr arrive, 12/hr capacity, variance in both
    ops = tv_ops(arr_rate=10, svc_rate=12, var_arr=4, var_svc=2, tau=8)
    
    # Informational TV: Knowledge gaps, decision complexity, redundant comms
    info = tv_info(dkl=2.5, decision_entropy=3.2, redundancy_mi=1.1)
    
    # Total TV and human component
    total = tv_total(ops, info)
    human_tv = 20.0  # humans handle 20 hours of the total TV
    
    print(format_time_violence_report(ops, info, human_tv, hours_saved=0))
    
    # Example: Calculate C-ROI for automation project
    print("\nExample 2: Support Automation Project C-ROI")
    print("=" * 60)
    
    # Project reduces human TV by 15 hours/week, costs $5K, saves $10K in labor
    hours_saved = 15.0
    td = time_dividends(hours_saved)
    print(f"\nTime Dividend Distribution:")
    print(f"  Users:      {td['users']:.1f} hours")
    print(f"  Navigators: {td['navigators']:.1f} hours")
    print(f"  Company:    {td['company']:.1f} hours")
    print(f"  Total:      {td['total']:.1f} hours")
    
    # Calculate C-ROI
    roi = roi_conscious(
        rev=10000,           # $10K revenue impact
        dtvh=hours_saved,    # 15 hours/week saved
        v_t=35,              # $35/hour shadow price
        delta_c=0.15,        # 15% improvement in consciousness
        trust=0.8,           # 80% trust (some evidence)
        compliance=1.0,      # Full compliance with constraints
        quality=0.9          # 90% quality score
    )
    
    print(format_c_roi_report(roi))
    
    print("\nInterpretation:")
    print(f"  Traditional ROI would only show: ${roi['components']['revenue']:,.0f}")
    print(f"  Conscious ROI includes time value: ${roi['c_roi']:,.0f}")
    print(f"  Time value alone: ${roi['time_value']:,.0f}")
    print(f"  Multiplier: {roi['c_roi'] / roi['components']['revenue']:.2f}x")

