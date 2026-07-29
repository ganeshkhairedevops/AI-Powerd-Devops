import { FaEdit, FaCopy, FaTrash } from "react-icons/fa";
import { useChatContext } from "../context/ChatContext";

function ConversationHeader() {

    const {
        currentChat,
        renameChat,
        deleteChat,
    } = useChatContext();

    if (!currentChat) return null;

    function handleRename() {

        const newTitle = prompt(
            "Rename conversation",
            currentChat.title
        );

        if (
            newTitle &&
            newTitle.trim() !== ""
        ) {

            renameChat(
                currentChat.id,
                newTitle.trim()
            );

        }

    }

    async function handleCopy() {

        const text = currentChat.messages
            .map(
                m =>
                    `${m.role.toUpperCase()}:\n${m.content}`
            )
            .join("\n\n");

        await navigator.clipboard.writeText(text);

    }

    function handleDelete() {

        if (
            window.confirm(
                "Delete this conversation?"
            )
        ) {

            deleteChat(currentChat.id);

        }

    }

    return (

        <div className="border-b border-slate-700 p-4 flex justify-between items-center">

            <div>

                <h2 className="text-xl font-semibold">

                    {currentChat.title}

                </h2>

                <p className="text-sm text-gray-400">

                    {new Date(
                        currentChat.updatedAt
                    ).toLocaleString()}

                </p>

            </div>

            <div className="flex gap-3">

                <button onClick={handleRename}>
                    <FaEdit />
                </button>

                <button onClick={handleCopy}>
                    <FaCopy />
                </button>

                <button onClick={handleDelete}>
                    <FaTrash />
                </button>

            </div>

        </div>

    );

}

export default ConversationHeader;