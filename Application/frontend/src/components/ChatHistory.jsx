import HistoryItem from "./HistoryItem";

function ChatHistory() {

    const chats = [
        "Docker Containers",
        "Kubernetes Pods",
        "Linux Memory",
    ];

    return (

        <div className="p-4">

            <button
                className="w-full bg-cyan-600 rounded-lg py-2 mb-5"
            >
                + New Chat
            </button>

            {
                chats.map((chat, index) => (

                    <HistoryItem
                        key={index}
                        title={chat}
                    />

                ))
            }

        </div>

    );

}

export default ChatHistory;