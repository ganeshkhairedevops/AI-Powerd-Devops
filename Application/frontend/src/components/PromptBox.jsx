import { useState } from "react";

function PromptBox({ onSend, loading }) {

    const [question, setQuestion] = useState("");

    function send() {

        if (!question.trim()) return;

        onSend(question);

        setQuestion("");
    }

    return (

        <div className="flex gap-3 p-5 border-t border-slate-700">

            <input
                value={question}
                onChange={(e)=>setQuestion(e.target.value)}
                onKeyDown={(e)=>{

                    if(e.key==="Enter"){

                        send();

                    }

                }}
                className="flex-1 bg-slate-900 rounded-lg p-3 outline-none"
                placeholder="Ask your DevOps question..."
            />

            <button
                onClick={send}
                disabled={loading}
                className="bg-cyan-600 hover:bg-cyan-700 px-6 rounded-lg"
            >
                {loading ? "Thinking..." : "Send"}
            </button>

        </div>

    );

}

export default PromptBox;