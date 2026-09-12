"""
Test suite for NanoCoT core components and streaming sanitizer.
"""

import asyncio
from core import ComplexityClassifier, MicroCoTInjector, PhysicalResponseSanitizer


def test_complexity_classifier():
    classifier = ComplexityClassifier()
    
    # Simple cases
    assert classifier.classify([{"role": "user", "content": "hi how are you"}]) == False
    assert classifier.classify([{"role": "user", "content": "translate hello to french"}]) == False
    
    # Complex cases
    assert classifier.classify([{"role": "user", "content": "Write a python function to refactor async database connection pool."}]) == True
    assert classifier.classify([{"role": "user", "content": "Explain why this math equation has no real solutions."}]) == True
    print("✓ ComplexityClassifier test passed.")


def test_micro_cot_injector():
    injector = MicroCoTInjector()
    messages = [{"role": "user", "content": "Build a REST API."}]
    injected = injector.inject(messages)
    
    assert len(injected) == 2
    assert injected[0]["role"] == "system"
    assert "<nanocot_think>" in injected[0]["content"]
    print("✓ MicroCoTInjector test passed.")


def test_physical_response_sanitizer_non_streaming():
    sanitizer = PhysicalResponseSanitizer()
    raw_response = (
        "<nanocot_think>\n"
        "- Need FastAPI endpoint\n"
        "- Add CORS\n"
        "</nanocot_think>\n\n"
        "Here is the clean implementation of FastAPI endpoint."
    )
    cleaned = sanitizer.sanitize_text(raw_response)
    assert "<nanocot_think>" not in cleaned
    assert "</nanocot_think>" not in cleaned
    assert cleaned.startswith("Here is the clean implementation")
    print("✓ PhysicalResponseSanitizer Non-Streaming test passed.")


async def test_physical_response_sanitizer_streaming():
    sanitizer = PhysicalResponseSanitizer()
    
    async def mock_stream():
        chunks = [
            "<nano",
            "cot_think>\n- Analyze issue\n- Step 2\n",
            "</nanocot_think>",
            "\n\nFINAL RESULT: ",
            "System is operational."
        ]
        for c in chunks:
            yield c

    result_chunks = []
    async for chunk in sanitizer.sanitize_stream(mock_stream()):
        result_chunks.append(chunk)

    full_output = "".join(result_chunks)
    assert "<nanocot_think>" not in full_output
    assert "Analyze issue" not in full_output
    assert "FINAL RESULT: System is operational." in full_output
    print("✓ PhysicalResponseSanitizer Streaming test passed.")


if __name__ == "__main__":
    test_complexity_classifier()
    test_micro_cot_injector()
    test_physical_response_sanitizer_non_streaming()
    asyncio.run(test_physical_response_sanitizer_streaming())
    print("\nALL NANOCOT ENGINE TESTS PASSED GREEN!")
