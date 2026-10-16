#!/usr/bin/env python3
"""
Collaborative Software Engineering Group Chat
==============================================
Four agents (PM, Developer) collaborate in a round-robin
discussion to implement a software feature. The PM emits TERMINATE once
all unit tests pass.

Usage:
    python main.py
    python main.py "Build a URL shortener"
"""

from __future__ import annotations

import asyncio
import sys

from dotenv import load_dotenv

from coordinator import run_group_chat, print_summary, save_output_to_file

load_dotenv()

DEFAULT_FEATURE = (
    "Build a simple Calculator class in Python that supports: "
    "add, subtract, multiply, divide. "
    "Division by zero should raise ValueError. "
    "Include type hints and full unit test coverage."
)


async def main() -> None:
    feature = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_FEATURE
    print(f"\n  Feature: {feature}\n")
    ctx = await run_group_chat(feature_request=feature, max_turns=24)
    print_summary(ctx)
    out = save_output_to_file(ctx)
    print(f"  Output saved to: {out}\n")


if __name__ == "__main__":
    asyncio.run(main())
