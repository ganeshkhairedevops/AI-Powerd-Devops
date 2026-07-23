import { useState } from "react";

import api from "../services/api";

import Message from "./Message";

import PromptBox from "./PromptBox";

function ChatWindow() {

    const [messages,setMessages]=useState([]);

    const [loading,setLoading]=useState(false);

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

            </div>

            <PromptBox
                onSend={askAgent}
                loading={loading}
            />

        </div>

    );

}

export default ChatWindow;