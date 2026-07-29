import { useMemo, useState } from "react";
import { FaPlus } from "react-icons/fa";
import { useChatContext } from "../context/ChatContext";
import SearchBar from "./SearchBar";
import HistoryItem from "./HistoryItem";

function ChatHistory() {
    const {
        conversations,
        currentChatId,
        createNewChat,
        deleteChat,
        renameChat,
        setCurrentChatId,
    } = useChatContext();

    const [search, setSearch] = useState("");

    const filteredChats = useMemo(() => {
        return conversations.filter((chat) =>
            chat.title
                .toLowerCase()
                .includes(search.toLowerCase())
        );
    }, [conversations, search]);

    return (
        <>
            <button
                onClick={createNewChat}
                className="w-full flex items-center justify-center gap-2 rounded-lg bg-blue-600 py-2 hover:bg-blue-700 transition"
            >
                <FaPlus />
                New Chat
            </button>

            <div className="mt-4">
                <SearchBar
                    value={search}
                    onChange={setSearch}
                />
            </div>

            <div className="mt-6">
                <h3 className="text-xs uppercase text-gray-400 mb-2">
                    Recent Chats
                </h3>

                <div className="space-y-2">
                    {filteredChats.map((chat) => (
                        <HistoryItem
                            key={chat.id}
                            chat={chat}
                            active={
                                chat.id === currentChatId
                            }
                            onSelect={
                                setCurrentChatId
                            }
                            onRename={
                                renameChat
                            }
                            onDelete={
                                deleteChat
                            }
                        />
                    ))}
                </div>
            </div>
        </>
    );
}

export default ChatHistory;