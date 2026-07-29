import { createContext, useContext, useEffect, useState } from "react";
import {
    saveChats,
    loadChats,
    generateTitle,
} from "../utils/chatUtils";

const ChatContext = createContext();

export function ChatProvider({ children }) {

    const [conversations, setConversations] = useState(loadChats);

    const [currentChatId, setCurrentChatId] = useState(null);

    // Save chats whenever they change
    useEffect(() => {
        saveChats(conversations);
    }, [conversations]);

    // Auto-select first chat on startup
    useEffect(() => {
        if (!currentChatId && conversations.length > 0) {
            setCurrentChatId(conversations[0].id);
        }
    }, [conversations, currentChatId]);

    function createNewChat() {

    const id = Date.now();

    const chat = {

        id,
        title: "New Chat",
        messages: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),

    };

    setConversations(prev => [chat, ...prev]);

    setCurrentChatId(id);

    return id;

    }   

    function deleteChat(id) {

        const updated = conversations.filter(chat => chat.id !== id);

        setConversations(updated);

        if (currentChatId === id) {
            setCurrentChatId(updated.length ? updated[0].id : null);
        }
    }

    function renameChat(id, title) {

        setConversations(prev =>
            prev.map(chat =>
                chat.id === id
                    ? {
                          ...chat,
                          title,
                          updatedAt: new Date().toISOString(),
                      }
                    : chat
            )
        );
    }

    function updateMessages(chatId, messages) {

        setConversations(prev =>
            prev.map(chat => {

                if (chat.id !== chatId) return chat;

                let title = chat.title;

                // Automatically rename after the first user message
                if (
                    chat.title === "New Chat" &&
                    messages.length > 0
                ) {
                    const firstUserMessage = messages.find(
                        message => message.role === "user"
                    );

                    if (firstUserMessage) {
                        title = generateTitle(firstUserMessage.content);
                    }
                }

                return {
                    ...chat,
                    title,
                    messages,
                    updatedAt: new Date().toISOString(),
                };
            })
        );
    }

    const currentChat =
        conversations.find(
            chat => chat.id === currentChatId
        ) || null;

    return (
        <ChatContext.Provider
            value={{
                conversations,
                currentChatId,
                currentChat,

                createNewChat,
                deleteChat,
                renameChat,
                updateMessages,

                setCurrentChatId,
            }}
        >
            {children}
        </ChatContext.Provider>
    );
}

export function useChatContext() {
    return useContext(ChatContext);
}