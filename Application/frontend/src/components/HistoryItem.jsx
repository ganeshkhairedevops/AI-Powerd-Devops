import { useState } from "react";
import { FaEdit, FaTrash, FaCheck } from "react-icons/fa";

function HistoryItem({
    chat,
    active,
    onSelect,
    onRename,
    onDelete,
}) {
    const [editing, setEditing] = useState(false);
    const [title, setTitle] = useState(chat.title);

    function save() {
        if (title.trim()) {
            onRename(chat.id, title.trim());
        }
        setEditing(false);
    }

    return (
        <div
            className={`group rounded-lg p-2 cursor-pointer transition ${
                active
                    ? "bg-blue-600"
                    : "hover:bg-slate-800"
            }`}
        >
            <div className="flex items-center justify-between">
                {editing ? (
                    <input
                        autoFocus
                        value={title}
                        onChange={(e) =>
                            setTitle(e.target.value)
                        }
                        onBlur={save}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") save();
                        }}
                        className="w-full bg-transparent outline-none text-sm"
                    />
                ) : (
                    <span
                        className="flex-1 text-sm truncate"
                        onClick={() => onSelect(chat.id)}
                    >
                        ?? {chat.title}
                    </span>
                )}

                <div className="hidden group-hover:flex gap-2 ml-2">
                    {editing ? (
                        <FaCheck
                            size={12}
                            onClick={save}
                        />
                    ) : (
                        <FaEdit
                            size={12}
                            onClick={() =>
                                setEditing(true)
                            }
                        />
                    )}

                    <FaTrash
                        size={12}
                        onClick={() => onDelete(chat.id)}
                    />
                </div>
            </div>
        </div>
    );
}

export default HistoryItem;