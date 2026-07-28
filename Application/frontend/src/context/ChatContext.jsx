// src/context/ChatContext.jsx

import { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {
    const [conversations, setConversations] = useState([]);
    const [currentChatId, setCurrentChatId] = useState(null);

    const createNewChat = () => {
        const newChat = {
            id: Date.now(),
            title: "New Chat",
            messages: [],
            createdAt: new Date().toISOString(),
        };

        setConversations((prev) => [newChat, ...prev]);
        setCurrentChatId(newChat.id);
    };

    const deleteChat = (id) => {
        setConversations((prev) =>
            prev.filter((chat) => chat.id !== id)
        );

        if (currentChatId === id) {
            setCurrentChatId(null);
        }
    };

    const updateMessages = (id, messages) => {
        setConversations((prev) =>
            prev.map((chat) =>
                chat.id === id
                    ? { ...chat, messages }
                    : chat
            )
        );
    };

    return (
        <ChatContext.Provider
            value={{
                conversations,
                setConversations,
                currentChatId,
                setCurrentChatId,
                createNewChat,
                deleteChat,
                updateMessages,
            }}
        >
            {children}
        </ChatContext.Provider>
    );
}

export function useChatContext() {
    return useContext(ChatContext);
}