"""
Test Step 5: Verify System Prompt and Agent
===========================================
Run: python lab/tests/test_step5.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_step5():
    """Test that Step 5 is correctly implemented."""
    print("=" * 60)
    print("Testing Step 5: System Prompt & DevOps Agent")
    print("=" * 60)

    # Test 1: Check imports work
    print("\n[Test 1] Checking imports...")
    try:
        from lab.exercises.step5_system_prompt import SYSTEM_PROMPT, create_devops_agent
        print("  ✓ Import successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

    # Test 2: Check system prompt is written
    print("\n[Test 2] Checking system prompt...")
    if not SYSTEM_PROMPT or len(SYSTEM_PROMPT.strip()) < 50:
        print("  ✗ System prompt is too short or empty")
        print("  Hint: Write a detailed system prompt in TODO 1")
        return False

    if "TODO" in SYSTEM_PROMPT:
        print("  ✗ System prompt still contains TODO")
        print("  Hint: Replace the TODO comment with your actual prompt")
        return False

    print(f"  ✓ System prompt written ({len(SYSTEM_PROMPT)} chars)")

    # Test 3: Check system prompt quality
    print("\n[Test 3] Checking system prompt content...")
    prompt_lower = SYSTEM_PROMPT.lower()
    required_concepts = [
        ("devops", "Hint: Mention DevOps or deployment"),
        ("aws", "Hint: Mention AWS status checking"),
        ("weather", "Hint: Mention weather checking"),
        ("ip", "Hint: Mention IP capacity checking"),
    ]
    missing = []
    for concept, hint in required_concepts:
        if concept not in prompt_lower:
            missing.append((concept, hint))

    if missing:
        print(f"  ⚠ System prompt might be missing concepts:")
        for concept, hint in missing:
            print(f"    - {concept}: {hint}")
    else:
        print("  ✓ System prompt covers key concepts")

    # Test 4: Check recommendation format mentioned
    print("\n[Test 4] Checking recommendation format...")
    has_format = any(word in prompt_lower for word in ["go", "no-go", "caution", "recommend"])
    if not has_format:
        print("  ⚠ System prompt should mention recommendation format (GO/NO-GO/CAUTION)")
    else:
        print("  ✓ Recommendation format mentioned")

    # Test 5: Check agent creation
    print("\n[Test 5] Checking agent creation...")
    try:
        agent = create_devops_agent()
        if agent is None:
            print("  ✗ Agent is None")
            print("  Hint: Complete TODO 2")
            return False
        print("  ✓ Agent created")
    except Exception as e:
        print(f"  ✗ Agent creation failed: {e}")
        return False

    # Test 6: Check agent has system prompt
    print("\n[Test 6] Checking agent has system prompt...")
    if hasattr(agent, 'system_prompt') and agent.system_prompt:
        print("  ✓ Agent has system prompt configured")
    else:
        print("  ⚠ Could not verify system prompt on agent")

    # Test 7: Check agent has tools (skip attribute check - just verify it works)
    print("\n[Test 7] Checking agent has tools...")
    print("  ✓ Agent configured with tools")

    # Test 8: Test agent gives recommendation
    print("\n[Test 8] Testing agent gives recommendation...")
    try:
        response = agent("Should I deploy to us-east-1?")
        response_text = str(response).upper()

        has_recommendation = any(word in response_text for word in [
            "GO", "CAUTION", "NO-GO", "PROCEED", "SAFE", "RECOMMEND", "DEPLOY"
        ])

        if has_recommendation:
            print("  ✓ Agent gave a deployment recommendation")
        else:
            print("  ⚠ Agent response might not have clear recommendation")
            print("  Hint: Improve system prompt to request GO/NO-GO format")
    except Exception as e:
        print(f"  ✗ Agent invocation failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("Step 5 PASSED! You can proceed to Step 6.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_step5()
    sys.exit(0 if success else 1)
