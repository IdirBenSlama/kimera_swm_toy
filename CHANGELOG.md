# Changelog

All notable changes to the Kimera project will be documented in this file.

## [v0.7.1] - 2024-12-19

### Added
- **Echo-form implementation**: Geoids now include an `echo` field containing the trimmed text used for hashing and embedding
- **Stable deterministic hashing**: Geoid IDs are now generated from `sha256(lang + echo)` instead of random UUIDs
- **Whitespace-insensitive deduplication**: Leading/trailing spaces no longer create different embeddings
- **Enhanced explorer**: Added optional Echo columns in the web explorer for better observability

### Changed
- **Geoid structure**: Added `echo` field to the Geoid dataclass
- **Cache keying**: Embedding cache now uses trimmed text (echo) as the key
- **GID generation**: Switched from UUID4 to deterministic SHA256-based hashing

### Technical Details
- Cache invalidation: One-time cache clear required due to key format change
- Backward compatibility: All existing APIs remain unchanged
- Performance: No performance impact, potential cache efficiency gains

### Benefits
- **Debugger friendly**: Every result row shows exactly what text was embedded
- **Stable hashing**: Same text always produces same geoid ID
- **Future-proof**: Foundation for advanced normalization (case folding, Unicode NFC, etc.)

## [v0.7.0] - 2024-12-19

### Added
- Negation fix implementation with environment variable control
- Comprehensive benchmark suite with emoji-safe logging
- PowerShell scripts for cross-platform experiment execution
- Enhanced error analysis tools and explorer interface

### Fixed
- Emoji handling in Windows environments
- Geoid creation patterns across all helper scripts
- Environment variable toggle mechanism for feature flags