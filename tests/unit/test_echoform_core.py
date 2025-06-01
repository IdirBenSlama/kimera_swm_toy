#!/usr/bin/env python3
"""
EchoForm core unit tests
"""
import sys
sys.path.insert(0, 'src')

import json
import time
from kimera.echoform import EchoForm

def test_echoform_creation():
    """Test basic EchoForm creation"""
    echo = EchoForm()
    assert echo is not None
    
def test_echoform_basic_operations():
    """Test basic EchoForm operations"""
    echo = EchoForm()
    
    # Test basic functionality
    result = echo.process("test input")
    assert result is not None
    
def test_echoform_configuration():
    """Test EchoForm configuration"""
    config = {
        "mode": "test",
        "debug": True
    }
    echo = EchoForm(config=config)
    assert echo.config["mode"] == "test"
    assert echo.config["debug"] is True

if __name__ == "__main__":
    test_echoform_creation()
    test_echoform_basic_operations()
    test_echoform_configuration()
    print("[PASS] All EchoForm core tests passed!")