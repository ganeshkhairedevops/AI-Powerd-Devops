function Message({ role, text }) {

    const isUser = role === "user";

    return (

        <div
            className={`mb-4 flex ${
                isUser
                    ? "justify-end"
                    : "justify-start"
            }`}
        >

            <div
                className={`max-w-3xl rounded-xl px-4 py-3 whitespace-pre-wrap ${
                    isUser
                        ? "bg-cyan-600 text-white"
                        : "bg-slate-800 text-gray-100"
                }`}
            >

                {text}

            </div>

        </div>

    );

}

export default Message;