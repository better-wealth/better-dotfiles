"""
better-dotfiles/src/better_dotfiles/better_dotfiles.py
better_dotfiles
https://github.com/better-wealth/better-dotfiles
MIT License
2022 (C) John Patrick Roach
"""

logo: str = """ +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |b|e|t|t|e|r|-|d|o|t|f|i|l|e|s|
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"""


def fib(num: int) -> int:
    """Fibonacci test."""
    return num if num < 2 else fib(num - 1) + fib(num - 2)
