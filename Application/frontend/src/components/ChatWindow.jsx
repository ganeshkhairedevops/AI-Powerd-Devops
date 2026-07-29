import { useEffect, useRef } from "react";

import Message from "./Message";
import PromptBox from "./PromptBox";

import useChat from "../hooks/useChat";
import { useChatContext } from "../context/ChatContext";

function ChatWindow() {

    const { currentChat } = useChatContext();

    const { loading, sendMessage } = useChat();

    const messages = currentChat?.messages || [];

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });

    }, [messages]);

    return (

        <div className="flex flex-col flex-1">

            <div className="flex-1 overflow-auto p-8">

                {messages.map((message, index) => (

                    <Message
                        key={index}
                        role={message.role}
                        text={message.content}
                    />

                ))}

                {loading && (

                    <div className="text-gray-400 animate-pulse mt-4">

                        ?? AI is thinking...

                    </div>

                )}

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