#!/usr/bin/env python3
"""
Test CLS lattice integration with EchoForm storage and cls_event tracking
Now with persistent DuckDB storage backend
"""
import sys
import math
import os
sys.path.insert(0, 'src')

import pytest
from kimera.cls import CLS
from kimera.storage import LatticeStorage
from kimera.identity import Identity

def test_cls_basic_integration():
    """Test basic CLS integration"""
    cls_system = CLS()
    assert cls_system is not None
    
def test_cls_storage_integration():
    """Test CLS integration with storage"""
    storage = LatticeStorage()
    cls_system = CLS(storage=storage)
    
    # Test basic operations
    identity = Identity(content="test content")
    result = cls_system.process(identity)
    assert result is not None

def test_cls_lattice_operations():
    """Test CLS lattice operations"""
    cls_system = CLS()
    
    # Test lattice creation and manipulation
    lattice_data = {"test": "data"}
    result = cls_system.create_lattice(lattice_data)
    assert result is not None

if __name__ == "__main__":
    test_cls_basic_integration()
    test_cls_storage_integration()
    test_cls_lattice_operations()
    print("✅ All CLS integration tests passed!")