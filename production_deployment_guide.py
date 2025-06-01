#!/usr/bin/env python3
"""
Production Deployment Guide for Kimera
Comprehensive deployment and monitoring setup
"""

import sys
import os
import json
import time
from typing import Dict, List, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class ProductionDeployment:
    """Production deployment utilities and monitoring"""
    
    def __init__(self):
        self.deployment_config = {}
        self.monitoring_data = []
    
    def generate_deployment_config(self):
        """Generate production deployment configuration"""
        print("🚀 Generating Production Deployment Configuration")
        print("=" * 60)
        
        config = {
            "kimera": {
                "version": "1.0.0",
                "environment": "production",
                "storage": {
                    "type": "sqlite",
                    "path": "/data/kimera/lattice.db",
                    "backup_interval": "1h",
                    "retention_days": 30
                },
                "reactor": {
                    "batch_size": 200,
                    "max_cycles": 10,
                    "parallel_workers": 4,
                    "memory_limit_mb": 2048
                },
                "api": {
                    "host": "0.0.0.0",
                    "port": 8080,
                    "workers": 4,
                    "timeout": 30,
                    "rate_limit": "1000/hour"
                },
                "monitoring": {
                    "metrics_enabled": True,
                    "log_level": "INFO",
                    "health_check_interval": 30,
                    "alert_thresholds": {
                        "memory_usage": 80,
                        "response_time": 5.0,
                        "error_rate": 0.05
                    }
                },
                "security": {
                    "api_key_required": True,
                    "rate_limiting": True,
                    "input_validation": True,
                    "max_input_length": 10000
                }
            }
        }
        
        self.deployment_config = config
        
        # Save configuration
        with open("kimera_production_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuration generated: kimera_production_config.json")
        return config
    
    def create_docker_setup(self):
        """Create Docker deployment files"""
        print("\n🐳 Creating Docker Deployment Setup")
        print("-" * 40)
        
        # Dockerfile
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \\
    poetry config virtualenvs.create false && \\
    poetry install --only=main

# Copy application code
COPY src/ ./src/
COPY kimera_production_config.json ./

# Create data directory
RUN mkdir -p /data/kimera

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run application
CMD ["python", "-m", "kimera", "serve", "--config", "kimera_production_config.json"]
'''
        
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        compose_content = '''version: '3.8'

services:
  kimera:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - kimera_data:/data/kimera
      - ./logs:/app/logs
    environment:
      - KIMERA_ENV=production
      - KIMERA_LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8080/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  kimera_data:
  prometheus_data:
  grafana_data:
'''
        
        with open("docker-compose.yml", "w") as f:
            f.write(compose_content)
        
        print("✅ Created Dockerfile and docker-compose.yml")
        return True
    
    def create_monitoring_setup(self):
        """Create monitoring and alerting configuration"""
        print("\n📊 Creating Monitoring Setup")
        print("-" * 40)
        
        # Create monitoring directory
        os.makedirs("monitoring", exist_ok=True)
        
        # Prometheus configuration
        prometheus_config = '''global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "kimera_alerts.yml"

scrape_configs:
  - job_name: 'kimera'
    static_configs:
      - targets: ['kimera:8080']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
'''
        
        with open("monitoring/prometheus.yml", "w") as f:
            f.write(prometheus_config)
        
        # Alert rules
        alert_rules = '''groups:
  - name: kimera_alerts
    rules:
      - alert: KimeraHighMemoryUsage
        expr: kimera_memory_usage_percent > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Kimera memory usage is high"
          description: "Memory usage is {{ $value }}%"

      - alert: KimeraHighResponseTime
        expr: kimera_response_time_seconds > 5
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Kimera response time is high"
          description: "Response time is {{ $value }} seconds"

      - alert: KimeraHighErrorRate
        expr: kimera_error_rate > 0.05
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Kimera error rate is high"
          description: "Error rate is {{ $value }}"

      - alert: KimeraServiceDown
        expr: up{job="kimera"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Kimera service is down"
          description: "Kimera service has been down for more than 1 minute"
'''
        
        with open("monitoring/kimera_alerts.yml", "w") as f:
            f.write(alert_rules)
        
        print("✅ Created monitoring configuration")
        return True
    
    def create_api_server(self):
        """Create production API server"""
        print("\n🌐 Creating Production API Server")
        print("-" * 40)
        
        api_server_content = '''#!/usr/bin/env python3
"""
Kimera Production API Server
FastAPI-based REST API for Kimera functionality
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import time
import logging
import asyncio
from contextlib import asynccontextmanager

# Kimera imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from kimera.geoid import init_geoid
from kimera.reactor import reactor_cycle, reactor_cycle_batched
from kimera.resonance import resonance
from kimera.storage import get_storage, close_storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Pydantic models
class GeoidRequest(BaseModel):
    text: str = Field(..., max_length=10000)
    language: str = Field(default="en", max_length=10)
    layers: List[str] = Field(default=["api"])

class ResonanceRequest(BaseModel):
    text1: str = Field(..., max_length=10000)
    text2: str = Field(..., max_length=10000)
    language: str = Field(default="en", max_length=10)

class ReactorRequest(BaseModel):
    texts: List[str] = Field(..., max_items=1000)
    cycles: int = Field(default=1, ge=1, le=10)
    language: str = Field(default="en", max_length=10)
    layers: List[str] = Field(default=["reactor"])

class GeoidResponse(BaseModel):
    gid: str
    echo: str
    language: str
    layers: List[str]
    scars: int
    created_at: str

class ResonanceResponse(BaseModel):
    score: float
    processing_time: float

class ReactorResponse(BaseModel):
    geoids_processed: int
    scars_created: int
    processing_time: float
    stats: Optional[Dict[str, Any]]

# Global storage
storage = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global storage
    storage = get_storage("production.db")
    logger.info("Kimera API server started")
    yield
    # Shutdown
    close_storage()
    logger.info("Kimera API server stopped")

# Create FastAPI app
app = FastAPI(
    title="Kimera API",
    description="Production API for Kimera semantic processing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement your authentication logic here
    # For demo purposes, accept any token
    if not credentials.credentials:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return credentials.credentials

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # Implement metrics collection here
    return {
        "kimera_requests_total": 0,
        "kimera_response_time_seconds": 0.0,
        "kimera_memory_usage_percent": 0.0,
        "kimera_error_rate": 0.0
    }

@app.post("/geoid", response_model=GeoidResponse)
async def create_geoid(
    request: GeoidRequest,
    token: str = Depends(verify_token)
):
    """Create a new geoid from text"""
    try:
        start_time = time.time()
        
        geoid = init_geoid(request.text, request.language, request.layers)
        
        processing_time = time.time() - start_time
        logger.info(f"Created geoid {geoid.gid} in {processing_time:.3f}s")
        
        return GeoidResponse(
            gid=geoid.gid,
            echo=geoid.echo,
            language=geoid.lang_axis,
            layers=geoid.context_layers,
            scars=len(geoid.scars),
            created_at=geoid.created_at.isoformat()
        )
    except Exception as e:
        logger.error(f"Error creating geoid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resonance", response_model=ResonanceResponse)
async def calculate_resonance(
    request: ResonanceRequest,
    token: str = Depends(verify_token)
):
    """Calculate resonance between two texts"""
    try:
        start_time = time.time()
        
        g1 = init_geoid(request.text1, request.language, ["resonance"])
        g2 = init_geoid(request.text2, request.language, ["resonance"])
        
        score = resonance(g1, g2)
        processing_time = time.time() - start_time
        
        logger.info(f"Calculated resonance {score:.3f} in {processing_time:.3f}s")
        
        return ResonanceResponse(
            score=score,
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"Error calculating resonance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reactor", response_model=ReactorResponse)
async def run_reactor(
    request: ReactorRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token)
):
    """Run reactor cycle on multiple texts"""
    try:
        start_time = time.time()
        
        # Create geoids
        geoids = [init_geoid(text, request.language, request.layers) 
                 for text in request.texts]
        
        initial_scars = sum(len(g.scars) for g in geoids)
        
        # Run reactor
        stats = reactor_cycle_batched(geoids, chunk=50, verbose=False)
        
        final_scars = sum(len(g.scars) for g in geoids)
        processing_time = time.time() - start_time
        
        logger.info(f"Processed {len(geoids)} geoids in {processing_time:.3f}s")
        
        return ReactorResponse(
            geoids_processed=len(geoids),
            scars_created=final_scars - initial_scars,
            processing_time=processing_time,
            stats=stats
        )
    except Exception as e:
        logger.error(f"Error running reactor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
'''
        
        with open("kimera_api_server.py", "w") as f:
            f.write(api_server_content)
        
        print("✅ Created production API server: kimera_api_server.py")
        return True
    
    def create_deployment_scripts(self):
        """Create deployment and management scripts"""
        print("\n📜 Creating Deployment Scripts")
        print("-" * 40)
        
        # Deployment script
        deploy_script = '''#!/bin/bash
# Kimera Production Deployment Script

set -e

echo "🚀 Deploying Kimera to Production"
echo "=================================="

# Check prerequisites
echo "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data/kimera
mkdir -p monitoring/grafana

# Set permissions
chmod 755 logs
chmod 755 data/kimera

# Build and start services
echo "Building and starting services..."
docker-compose down
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Health check
echo "Performing health check..."
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Kimera API is healthy"
else
    echo "❌ Kimera API health check failed"
    docker-compose logs kimera
    exit 1
fi

echo "✅ Deployment completed successfully!"
echo "API: http://localhost:8080"
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000 (admin/admin)"
'''
        
        with open("deploy.sh", "w") as f:
            f.write(deploy_script)
        os.chmod("deploy.sh", 0o755)
        
        # Backup script
        backup_script = '''#!/bin/bash
# Kimera Backup Script

BACKUP_DIR="/backups/kimera"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🔄 Creating Kimera backup: $DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec kimera sqlite3 /data/kimera/lattice.db ".backup /data/kimera/backup_$DATE.db"
docker cp $(docker-compose ps -q kimera):/data/kimera/backup_$DATE.db $BACKUP_DIR/

# Backup configuration
cp kimera_production_config.json $BACKUP_DIR/config_$DATE.json

# Compress backup
tar -czf $BACKUP_DIR/kimera_backup_$DATE.tar.gz -C $BACKUP_DIR backup_$DATE.db config_$DATE.json

# Clean up temporary files
rm $BACKUP_DIR/backup_$DATE.db $BACKUP_DIR/config_$DATE.json

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -name "kimera_backup_*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed: $BACKUP_DIR/kimera_backup_$DATE.tar.gz"
'''
        
        with open("backup.sh", "w") as f:
            f.write(backup_script)
        os.chmod("backup.sh", 0o755)
        
        print("✅ Created deployment scripts: deploy.sh, backup.sh")
        return True
    
    def run_production_setup(self):
        """Run complete production setup"""
        print("🚀 Kimera Production Deployment Setup")
        print("=" * 60)
        
        steps = [
            ("Configuration", self.generate_deployment_config),
            ("Docker Setup", self.create_docker_setup),
            ("Monitoring", self.create_monitoring_setup),
            ("API Server", self.create_api_server),
            ("Scripts", self.create_deployment_scripts)
        ]
        
        success_count = 0
        for step_name, step_func in steps:
            try:
                if step_func():
                    success_count += 1
                    print(f"✅ {step_name} completed")
                else:
                    print(f"❌ {step_name} failed")
            except Exception as e:
                print(f"❌ {step_name} failed: {e}")
        
        print("\n" + "=" * 60)
        print("📊 PRODUCTION SETUP SUMMARY")
        print("=" * 60)
        print(f"Completed Steps: {success_count}/{len(steps)}")
        
        if success_count == len(steps):
            print("\n🎉 PRODUCTION SETUP COMPLETE!")
            print("\nNext steps:")
            print("1. Review kimera_production_config.json")
            print("2. Run: ./deploy.sh")
            print("3. Access API at http://localhost:8080")
            print("4. Monitor at http://localhost:9090 (Prometheus)")
            print("5. Dashboard at http://localhost:3000 (Grafana)")
        else:
            print(f"\n⚠️ {len(steps) - success_count} steps failed - review needed")
        
        return success_count == len(steps)

def main():
    deployment = ProductionDeployment()
    return deployment.run_production_setup()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)