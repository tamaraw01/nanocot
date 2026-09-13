#!/usr/bin/env python3
"""
NanoCoT Example: Demonstrating complexity classification and response sanitization
"""

import asyncio
from core import ComplexityClassifier, MicroCoTInjector, PhysicalResponseSanitizer

async def demo():
    classifier = ComplexityClassifier()
    injector = MicroCoTInjector()
    sanitizer = PhysicalResponseSanitizer()

    # Example 1: Simple request
    simple_msgs = [
        {"role": "user", "content": "What is 2 + 2?"}
    ]
    is_complex = classifier.classify(simple_msgs)
    print(f"Simple query 'What is 2 + 2?' - Complex: {is_complex}")
    
    # Example 2: Complex request
    complex_msgs = [
        {"role": "user", "content": "Write a Python function to optimize database queries using connection pooling."}
    ]
    is_complex = classifier.classify(complex_msgs)
    print(f"Complex query detected: {is_complex}")

    # Example 3: Micro-CoT injection
    if is_complex:
        injected = injector.inject(complex_msgs)
        print(f"System directive injected: {injected[0]['role']} message includes reasoning budget")

    # Example 4: Response sanitization
    raw_response = (
        "Let me think about this. <nanocot_think>\n"
        "- Need to handle concurrent connections\n"
        "- Use a pool to reuse connections\n"
        "</nanocot_think>\n\n"
        "Here is the optimized implementation:"
    )
    clean = sanitizer.sanitize_text(raw_response)
    print(f"Sanitized response:\n{clean}")

if __name__ == "__main__":
    asyncio.run(demo())
