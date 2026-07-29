import HistoryItem from "./HistoryItem";
import { useChatContext } from "../context/ChatContext";

function ChatHistory() {

    const {

        conversations,

        createNewChat,

        currentChatId,

        setCurrentChatId

    } = useChatContext();

    return (

        <div className="p-4">

            <button
                onClick={createNewChat}
                className="w-full bg-cyan-600 rounded-lg py-2 mb-5"
            >

                + New Chat

            </button>

            {

                conversations.map(chat => (

                    <HistoryItem

                        key={chat.id}

                        title={chat.title}

                        active={chat.id === currentChatId}

                        onClick={() =>
                            setCurrentChatId(chat.id)
                        }

                    />

                ))

            }

        </div>

    );

}

export default ChatHistory;