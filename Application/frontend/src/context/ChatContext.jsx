import { createContext, useContext, useEffect, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {

    const [conversations, setConversations] = useState(() => {

        const saved = localStorage.getItem("devops-chat");

        return saved ? JSON.parse(saved) : [];

    });

    const [currentChatId, setCurrentChatId] = useState(null);

    useEffect(() => {

        localStorage.setItem(
            "devops-chat",
            JSON.stringify(conversations)
        );

    }, [conversations]);

    function createNewChat() {

        const id = Date.now();

        const chat = {

            id,
            title: "New Chat",
            messages: [],
            createdAt: new Date().toISOString()

        };

        setConversations(prev => [chat, ...prev]);

        setCurrentChatId(id);

    }

    function deleteChat(id) {

        setConversations(prev =>
            prev.filter(chat => chat.id !== id)
        );

        if (currentChatId === id)
            setCurrentChatId(null);

    }

    function updateMessages(chatId, messages) {

        setConversations(prev =>
            prev.map(chat =>
                chat.id === chatId
                    ? { ...chat, messages }
                    : chat
            )
        );

    }

    const currentChat = conversations.find(
        c => c.id === currentChatId
    );

    return (

        <ChatContext.Provider
            value={{
                conversations,
                currentChatId,
                currentChat,
                createNewChat,
                deleteChat,
                updateMessages,
                setCurrentChatId
            }}
        >

            {children}

        </ChatContext.Provider>

    );

}

export function useChatContext() {

    return useContext(ChatContext);

}