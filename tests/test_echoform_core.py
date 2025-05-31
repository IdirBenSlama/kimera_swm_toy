#!/usr/bin/env python3
"""
EchoForm core unit tests
"""
import sys
sys.path.insert(0, 'src')

import json
import time
from kimera.echoform import EchoForm


def test_echoform_initialization():
    """Test EchoForm initialization with various parameters"""
    # Minimal initialization
    echo = EchoForm(anchor="test")
    assert echo.anchor == "test"
    assert echo.domain == "echo"
    assert echo.phase == "active"
    assert echo.recursive is True
    assert echo.terms == []
    assert echo.topology == {}
    assert echo.trace_signature != ""
    assert echo.echo_created_at is not None
    
    # Full initialization
    custom_time = time.time()
    echo2 = EchoForm(
        anchor="custom",
        domain="scar",
        terms=[{"test": "term"}],
        phase="dormant",
        recursive=False,
        topology={"key": "value"},
        trace_signature="custom_trace",
        echo_created_at=custom_time
    )
    assert echo2.anchor == "custom"
    assert echo2.domain == "scar"
    assert echo2.phase == "dormant"
    assert echo2.recursive is False
    assert echo2.terms == [{"test": "term"}]
    assert echo2.topology == {"key": "value"}
    assert echo2.trace_signature == "custom_trace"
    assert echo2.echo_created_at == custom_time


def test_compute_trace():
    """Test trace signature computation"""
    echo = EchoForm(anchor="test", phase="active")
    
    # Basic trace
    trace1 = echo.compute_trace()
    assert len(trace1) == 16
    assert trace1.isalnum()
    
    # Trace with previous signature
    trace2 = echo.compute_trace("prev_sig")
    assert len(trace2) == 16
    assert trace1 != trace2  # Should be different with prev_sig
    
    # Same inputs should give same output
    trace3 = echo.compute_trace("prev_sig")
    assert trace2 == trace3


def test_intensity_sum():
    """Test intensity calculation with and without time decay"""
    # Empty terms
    echo = EchoForm(anchor="test")
    assert echo.intensity_sum() == 0.0
    assert echo.intensity_sum(apply_time_decay=False) == 0.0
    
    # Terms with intensity (no time decay)
    echo.terms = [
        {"intensity": 1.0},
        {"intensity": 2.5},
        {"intensity": 0.5}
    ]
    assert echo.intensity_sum(apply_time_decay=False) == 4.0
    
    # Terms without intensity (should default to 0)
    echo.terms = [
        {"symbol": "test"},
        {"intensity": 1.0},
        {"other": "field"}
    ]
    assert echo.intensity_sum(apply_time_decay=False) == 1.0


def test_intensity_sum_time_decay():
    """Test time-decay weighting in intensity calculation"""
    import time
    from kimera.echoform import TIME_DECAY_TAU
    
    current_time = time.time()
    
    # Create echo with terms having different timestamps
    echo = EchoForm(anchor="decay_test")
    echo.terms = [
        {
            "intensity": 1.0,
            "timestamp": current_time  # Recent - should have full weight
        },
        {
            "intensity": 1.0,
            "timestamp": current_time - TIME_DECAY_TAU  # One τ ago - should be ~0.37
        },
        {
            "intensity": 1.0,
            "timestamp": current_time - 2 * TIME_DECAY_TAU  # Two τ ago - should be ~0.14
        },
        {
            "intensity": 1.0
            # No timestamp - should use form creation time
        }
    ]
    
    # Test without decay
    intensity_no_decay = echo.intensity_sum(apply_time_decay=False)
    assert intensity_no_decay == 4.0
    
    # Test with decay
    intensity_with_decay = echo.intensity_sum(apply_time_decay=True)
    
    # Should be less than without decay due to time decay
    assert intensity_with_decay < intensity_no_decay
    
    # Should be greater than 1.0 (at least the recent term)
    assert intensity_with_decay > 1.0
    
    # Should be less than 3.0 (since older terms decay)
    assert intensity_with_decay < 3.0
    
    print(f"  Intensity without decay: {intensity_no_decay:.3f}")
    print(f"  Intensity with decay: {intensity_with_decay:.3f}")
    print(f"  Decay factor: {intensity_with_decay/intensity_no_decay:.3f}")


def test_time_decay_constants():
    """Test that time decay constants are reasonable"""
    from kimera.echoform import TIME_DECAY_TAU
    import math
    
    # τ should be 14 days in seconds
    expected_tau = 14 * 24 * 3600
    assert TIME_DECAY_TAU == expected_tau
    
    # Test decay factors at key intervals
    # After 1 day: exp(-1/14) ≈ 0.93
    one_day = 24 * 3600
    decay_1day = math.exp(-one_day / TIME_DECAY_TAU)
    assert 0.9 < decay_1day < 0.95
    
    # After 14 days (1 τ): exp(-1) ≈ 0.37
    decay_14days = math.exp(-TIME_DECAY_TAU / TIME_DECAY_TAU)
    assert 0.35 < decay_14days < 0.4
    
    # After 28 days (2 τ): exp(-2) ≈ 0.14
    decay_28days = math.exp(-2 * TIME_DECAY_TAU / TIME_DECAY_TAU)
    assert 0.12 < decay_28days < 0.16
    
    print(f"  τ = {TIME_DECAY_TAU} seconds ({TIME_DECAY_TAU/(24*3600):.1f} days)")
    print(f"  1-day decay factor: {decay_1day:.3f}")
    print(f"  14-day decay factor: {decay_14days:.3f}")
    print(f"  28-day decay factor: {decay_28days:.3f}")


def test_add_term():
    """Test adding terms"""
    echo = EchoForm(anchor="test")
    
    # Basic term
    echo.add_term("symbol1", "role1")
    assert len(echo.terms) == 1
    assert echo.terms[0]["symbol"] == "symbol1"
    assert echo.terms[0]["role"] == "role1"
    assert echo.terms[0]["intensity"] == 1.0
    
    # Term with custom intensity and extra fields
    echo.add_term("symbol2", "role2", 2.5, extra="field", another=42)
    assert len(echo.terms) == 2
    assert echo.terms[1]["symbol"] == "symbol2"
    assert echo.terms[1]["role"] == "role2"
    assert echo.terms[1]["intensity"] == 2.5
    assert echo.terms[1]["extra"] == "field"
    assert echo.terms[1]["another"] == 42


def test_mutate_phase():
    """Test phase mutation"""
    echo1 = EchoForm(
        anchor="test",
        domain="scar",
        terms=[{"symbol": "test", "intensity": 1.0}],
        topology={"key": "value"}
    )
    original_trace = echo1.trace_signature
    original_time = echo1.echo_created_at
    
    # Mutate phase
    echo2 = echo1.mutate_phase("new_phase")
    
    # Original should be unchanged
    assert echo1.phase == "active"
    assert echo1.trace_signature == original_trace
    assert echo1.echo_created_at == original_time
    
    # New form should have changes
    assert echo2.phase == "new_phase"
    assert echo2.anchor == echo1.anchor
    assert echo2.domain == echo1.domain
    assert echo2.terms == echo1.terms  # Should be copied
    assert echo2.topology == echo1.topology  # Should be copied
    assert echo2.trace_signature != original_trace  # Should be different
    assert echo2.echo_created_at >= original_time  # Should be same or newer (timing can be identical)


def test_flatten():
    """Test JSON serialization"""
    echo = EchoForm(
        anchor="test",
        domain="scar",
        terms=[{"symbol": "test", "intensity": 1.0}],
        phase="active"
    )
    
    blob = echo.flatten()
    
    # Should be valid JSON
    data = json.loads(blob)
    assert isinstance(data, dict)
    
    # Should contain all fields
    assert data["anchor"] == "test"
    assert data["domain"] == "scar"
    assert data["phase"] == "active"
    assert data["terms"] == [{"symbol": "test", "intensity": 1.0}]
    assert "trace_signature" in data
    assert "echo_created_at" in data


def test_reinflate():
    """Test JSON deserialization"""
    # Create test data
    test_data = {
        "anchor": "test",
        "domain": "scar",
        "terms": [{"symbol": "test", "intensity": 1.0}],
        "phase": "dormant",
        "recursive": False,
        "topology": {"key": "value"},
        "trace_signature": "test_trace_123456",
        "echo_created_at": 1234567890.0
    }
    blob = json.dumps(test_data)
    
    # Reinflate
    echo = EchoForm.reinflate(blob)
    
    # Verify all fields
    assert echo.anchor == "test"
    assert echo.domain == "scar"
    assert echo.terms == [{"symbol": "test", "intensity": 1.0}]
    assert echo.phase == "dormant"
    assert echo.recursive is False
    assert echo.topology == {"key": "value"}
    assert echo.trace_signature == "test_trace_123456"
    assert echo.echo_created_at == 1234567890.0


def test_to_dict():
    """Test dictionary conversion"""
    echo = EchoForm(
        anchor="test",
        domain="scar",
        terms=[{"symbol": "test"}],
        phase="active"
    )
    
    data = echo.to_dict()
    
    assert isinstance(data, dict)
    assert data["anchor"] == "test"
    assert data["domain"] == "scar"
    assert data["terms"] == [{"symbol": "test"}]
    assert data["phase"] == "active"
    assert "trace_signature" in data
    assert "echo_created_at" in data


def test_repr():
    """Test string representation"""
    echo = EchoForm(anchor="test", domain="scar")
    echo.add_term("symbol1", "role1")
    echo.add_term("symbol2", "role2")
    
    repr_str = repr(echo)
    assert "EchoForm" in repr_str
    assert "anchor='test'" in repr_str
    assert "domain='scar'" in repr_str
    assert "phase='active'" in repr_str
    assert "terms=2" in repr_str


def test_roundtrip_consistency():
    """Test that flatten → reinflate preserves all data"""
    echo1 = EchoForm(
        anchor="roundtrip_test",
        domain="law",
        terms=[
            {"symbol": "α", "role": "primary", "intensity": 1.5},
            {"symbol": "β", "role": "secondary", "intensity": 0.8, "meta": "data"}
        ],
        phase="evolving",
        recursive=False,
        topology={"nodes": [1, 2, 3], "edges": {"a": "b"}}
    )
    
    # Roundtrip
    blob = echo1.flatten()
    echo2 = EchoForm.reinflate(blob)
    
    # Verify complete equality
    assert echo1.anchor == echo2.anchor
    assert echo1.domain == echo2.domain
    assert echo1.terms == echo2.terms
    assert echo1.phase == echo2.phase
    assert echo1.recursive == echo2.recursive
    assert echo1.topology == echo2.topology
    assert echo1.trace_signature == echo2.trace_signature
    assert echo1.echo_created_at == echo2.echo_created_at
    assert echo1.intensity_sum() == echo2.intensity_sum()


def main():
    """Run all unit tests"""
    print("🧪 EchoForm Unit Tests with Time-Decay")
    print("=" * 40)
    
    tests = [
        test_echoform_initialization,
        test_compute_trace,
        test_intensity_sum,
        test_intensity_sum_time_decay,
        test_time_decay_constants,
        test_add_term,
        test_mutate_phase,
        test_flatten,
        test_reinflate,
        test_to_dict,
        test_repr,
        test_roundtrip_consistency
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Results: {passed}/{len(tests)} tests passed")
    return passed == len(tests)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)