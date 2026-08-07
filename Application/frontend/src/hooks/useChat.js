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

        // Create chat automatically
        if (!chatId) {
            chatId = createNewChat();
        }

        const existingMessages =
            currentChat?.messages || [];

        const updatedMessages = [
            ...existingMessages,
            {
                role: "user",
                content: question,
            },
        ];

        updateMessages(chatId, updatedMessages);

        setLoading(true);

        try {

            const res = await api.post("/chat", {

                conversation_id: String(chatId),

                message: question,

            });

            updateMessages(chatId, [

                ...updatedMessages,

                {
                    role: "assistant",
                    content: res.data.answer,
                },

            ]);

        }

        catch {

            updateMessages(chatId, [

                ...updatedMessages,

                {
                    role: "assistant",
                    content: "Unable to connect to backend.",
                },

            ]);

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