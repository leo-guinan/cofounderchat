"""
Tests for Conscious Economics calculation tools.

These tests verify that Time Violence metrics, Consciousness Index,
Time Dividends, and Conscious ROI calculations are correct and robust.
"""

import pytest
import math
from cofounderchat.conscious_tools import (
    tv_ops,
    tv_info,
    tv_total,
    conscious_index,
    time_dividends,
    roi_conscious,
    format_time_violence_report,
    format_c_roi_report,
)


class TestTimeViolenceOps:
    """Test Operational Time Violence calculations."""
    
    def test_basic_calculation(self):
        """Test basic ops TV calculation."""
        result = tv_ops(arr_rate=10, svc_rate=12, var_arr=4, var_svc=2, tau=8)
        # (10/12) * sqrt(4+2) * 8 = 0.833 * 2.449 * 8 ≈ 16.33
        assert result > 16 and result < 17
    
    def test_zero_variance(self):
        """Test with zero variance (deterministic system)."""
        result = tv_ops(arr_rate=5, svc_rate=10, var_arr=0, var_svc=0, tau=10)
        assert result == 0.0
    
    def test_high_utilization(self):
        """Test high utilization increases TV."""
        low_util = tv_ops(arr_rate=5, svc_rate=20, var_arr=1, var_svc=1, tau=10)
        high_util = tv_ops(arr_rate=15, svc_rate=20, var_arr=1, var_svc=1, tau=10)
        assert high_util > low_util
    
    def test_invalid_service_rate(self):
        """Test that zero/negative service rate raises error."""
        with pytest.raises(ValueError):
            tv_ops(arr_rate=10, svc_rate=0, var_arr=1, var_svc=1, tau=8)
        with pytest.raises(ValueError):
            tv_ops(arr_rate=10, svc_rate=-5, var_arr=1, var_svc=1, tau=8)
    
    def test_negative_inputs(self):
        """Test that negative inputs raise errors."""
        with pytest.raises(ValueError):
            tv_ops(arr_rate=-1, svc_rate=10, var_arr=1, var_svc=1, tau=8)
        with pytest.raises(ValueError):
            tv_ops(arr_rate=10, svc_rate=10, var_arr=-1, var_svc=1, tau=8)


class TestTimeViolenceInfo:
    """Test Informational Time Violence calculations."""
    
    def test_basic_calculation(self):
        """Test basic info TV calculation."""
        result = tv_info(dkl=2.5, decision_entropy=3.2, redundancy_mi=1.1)
        assert result == pytest.approx(6.8)
    
    def test_zero_info_tv(self):
        """Test zero informational TV (perfect information)."""
        result = tv_info(dkl=0, decision_entropy=0, redundancy_mi=0)
        assert result == 0.0
    
    def test_negative_inputs(self):
        """Test that negative inputs raise errors."""
        with pytest.raises(ValueError):
            tv_info(dkl=-1, decision_entropy=1, redundancy_mi=1)


class TestTimeViolenceTotal:
    """Test Total Time Violence calculations."""
    
    def test_basic_calculation(self):
        """Test total = ops + info."""
        ops = 10.0
        info = 5.0
        total = tv_total(ops, info)
        assert total == 15.0
    
    def test_zero_total(self):
        """Test zero TV (ideal system)."""
        total = tv_total(0, 0)
        assert total == 0.0


class TestConsciousnessIndex:
    """Test Consciousness Index calculations."""
    
    def test_perfect_automation(self):
        """Test C(S) = 1 when no human TV."""
        c_index = conscious_index(tv_human=0, tv_total=100)
        assert c_index == 1.0
    
    def test_zero_automation(self):
        """Test C(S) = 0 when all TV is human."""
        c_index = conscious_index(tv_human=100, tv_total=100)
        assert c_index == 0.0
    
    def test_partial_automation(self):
        """Test C(S) = 0.8 when 20% of TV is human."""
        c_index = conscious_index(tv_human=20, tv_total=100)
        assert c_index == pytest.approx(0.8)
    
    def test_zero_total_tv(self):
        """Test edge case: zero total TV."""
        c_index = conscious_index(tv_human=0, tv_total=0)
        assert c_index == 1.0
    
    def test_human_exceeds_total(self):
        """Test edge case: human TV > total TV (measurement error)."""
        c_index = conscious_index(tv_human=150, tv_total=100)
        assert c_index == 0.0
    
    def test_negative_inputs(self):
        """Test that negative inputs raise errors."""
        with pytest.raises(ValueError):
            conscious_index(tv_human=-1, tv_total=100)


class TestTimeDividends:
    """Test Time Dividend calculations."""
    
    def test_default_distribution(self):
        """Test default 60/20/20 distribution."""
        td = time_dividends(hours_saved=100)
        assert td['users'] == pytest.approx(60.0)
        assert td['navigators'] == pytest.approx(20.0)
        assert td['company'] == pytest.approx(20.0)
        assert td['total'] == pytest.approx(100.0)
    
    def test_custom_distribution(self):
        """Test custom distribution."""
        custom = {'users': 0.7, 'navigators': 0.2, 'company': 0.1}
        td = time_dividends(hours_saved=100, distribution=custom)
        assert td['users'] == pytest.approx(70.0)
        assert td['navigators'] == pytest.approx(20.0)
        assert td['company'] == pytest.approx(10.0)
    
    def test_zero_hours(self):
        """Test zero hours saved."""
        td = time_dividends(hours_saved=0)
        assert td['total'] == 0.0
    
    def test_invalid_distribution_sum(self):
        """Test distribution that doesn't sum to 1.0."""
        invalid = {'users': 0.5, 'navigators': 0.3, 'company': 0.1}
        with pytest.raises(ValueError):
            time_dividends(hours_saved=100, distribution=invalid)
    
    def test_missing_distribution_keys(self):
        """Test distribution missing required keys."""
        invalid = {'users': 0.8, 'navigators': 0.2}
        with pytest.raises(ValueError):
            time_dividends(hours_saved=100, distribution=invalid)
    
    def test_negative_hours(self):
        """Test negative hours raises error."""
        with pytest.raises(ValueError):
            time_dividends(hours_saved=-10)


class TestConsciousROI:
    """Test Conscious ROI calculations."""
    
    def test_basic_calculation(self):
        """Test basic C-ROI calculation."""
        result = roi_conscious(
            rev=1000,
            dtvh=10,
            v_t=50,
            delta_c=0.1,
            trust=0.8,
            compliance=1.0,
            quality=0.9
        )
        # With default weights (all 1.0):
        # 1000 + 500 + 10 + 0.1 + 0.8 + 1.0 + 0.9 = 1512.8
        assert result['c_roi'] == pytest.approx(1512.8)
        assert result['time_value'] == pytest.approx(500)
    
    def test_revenue_only(self):
        """Test C-ROI with only revenue."""
        result = roi_conscious(rev=1000, dtvh=0)
        # Should be 1000 (rev) + 0 (time) + other small components
        assert result['components']['revenue'] == 1000
        assert result['components']['time_value'] == 0
    
    def test_custom_weights(self):
        """Test C-ROI with custom weights."""
        weights = {
            'alpha': 2.0,   # 2x weight on revenue
            'beta': 1.0,
            'gamma': 0.5,
            'delta': 0.5,
            'epsilon': 0.0,  # Ignore trust
            'zeta': 0.0,     # Ignore compliance
            'eta': 0.0,      # Ignore quality
        }
        result = roi_conscious(
            rev=1000,
            dtvh=10,
            v_t=50,
            weights=weights
        )
        # 2*1000 + 1*500 + 0.5*10 + ... = 2505
        assert result['components']['revenue'] == 2000
        assert result['components']['trust'] == 0
    
    def test_default_td(self):
        """Test that TD defaults to dtvh if not specified."""
        result = roi_conscious(rev=0, dtvh=100)
        assert result['components']['time_dividends'] == 100
    
    def test_custom_shadow_price(self):
        """Test custom shadow price of time."""
        result = roi_conscious(rev=0, dtvh=10, v_t=100)
        assert result['time_value'] == 1000
        assert result['shadow_price_of_time'] == 100
    
    def test_invalid_weights(self):
        """Test invalid weight keys raise error."""
        invalid_weights = {'alpha': 1.0, 'beta': 1.0}  # Missing keys
        with pytest.raises(ValueError):
            roi_conscious(rev=1000, dtvh=10, weights=invalid_weights)


class TestFormattingFunctions:
    """Test report formatting functions."""
    
    def test_time_violence_report_format(self):
        """Test TV report formatting."""
        report = format_time_violence_report(
            ops_score=10.0,
            info_score=5.0,
            tv_human=12.0,
            hours_saved=3.0
        )
        assert "Operational TV:" in report
        assert "10.00" in report
        assert "Informational TV:" in report
        assert "5.00" in report
        assert "Total TV:" in report
        assert "15.00" in report
        assert "Consciousness C(S):" in report
        assert "Time Saved" in report
    
    def test_c_roi_report_format(self):
        """Test C-ROI report formatting."""
        roi = roi_conscious(rev=1000, dtvh=10, v_t=50)
        report = format_c_roi_report(roi)
        assert "Conscious ROI" in report
        assert "Revenue" in report
        assert "Time Value" in report
        assert "Total C-ROI*:" in report
        assert "$50.00/hour" in report


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_very_large_values(self):
        """Test with very large numbers."""
        result = roi_conscious(rev=1e9, dtvh=1e6, v_t=100)
        assert result['c_roi'] > 1e9
    
    def test_very_small_values(self):
        """Test with very small numbers."""
        result = roi_conscious(rev=0.01, dtvh=0.01, v_t=0.01)
        assert result['c_roi'] > 0
    
    def test_floating_point_precision(self):
        """Test floating point edge cases."""
        # Distribution that sums to 1.0 within floating point tolerance
        dist = {'users': 0.333333, 'navigators': 0.333333, 'company': 0.333334}
        td = time_dividends(hours_saved=100, distribution=dist)
        assert abs(td['total'] - 100.0) < 1e-6


class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_full_workflow(self):
        """Test complete Conscious Economics calculation workflow."""
        # 1. Calculate Time Violence
        ops = tv_ops(arr_rate=10, svc_rate=12, var_arr=4, var_svc=2, tau=8)
        info = tv_info(dkl=2.5, decision_entropy=3.2, redundancy_mi=1.1)
        total = tv_total(ops, info)
        
        # 2. Calculate Consciousness Index
        tv_human_before = 20.0
        c_before = conscious_index(tv_human_before, total)
        
        # 3. After automation, reduce human TV
        hours_saved = 10.0
        tv_human_after = tv_human_before - hours_saved
        c_after = conscious_index(tv_human_after, total)
        delta_c = c_after - c_before
        
        # 4. Calculate Time Dividends
        td = time_dividends(hours_saved)
        
        # 5. Calculate Conscious ROI
        roi = roi_conscious(
            rev=5000,
            dtvh=hours_saved,
            v_t=35,
            td=td['total'],
            delta_c=delta_c,
            trust=0.8,
            compliance=1.0,
            quality=0.9
        )
        
        # Verify the chain
        assert ops > 0
        assert info > 0
        assert total > 0
        assert c_after > c_before
        assert delta_c > 0
        assert td['total'] == hours_saved
        assert roi['c_roi'] > roi['components']['revenue']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

