import { useState } from "react";
import api from "../services/api";

export default function useChat() {

    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    async function sendMessage(question) {

        const updated = [
            ...messages,
            {
                role: "user",
                text: question,
            },
        ];

        setMessages(updated);
        setLoading(true);

        try {

            const res = await api.post("/chat", {
                message: question,
            });

            setMessages([
                ...updated,
                {
                    role: "assistant",
                    text: res.data.answer,
                },
            ]);

        } catch {

            setMessages([
                ...updated,
                {
                    role: "assistant",
                    text: "Unable to connect to backend.",
                },
            ]);

        } finally {

            setLoading(false);

        }
    }

    return {
        messages,
        loading,
        sendMessage,
    };
}