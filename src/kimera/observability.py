"""
Observability and telemetry for Kimera Identity system
Prometheus metrics and entropy tracking
"""

import time
import functools
from typing import Dict, Any, Optional, Callable
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
import logging

# Create a custom registry for Kimera metrics
kimera_registry = CollectorRegistry()

# Define Prometheus metrics
identity_operations_total = Counter(
    'kimera_identity_operations_total',
    'Total number of identity operations',
    ['operation_type', 'identity_type'],
    registry=kimera_registry
)

identity_entropy_histogram = Histogram(
    'kimera_identity_entropy',
    'Distribution of identity entropy values',
    ['identity_type'],
    registry=kimera_registry
)

identity_tau_histogram = Histogram(
    'kimera_identity_effective_tau',
    'Distribution of effective tau values',
    ['identity_type'],
    registry=kimera_registry
)

lattice_operations_total = Counter(
    'kimera_lattice_operations_total',
    'Total number of lattice operations',
    ['operation_type'],
    registry=kimera_registry
)

lattice_intensity_histogram = Histogram(
    'kimera_lattice_intensity',
    'Distribution of lattice intensity values',
    registry=kimera_registry
)

storage_operations_timer = Histogram(
    'kimera_storage_operations_duration_seconds',
    'Time spent on storage operations',
    ['operation_type'],
    registry=kimera_registry
)

active_identities_gauge = Gauge(
    'kimera_active_identities',
    'Number of active identities in storage',
    ['identity_type'],
    registry=kimera_registry
)

# Setup logging
logger = logging.getLogger(__name__)


def track_entropy(func: Callable) -> Callable:
    """
    Decorator to track entropy metrics for identity operations
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            # Extract identity from result or args
            identity = None
            if hasattr(result, 'entropy'):
                identity = result
            elif args and hasattr(args[0], 'entropy'):
                identity = args[0]
            
            if identity:
                # Track entropy metrics
                entropy_value = identity.entropy()
                effective_tau = identity.effective_tau()
                identity_type = identity.type
                
                identity_entropy_histogram.labels(identity_type=identity_type).observe(entropy_value)
                identity_tau_histogram.labels(identity_type=identity_type).observe(effective_tau)
                identity_operations_total.labels(
                    operation_type=func.__name__,
                    identity_type=identity_type
                ).inc()
                
                logger.debug(f"Identity {identity.id}: entropy={entropy_value:.3f}, tau={effective_tau:.3f}")
            
            # Track operation timing
            duration = time.time() - start_time
            storage_operations_timer.labels(operation_type=func.__name__).observe(duration)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    
    return wrapper


def track_lattice_operation(func: Callable) -> Callable:
    """
    Decorator to track lattice operation metrics
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            # Track lattice metrics
            lattice_operations_total.labels(operation_type=func.__name__).inc()
            
            # If result is a numeric intensity, track it
            if isinstance(result, (int, float)):
                lattice_intensity_histogram.observe(result)
                logger.debug(f"Lattice operation {func.__name__}: intensity={result:.3f}")
            
            # Track operation timing
            duration = time.time() - start_time
            storage_operations_timer.labels(operation_type=func.__name__).observe(duration)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in lattice operation {func.__name__}: {e}")
            raise
    
    return wrapper


def update_identity_gauges(storage) -> None:
    """
    Update gauge metrics for active identities
    """
    try:
        # Get identity counts by type
        geoid_count = len([i for i in storage.list_identities() if i.get('type') == 'geoid'])
        scar_count = len([i for i in storage.list_identities() if i.get('type') == 'scar'])
        
        active_identities_gauge.labels(identity_type='geoid').set(geoid_count)
        active_identities_gauge.labels(identity_type='scar').set(scar_count)
        
        logger.debug(f"Updated identity gauges: geoid={geoid_count}, scar={scar_count}")
        
    except Exception as e:
        logger.error(f"Error updating identity gauges: {e}")


def get_metrics_summary() -> Dict[str, Any]:
    """
    Get a summary of current metrics
    """
    try:
        # Generate Prometheus metrics
        metrics_output = generate_latest(kimera_registry).decode('utf-8')
        
        # Parse some key metrics for summary
        lines = metrics_output.split('\n')
        summary = {
            "timestamp": time.time(),
            "metrics_available": True,
            "prometheus_output": metrics_output
        }
        
        # Extract some key values
        for line in lines:
            if line.startswith('kimera_identity_operations_total'):
                summary["identity_operations"] = line
            elif line.startswith('kimera_lattice_operations_total'):
                summary["lattice_operations"] = line
        
        return summary
        
    except Exception as e:
        logger.error(f"Error generating metrics summary: {e}")
        return {
            "timestamp": time.time(),
            "metrics_available": False,
            "error": str(e)
        }


def log_entropy_event(identity_id: str, entropy: float, effective_tau: float, event_type: str = "calculation") -> None:
    """
    Log entropy-related events for debugging and analysis
    """
    logger.info(f"Entropy event: {event_type} | ID: {identity_id} | entropy: {entropy:.3f} | tau: {effective_tau:.3f}")


def export_metrics_to_file(filepath: str = "kimera_metrics.txt") -> bool:
    """
    Export current metrics to a file
    """
    try:
        metrics_output = generate_latest(kimera_registry).decode('utf-8')
        
        with open(filepath, 'w') as f:
            f.write(f"# Kimera Metrics Export - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(metrics_output)
        
        logger.info(f"Metrics exported to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting metrics to {filepath}: {e}")
        return False


# Convenience function to get metrics endpoint data
def get_prometheus_metrics() -> str:
    """
    Get Prometheus-formatted metrics for HTTP endpoint
    """
    return generate_latest(kimera_registry).decode('utf-8')