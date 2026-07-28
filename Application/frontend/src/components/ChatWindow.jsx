import { useEffect, useRef } from "react";

import Message from "./Message";
import PromptBox from "./PromptBox";

import useChat from "../hooks/useChat";

function ChatWindow() {

    const {
        messages,
        loading,
        sendMessage,
    } = useChat();

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });

    }, [messages]);

    return (

        <div className="flex flex-col flex-1">

            <div className="flex-1 overflow-auto p-8">

                {
                    messages.map((m, index) => (

                        <Message
                            key={index}
                            role={m.role}
                            text={m.text}
                        />

                    ))
                }

                {
                    loading && (

                        <div className="text-gray-400 animate-pulse mt-4">

                            ?? AI is thinking...

                        </div>

                    )
                }

                <div ref={bottomRef}></div>

            </div>

            <PromptBox
                onSend={sendMessage}
                loading={loading}
            />

        </div>

    );

}

export default ChatWindow;