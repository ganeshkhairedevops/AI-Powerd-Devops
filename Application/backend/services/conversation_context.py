"""
Conversation Context

Resolves follow-up questions using the existing
conversation history.

The resolver does not modify or store memory.
It only creates a context-aware version of the
current question for internal processing.
"""

from llm import llm


class ConversationContext:

    # =================================================
    # Configuration
    # =================================================

    MAX_HISTORY_MESSAGES = 10

    FOLLOW_UP_WORDS = {
        "it",
        "its",
        "they",
        "them",
        "their",
        "this",
        "that",
        "these",
        "those",
        "he",
        "she",
    }

    # =================================================
    # Resolve Question
    # =================================================

    def resolve_question(
        self,
        question: str,
        history,
    ) -> str:
        """
        Resolve a follow-up question using
        previous conversation history.

        If the question does not depend on previous
        context, return it unchanged.
        """

        if not question:
            return question

        if not history:
            return question

        # -------------------------------------------------
        # Build history
        # -------------------------------------------------

        history_parts = []

        for message in history:

            role = getattr(
                message,
                "role",
                None,
            )

            content = getattr(
                message,
                "content",
                None,
            )

            if not role or not content:
                continue

            history_parts.append(
                f"{role}: {content}"
            )

        if not history_parts:
            return question

        recent_history = history_parts[
            -self.MAX_HISTORY_MESSAGES:
        ]

        history_text = "\n".join(
            recent_history
        )

        # -------------------------------------------------
        # Detect obvious follow-up references
        # -------------------------------------------------

        question_words = set(
            question.lower()
            .replace("?", "")
            .replace(",", "")
            .split()
        )

        contains_reference = bool(
            question_words
            & self.FOLLOW_UP_WORDS
        )
        # -------------------------------------------------
        # Self-contained question
        # -------------------------------------------------

        if not contains_reference:

            return question

        # -------------------------------------------------
        # Prompt
        # -------------------------------------------------

        prompt = f"""
You are the conversation-context resolver for
a DevOps AI assistant.

Your ONLY job is to rewrite the CURRENT QUESTION
so that it is completely self-contained.

Do NOT answer the question.

## CONVERSATION HISTORY

{history_text}

## CURRENT QUESTION

{question}

## IMPORTANT RULES

1. If the current question is self-contained,
   return it unchanged.

2. If the current question contains a reference such as:
   it, its, they, them, their, this, that, these, those,
   the pod, the deployment, the container, the service,
   or another reference whose meaning comes from the
   conversation history, you MUST resolve that reference.

3. Use the most recent relevant subject from the
   conversation history.

4. Preserve the user's original intent.

5. Do not answer the question.

6. Do not explain your reasoning.

7. Do not use Markdown.

8. Return ONLY the rewritten question.

## EXAMPLE

Conversation:

user: Which image is used by the nginx deployment?
assistant: nginx:1.27
user: How many replicas does it have?

Current question:

How many replicas does it have?

Correct resolved question:

How many replicas does the nginx deployment have?

## ANOTHER EXAMPLE

Conversation:

user: What port does the nginx service expose?
assistant: Port 80
user: Is it TCP?

Correct resolved question:

Is the nginx service port TCP?

## CURRENT QUESTION

{question}

Resolved question:
"""

        try:

            response = llm.invoke(
                prompt
            )

            if hasattr(
                response,
                "content",
            ):

                resolved = (
                    response.content.strip()
                )

            else:

                resolved = str(
                    response
                ).strip()

            # -------------------------------------------------
            # Clean accidental formatting
            # -------------------------------------------------

            resolved = (
                resolved
                .replace(
                    "Resolved question:",
                    "",
                )
                .strip()
            )

            # Remove accidental quotes
            if (
                len(resolved) >= 2
                and (
                    (
                        resolved.startswith('"')
                        and resolved.endswith('"')
                    )
                    or
                    (
                        resolved.startswith("'")
                        and resolved.endswith("'")
                    )
                )
            ):

                resolved = resolved[1:-1].strip()

            # -------------------------------------------------
            # Safety fallback
            # -------------------------------------------------

            if not resolved:
                return question

            return resolved

        except Exception as exc:

            print(
                "Conversation context resolution failed:",
                str(exc),
            )

            return question


# =====================================================
# Singleton
# =====================================================

conversation_context = ConversationContext()