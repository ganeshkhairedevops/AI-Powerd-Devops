function Message({ role, text }) {

    const isUser = role === "user";

    return (

        <div
            className={`flex mb-4 ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >

            <div
                className={`max-w-3xl rounded-xl px-4 py-3 ${
                    isUser
                        ? "bg-cyan-600 text-white"
                        : "bg-slate-800 text-white"
                }`}
            >
                {text}
            </div>

        </div>

    );

}

export default Message;