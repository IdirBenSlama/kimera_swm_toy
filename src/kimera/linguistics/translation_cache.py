"""
Advanced Translation Caching System

This module provides sophisticated caching mechanisms for translation services including:
- Persistent cache storage (SQLite)
- LRU eviction policy
- Cache warming and preloading
- Statistics and monitoring
"""

import sqlite3
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import logging
from dataclasses import asdict
import pickle

from .translation_service import TranslationResult

logger = logging.getLogger(__name__)


class TranslationCache:
    """Advanced translation cache with persistence and LRU eviction"""
    
    def __init__(
        self,
        cache_dir: Path = None,
        max_memory_items: int = 10000,
        max_disk_items: int = 100000,
        ttl_seconds: int = 86400 * 7,  # 7 days default
        enable_persistence: bool = True
    ):
        self.cache_dir = cache_dir or Path.home() / '.kimera' / 'cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_memory_items = max_memory_items
        self.max_disk_items = max_disk_items
        self.ttl_seconds = ttl_seconds
        self.enable_persistence = enable_persistence
        
        # In-memory LRU cache
        self._memory_cache: Dict[str, Tuple[TranslationResult, datetime]] = {}
        self._access_order: List[str] = []  # For LRU tracking
        
        # Statistics
        self._stats = {
            'memory_hits': 0,
            'disk_hits': 0,
            'misses': 0,
            'evictions': 0,
            'disk_writes': 0,
            'disk_reads': 0
        }
        
        # Initialize persistent storage
        if self.enable_persistence:
            self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database for persistent cache"""
        self.db_path = self.cache_dir / 'translation_cache.db'
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                    cache_key TEXT PRIMARY KEY,
                    source_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    access_count INTEGER DEFAULT 1,
                    last_accessed TIMESTAMP NOT NULL
                )
            ''')
            
            # Create indices for performance
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_expires 
                ON translations(expires_at)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_languages 
                ON translations(source_language, target_language)
            ''')
            conn.commit()
    
    async def get(self, cache_key: str) -> Optional[TranslationResult]:
        """Get translation from cache (memory first, then disk)"""
        
        # Check memory cache first
        if cache_key in self._memory_cache:
            result, expires = self._memory_cache[cache_key]
            if datetime.now() < expires:
                self._stats['memory_hits'] += 1
                self._update_lru(cache_key)
                return result
            else:
                # Expired - remove from memory
                self._remove_from_memory(cache_key)
        
        # Check disk cache if persistence enabled
        if self.enable_persistence:
            result = await self._get_from_disk(cache_key)
            if result:
                self._stats['disk_hits'] += 1
                # Promote to memory cache
                await self._add_to_memory(cache_key, result)
                return result
        
        self._stats['misses'] += 1
        return None
    
    async def put(
        self, 
        cache_key: str, 
        result: TranslationResult,
        ttl_override: Optional[int] = None
    ):
        """Store translation in cache"""
        ttl = ttl_override or self.ttl_seconds
        expires = datetime.now() + timedelta(seconds=ttl)
        
        # Add to memory cache
        await self._add_to_memory(cache_key, result, expires)
        
        # Persist to disk if enabled
        if self.enable_persistence:
            await self._save_to_disk(cache_key, result, expires)
    
    async def _add_to_memory(
        self, 
        cache_key: str, 
        result: TranslationResult,
        expires: Optional[datetime] = None
    ):
        """Add item to memory cache with LRU eviction"""
        if expires is None:
            expires = datetime.now() + timedelta(seconds=self.ttl_seconds)
        
        # Evict if at capacity
        if len(self._memory_cache) >= self.max_memory_items:
            self._evict_lru()
        
        self._memory_cache[cache_key] = (result, expires)
        self._update_lru(cache_key)
    
    def _update_lru(self, cache_key: str):
        """Update LRU access order"""
        if cache_key in self._access_order:
            self._access_order.remove(cache_key)
        self._access_order.append(cache_key)
    
    def _evict_lru(self):
        """Evict least recently used item from memory"""
        if self._access_order:
            lru_key = self._access_order.pop(0)
            if lru_key in self._memory_cache:
                del self._memory_cache[lru_key]
                self._stats['evictions'] += 1
    
    def _remove_from_memory(self, cache_key: str):
        """Remove item from memory cache"""
        if cache_key in self._memory_cache:
            del self._memory_cache[cache_key]
        if cache_key in self._access_order:
            self._access_order.remove(cache_key)
    
    async def _get_from_disk(self, cache_key: str) -> Optional[TranslationResult]:
        """Retrieve translation from disk cache"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM translations 
                    WHERE cache_key = ? AND expires_at > ?
                ''', (cache_key, datetime.now()))
                
                row = cursor.fetchone()
                if row:
                    # Update access statistics
                    conn.execute('''
                        UPDATE translations 
                        SET access_count = access_count + 1,
                            last_accessed = ?
                        WHERE cache_key = ?
                    ''', (datetime.now(), cache_key))
                    conn.commit()
                    
                    self._stats['disk_reads'] += 1
                    
                    # Reconstruct TranslationResult
                    metadata = json.loads(row['metadata']) if row['metadata'] else {}
                    return TranslationResult(
                        source_text=row['source_text'],
                        translated_text=row['translated_text'],
                        source_language=row['source_language'],
                        target_language=row['target_language'],
                        confidence=row['confidence'],
                        metadata=metadata
                    )
        except Exception as e:
            logger.error(f"Error reading from disk cache: {e}")
        
        return None
    
    async def _save_to_disk(
        self, 
        cache_key: str, 
        result: TranslationResult,
        expires: datetime
    ):
        """Save translation to disk cache"""
        try:
            # Check disk cache size and evict if necessary
            await self._evict_disk_if_needed()
            
            with sqlite3.connect(self.db_path) as conn:
                metadata_json = json.dumps(result.metadata) if result.metadata else None
                
                conn.execute('''
                    INSERT OR REPLACE INTO translations
                    (cache_key, source_text, translated_text, source_language,
                     target_language, confidence, metadata, created_at, 
                     expires_at, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    cache_key,
                    result.source_text,
                    result.translated_text,
                    result.source_language,
                    result.target_language,
                    result.confidence,
                    metadata_json,
                    datetime.now(),
                    expires,
                    datetime.now()
                ))
                conn.commit()
                self._stats['disk_writes'] += 1
                
        except Exception as e:
            logger.error(f"Error writing to disk cache: {e}")
    
    async def _evict_disk_if_needed(self):
        """Evict old entries from disk if over capacity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get current count
                count = conn.execute('SELECT COUNT(*) FROM translations').fetchone()[0]
                
                if count >= self.max_disk_items:
                    # Delete oldest 10% of entries
                    to_delete = int(self.max_disk_items * 0.1)
                    conn.execute('''
                        DELETE FROM translations
                        WHERE cache_key IN (
                            SELECT cache_key FROM translations
                            ORDER BY last_accessed ASC
                            LIMIT ?
                        )
                    ''', (to_delete,))
                    conn.commit()
                    self._stats['evictions'] += to_delete
                    
        except Exception as e:
            logger.error(f"Error during disk eviction: {e}")
    
    async def warm_cache(self, translations: List[Tuple[str, TranslationResult]]):
        """Pre-populate cache with translations"""
        for cache_key, result in translations:
            await self.put(cache_key, result)
    
    async def export_cache(self, output_path: Path) -> int:
        """Export cache to file for backup or transfer"""
        exported = 0
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM translations 
                    WHERE expires_at > ?
                    ORDER BY access_count DESC
                ''', (datetime.now(),))
                
                cache_data = []
                for row in cursor:
                    cache_data.append({
                        'cache_key': row['cache_key'],
                        'result': {
                            'source_text': row['source_text'],
                            'translated_text': row['translated_text'],
                            'source_language': row['source_language'],
                            'target_language': row['target_language'],
                            'confidence': row['confidence'],
                            'metadata': json.loads(row['metadata']) if row['metadata'] else {}
                        },
                        'expires_at': row['expires_at'],
                        'access_count': row['access_count']
                    })
                    exported += 1
                
                # Write to file
                with open(output_path, 'wb') as f:
                    f.write(pickle.dumps(cache_data))
                
                logger.info(f"Exported {exported} cache entries to {output_path}")
                
        except Exception as e:
            logger.error(f"Error exporting cache: {e}")
        
        return exported
    
    async def import_cache(self, input_path: Path) -> int:
        """Import cache from backup file"""
        imported = 0
        
        try:
            with open(input_path, 'rb') as f:
                content = f.read()
                cache_data = pickle.loads(content)
            
            for entry in cache_data:
                result = TranslationResult(**entry['result'])
                expires = datetime.fromisoformat(entry['expires_at'])
                
                if expires > datetime.now():
                    await self.put(entry['cache_key'], result)
                    imported += 1
            
            logger.info(f"Imported {imported} cache entries from {input_path}")
            
        except Exception as e:
            logger.error(f"Error importing cache: {e}")
        
        return imported
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = (
            self._stats['memory_hits'] + 
            self._stats['disk_hits'] + 
            self._stats['misses']
        )
        
        memory_hit_rate = (
            self._stats['memory_hits'] / total_requests 
            if total_requests > 0 else 0
        )
        
        overall_hit_rate = (
            (self._stats['memory_hits'] + self._stats['disk_hits']) / total_requests
            if total_requests > 0 else 0
        )
        
        return {
            **self._stats,
            'total_requests': total_requests,
            'memory_hit_rate': memory_hit_rate,
            'overall_hit_rate': overall_hit_rate,
            'memory_size': len(self._memory_cache),
            'memory_capacity': self.max_memory_items,
            'disk_capacity': self.max_disk_items
        }
    
    async def clear(self):
        """Clear all cache entries"""
        self._memory_cache.clear()
        self._access_order.clear()
        
        if self.enable_persistence:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('DELETE FROM translations')
                conn.commit()
        
        logger.info("Translation cache cleared")
    
    async def cleanup_expired(self) -> int:
        """Remove expired entries from cache"""
        cleaned = 0
        
        # Clean memory cache
        expired_keys = []
        for key, (_, expires) in self._memory_cache.items():
            if datetime.now() >= expires:
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_from_memory(key)
            cleaned += 1
        
        # Clean disk cache
        if self.enable_persistence:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    DELETE FROM translations 
                    WHERE expires_at < ?
                ''', (datetime.now(),))
                cleaned += cursor.rowcount
                conn.commit()
        
        logger.info(f"Cleaned up {cleaned} expired cache entries")
        return cleaned