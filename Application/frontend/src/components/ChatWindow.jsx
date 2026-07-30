import { useEffect, useRef } from "react";
import { FaRobot } from "react-icons/fa";

import Message from "./Message";
import PromptBox from "./PromptBox";
import ConversationHeader from "./ConversationHeader";
import SuggestionCards from "./chat/SuggestionCards";

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
    <div className="flex flex-1 flex-col bg-slate-950">
      {/* Conversation Header */}
      <ConversationHeader />

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-8">
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="mx-auto max-w-4xl text-center">
              {/* Robot Icon */}
              <div className="mb-6 flex justify-center">
                <div className="flex h-20 w-20 items-center justify-center rounded-full border border-slate-700 bg-slate-800">
                  <FaRobot className="text-4xl text-cyan-400" />
                </div>
              </div>

              {/* Welcome Title */}
              <h2 className="mb-4 text-4xl font-bold text-white">
                DevOps AI Agent
              </h2>

              {/* Description */}
              <p className="mb-10 text-lg text-slate-400">
                Ask anything about Docker, Kubernetes, Linux, Terraform,
                AWS, Jenkins, Ansible, GitHub, Helm, Monitoring, or
                DevOps.
              </p>

              {/* Quick Suggestions */}
              <SuggestionCards onSelect={sendMessage} />
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <Message
                key={index}
                role={message.role}
                text={message.content}
              />
            ))}

            {loading && (
              <div className="mt-4 flex animate-pulse items-center gap-3 text-slate-400">
                <FaRobot className="text-cyan-400" />
                <span>AI is thinking...</span>
              </div>
            )}
          </>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Prompt Box */}
      <PromptBox
        onSend={sendMessage}
        loading={loading}
      />
    </div>
  );
}

export default ChatWindow;