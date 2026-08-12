import { useState } from "react";
import api from "../services/api";
import { useChatContext } from "../context/ChatContext";

export default function useChat() {
  const {
    currentChat,
    currentChatId,
    createNewChat,
    updateMessages,
  } = useChatContext();

  const [loading, setLoading] = useState(false);

  async function sendMessage(question) {
    let chatId = currentChatId;

    // =====================================================
    // Create chat automatically
    // =====================================================

    if (!chatId) {
      chatId = createNewChat();
    }

    // =====================================================
    // Existing messages
    // =====================================================

    const existingMessages =
      currentChat?.messages || [];

    // =====================================================
    // Add user message
    // =====================================================

    const updatedMessages = [
      ...existingMessages,
      {
        role: "user",
        content: question,
      },
    ];

    updateMessages(
      chatId,
      updatedMessages
    );

    setLoading(true);

    try {
      // ===================================================
      // Send request to backend
      // ===================================================

      const res = await api.post(
        "/chat",
        {
          conversation_id: String(chatId),
          message: question,
        }
      );

      // ===================================================
      // Backend response
      // ===================================================

      const assistantMessage = {
        role: "assistant",

        content: res.data.answer,

        // =================================================
        // RAG Sources
        // =================================================

        sources: Array.isArray(
          res.data.sources
        )
          ? res.data.sources
          : [],

        // =================================================
        // Route
        // =================================================

        route:
          res.data.route || null,

        // =================================================
        // RAG / Agent flags
        // =================================================

        rag_used:
          res.data.rag_used || false,

        agent_used:
          res.data.agent_used || false,

        // =================================================
        // RAG Retrieval Metadata
        // =================================================

        retrieval:
          res.data.retrieval || null,
      };

      // ===================================================
      // Update conversation
      // ===================================================

      updateMessages(
        chatId,
        [
          ...updatedMessages,
          assistantMessage,
        ]
      );
    }

    catch (error) {
      console.error(
        "Chat error:",
        error
      );

      // ===================================================
      // Error message
      // ===================================================

      updateMessages(
        chatId,
        [
          ...updatedMessages,
          {
            role: "assistant",
            content:
              "Unable to connect to backend.",
            sources: [],
            route: null,
            rag_used: false,
            agent_used: false,
            retrieval: null,
          },
        ]
      );
    }

    finally {
      setLoading(false);
    }
  }

  return {
    loading,
    sendMessage,
  };
}