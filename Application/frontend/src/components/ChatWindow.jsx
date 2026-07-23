import { useState, useEffect, useRef } from "react";

import api from "../services/api";

import Message from "./Message";

import PromptBox from "./PromptBox";

import ToolExecution from "./ToolExecution";

function ChatWindow() {

    const [messages,setMessages]=useState([]);

    const [loading,setLoading]=useState(false);

    const [toolInfo, setToolInfo] = useState({
      tool: "",
      command: "",
      execution_time: 0
    });

    const bottomRef = useRef(null);

    async function askAgent(question){

        const updated=[
            ...messages,
            {
                role:"user",
                text:question
            }
        ];

        setMessages(updated);

        setLoading(true);

        try{

            const res=await api.post("/chat",{

                message:question

            });

            setToolInfo({
                tool: res.data.tool,
                command: res.data.command,
                execution_time: res.data.execution_time,
            });

            setMessages([
                ...updated,
                {
                    role:"assistant",
                    text:res.data.answer
                }
            ]);

        }

        catch(error){

            setMessages([
                ...updated,
                {
                    role:"assistant",
                    text:"Unable to connect to backend."
                }
            ]);

        }

        setLoading(false);

    }

    useEffect(()=>{

        bottomRef.current?.scrollIntoView({ behavior: "smooth" });

    }, [messages]);

    return(

        <div className="flex flex-col flex-1">

            <div className="flex-1 overflow-auto p-8">

                {
                    messages.map((m,index)=>

                        <Message
                            key={index}
                            role={m.role}
                            text={m.text}
                        />

                    )
                }
                {
                    loading && (

                        <div className="text-gray-400 animate-pulse mt-4">
                            
                            AI is thinking...
                        </div>
                    
                )}

            </div>

            <PromptBox
                onSend={askAgent}
                loading={loading}
            />
            <ToolExecution
                tool={toolInfo.tool}
                command={toolInfo.command}
                execution={toolInfo.execution_time}
            />

        </div>

    );

}

export default ChatWindow;