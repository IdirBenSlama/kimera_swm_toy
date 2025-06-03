"""
Translation Cache Implementation
================================

Provides persistent caching for translation results to improve performance
and reduce API calls.
"""

import os
import json
import time
import sqlite3
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class CacheBackend(ABC):
    """Abstract base class for cache backends."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Dict[str, Any], ttl: int):
        """Set value in cache with TTL."""
        pass
    
    @abstractmethod
    def delete(self, key: str):
        """Delete value from cache."""
        pass
    
    @abstractmethod
    def clear(self):
        """Clear all cache entries."""
        pass
    
    @abstractmethod
    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        pass


class MemoryCacheBackend(CacheBackend):
    """In-memory cache backend."""
    
    def __init__(self):
        self._cache = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from memory cache."""
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires"]:
                self._stats["hits"] += 1
                return entry["value"]
            else:
                # Expired - remove it
                del self._cache[key]
        
        self._stats["misses"] += 1
        return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int):
        """Set value in memory cache."""
        self._cache[key] = {
            "value": value,
            "expires": time.time() + ttl
        }
        self._stats["sets"] += 1
    
    def delete(self, key: str):
        """Delete value from memory cache."""
        if key in self._cache:
            del self._cache[key]
            self._stats["deletes"] += 1
    
    def clear(self):
        """Clear memory cache."""
        self._cache.clear()
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            **self._stats,
            "size": len(self._cache)
        }


class SQLiteCacheBackend(CacheBackend):
    """SQLite-based persistent cache backend."""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
        
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS translation_cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expires REAL NOT NULL,
                    created REAL NOT NULL
                )
            """)
            
            # Create index on expires for cleanup
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires 
                ON translation_cache(expires)
            """)
            
            conn.commit()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from SQLite cache."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute(
                "SELECT value, expires FROM translation_cache WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()
            
            if row:
                value_json, expires = row
                if time.time() < expires:
                    self._stats["hits"] += 1
                    return json.loads(value_json)
                else:
                    # Expired - remove it
                    conn.execute("DELETE FROM translation_cache WHERE key = ?", (key,))
                    conn.commit()
            
            self._stats["misses"] += 1
            return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int):
        """Set value in SQLite cache."""
        now = time.time()
        expires = now + ttl
        value_json = json.dumps(value)
        
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO translation_cache 
                (key, value, expires, created) 
                VALUES (?, ?, ?, ?)
            """, (key, value_json, expires, now))
            conn.commit()
        
        self._stats["sets"] += 1
    
    def delete(self, key: str):
        """Delete value from SQLite cache."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute(
                "DELETE FROM translation_cache WHERE key = ?",
                (key,)
            )
            if cursor.rowcount > 0:
                self._stats["deletes"] += 1
            conn.commit()
    
    def clear(self):
        """Clear SQLite cache."""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("DELETE FROM translation_cache")
            conn.commit()
    
    def cleanup_expired(self):
        """Remove expired entries from cache."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute(
                "DELETE FROM translation_cache WHERE expires < ?",
                (time.time(),)
            )
            deleted = cursor.rowcount
            conn.commit()
            
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} expired cache entries")
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM translation_cache")
            size = cursor.fetchone()[0]
            
            cursor = conn.execute(
                "SELECT COUNT(*) FROM translation_cache WHERE expires > ?",
                (time.time(),)
            )
            active = cursor.fetchone()[0]
        
        return {
            **self._stats,
            "size": size,
            "active": active,
            "expired": size - active
        }


class RedisCacheBackend(CacheBackend):
    """Redis-based cache backend."""
    
    def __init__(self, host: str = "localhost", port: int = 6379, 
                 db: int = 0, password: Optional[str] = None):
        try:
            import redis
        except ImportError:
            raise ImportError(
                "Redis cache backend requires redis-py. "
                "Install with: pip install redis"
            )
        
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
        
        # Test connection
        try:
            self.redis.ping()
        except redis.ConnectionError:
            raise ConnectionError(f"Failed to connect to Redis at {host}:{port}")
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from Redis cache."""
        value = self.redis.get(f"kimera:translation:{key}")
        
        if value:
            self._stats["hits"] += 1
            return json.loads(value)
        
        self._stats["misses"] += 1
        return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int):
        """Set value in Redis cache."""
        redis_key = f"kimera:translation:{key}"
        value_json = json.dumps(value)
        
        self.redis.setex(redis_key, ttl, value_json)
        self._stats["sets"] += 1
    
    def delete(self, key: str):
        """Delete value from Redis cache."""
        redis_key = f"kimera:translation:{key}"
        if self.redis.delete(redis_key) > 0:
            self._stats["deletes"] += 1
    
    def clear(self):
        """Clear Redis cache."""
        # Delete all keys matching our pattern
        pattern = "kimera:translation:*"
        cursor = 0
        
        while True:
            cursor, keys = self.redis.scan(cursor, match=pattern, count=100)
            if keys:
                self.redis.delete(*keys)
            if cursor == 0:
                break
    
    def stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        # Count keys matching our pattern
        pattern = "kimera:translation:*"
        cursor = 0
        count = 0
        
        while True:
            cursor, keys = self.redis.scan(cursor, match=pattern, count=100)
            count += len(keys)
            if cursor == 0:
                break
        
        return {
            **self._stats,
            "size": count
        }


class TranslationCache:
    """High-level translation cache manager."""
    
    def __init__(self, backend: str = "memory", ttl: int = 86400, **backend_kwargs):
        """
        Initialize translation cache.
        
        Args:
            backend: Cache backend type (memory, sqlite, redis)
            ttl: Default time-to-live in seconds
            **backend_kwargs: Backend-specific arguments
        """
        self.ttl = ttl
        self.backend = self._create_backend(backend, **backend_kwargs)
    
    def _create_backend(self, backend_type: str, **kwargs) -> CacheBackend:
        """Create cache backend instance."""
        if backend_type == "memory":
            return MemoryCacheBackend()
        elif backend_type == "sqlite":
            db_path = kwargs.get("db_path", "cache/translation_cache.db")
            return SQLiteCacheBackend(db_path)
        elif backend_type == "redis":
            return RedisCacheBackend(**kwargs)
        else:
            raise ValueError(f"Unknown cache backend: {backend_type}")
    
    def _generate_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate cache key for translation."""
        # Create a unique key based on text and languages
        key_data = f"{text}|{source_lang}|{target_lang}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, text: str, source_lang: str, target_lang: str) -> Optional[Dict[str, Any]]:
        """
        Get translation from cache.
        
        Returns:
            Cached translation data or None if not found
        """
        key = self._generate_key(text, source_lang, target_lang)
        return self.backend.get(key)
    
    def set(self, text: str, source_lang: str, target_lang: str, 
            translation: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Store translation in cache.
        
        Args:
            text: Source text
            source_lang: Source language code
            target_lang: Target language code
            translation: Translated text
            metadata: Additional metadata to store
        """
        key = self._generate_key(text, source_lang, target_lang)
        
        value = {
            "source_text": text,
            "translated_text": translation,
            "source_language": source_lang,
            "target_language": target_lang,
            "cached_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.backend.set(key, value, self.ttl)
    
    def delete(self, text: str, source_lang: str, target_lang: str):
        """Delete specific translation from cache."""
        key = self._generate_key(text, source_lang, target_lang)
        self.backend.delete(key)
    
    def clear(self):
        """Clear all cached translations."""
        self.backend.clear()
        logger.info("Translation cache cleared")
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = self.backend.stats()
        
        # Calculate hit rate
        total_requests = stats.get("hits", 0) + stats.get("misses", 0)
        hit_rate = stats["hits"] / total_requests if total_requests > 0 else 0
        
        return {
            **stats,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }
    
    def cleanup(self):
        """Perform cache cleanup (remove expired entries)."""
        if hasattr(self.backend, "cleanup_expired"):
            self.backend.cleanup_expired()


# Factory function for creating cache instances
def create_translation_cache(config: Dict[str, Any]) -> TranslationCache:
    """
    Create translation cache from configuration.
    
    Args:
        config: Cache configuration dictionary
        
    Returns:
        TranslationCache instance
    """
    backend = config.get("backend", "memory")
    ttl = config.get("ttl", 86400)
    
    backend_kwargs = {}
    
    if backend == "sqlite":
        backend_kwargs["db_path"] = config.get("sqlite_path", "cache/translation_cache.db")
    elif backend == "redis":
        redis_config = config.get("redis", {})
        backend_kwargs.update({
            "host": redis_config.get("host", "localhost"),
            "port": redis_config.get("port", 6379),
            "db": redis_config.get("db", 0),
            "password": redis_config.get("password")
        })
    
    return TranslationCache(backend=backend, ttl=ttl, **backend_kwargs)