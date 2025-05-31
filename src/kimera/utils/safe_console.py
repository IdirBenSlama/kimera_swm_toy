"""
Safe console output for cross-platform compatibility
"""
import sys
import os

def puts(msg: str, *, emoji_ok: bool = False):
    """
    Print without choking on Windows code pages.
    If emoji_ok is False, emojis are stripped/replaced.
    
    Args:
        msg: Message to print
        emoji_ok: If False, emojis will be replaced with ASCII on Windows CP1252
    """
    if os.name == "nt" and sys.stdout.encoding and sys.stdout.encoding.lower().startswith("cp12"):
        if not emoji_ok:
            # Replace common emojis with ASCII equivalents
            replacements = {
                "🚀": "[START]",
                "✅": "[PASS]", 
                "❌": "[FAIL]",
                "⚠️": "[WARN]",
                "🧪": "[TEST]",
                "📊": "[STATS]",
                "🎉": "[SUCCESS]",
                "💥": "[ERROR]",
                "📁": "[FILES]",
                "⏱️": "[TIME]",
                "📈": "[RESULTS]",
                "🔍": "[CHECK]",
                "📄": "[FILE]",
            }
            
            for emoji, replacement in replacements.items():
                msg = msg.replace(emoji, replacement)
            
            # Fallback: encode any remaining problematic characters
            msg = msg.encode("ascii", "backslashreplace").decode()
    
    print(msg)

def safe_print(msg: str):
    """Alias for puts() with emoji_ok=False"""
    puts(msg, emoji_ok=False)