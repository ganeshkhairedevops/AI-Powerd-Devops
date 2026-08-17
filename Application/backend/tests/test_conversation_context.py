"""
Conversation Context Test
"""

from memory.models import Message
from services.conversation_context import (
    conversation_context,
)


print("=" * 60)
print("CONVERSATION CONTEXT TEST")
print("=" * 60)


# =====================================================
# Conversation history
# =====================================================

history = [
    Message(
        role="user",
        content=(
            "Which image is used by "
            "the nginx deployment?"
        ),
    ),
    Message(
        role="assistant",
        content="nginx:1.27",
    ),
]


# =====================================================
# Follow-up question
# =====================================================

question = (
    "How many replicas does it have?"
)


resolved = (
    conversation_context.resolve_question(
        question=question,
        history=history,
    )
)


print()
print("Original:")
print(question)

print()
print("Resolved:")
print(resolved)

print()
print("=" * 60)


if resolved:

    print(
        "PASS: Context resolver returned a question."
    )

else:

    print(
        "FAIL: Context resolver returned empty output."
    )