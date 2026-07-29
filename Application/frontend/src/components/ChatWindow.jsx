import { useEffect, useRef } from "react";

import Message from "./Message";
import PromptBox from "./PromptBox";
import ConversationHeader from "./ConversationHeader";

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

    }, [messages, loading]);

    return (

        <div className="flex flex-col flex-1 bg-slate-950">

            {/* Conversation Header */}
            <ConversationHeader />

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-8">

                {
                    messages.length === 0 ? (

                        <div className="flex flex-col items-center justify-center h-full text-center text-gray-400">

                            <h2 className="text-3xl font-bold mb-4">
                                ?? DevOps AI Agent
                            </h2>

                            <p className="max-w-xl">
                                Ask anything about Docker, Kubernetes,
                                Linux, Terraform, AWS, Jenkins,
                                Ansible, GitHub, Helm, or DevOps.
                            </p>

                        </div>

                    ) : (

                        messages.map((message, index) => (

                            <Message
                                key={index}
                                role={message.role}
                                text={message.content}
                            />

                        ))

                    )
                }

                {
                    loading && (

                        <div className="flex items-center gap-2 text-gray-400 mt-4 animate-pulse">

                            ?? <span>AI is thinking...</span>

                        </div>

                    )
                }

                <div ref={bottomRef}></div>

            </div>

            {/* Prompt */}
            <PromptBox
                onSend={sendMessage}
                loading={loading}
            />

        </div>

    );

}

export default ChatWindow;