import { CopyToClipboard } from "react-copy-to-clipboard";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { FaCopy, FaCheck } from "react-icons/fa";
import { useState } from "react";

export default function CodeBlock({ language, value }) {
  const [copied, setCopied] = useState(false);

  return (
    <div className="my-4 overflow-hidden rounded-lg border border-slate-700">
      <div className="flex items-center justify-between bg-slate-800 px-4 py-2 text-sm">
        <span className="text-slate-300">
          {language || "text"}
        </span>

        <CopyToClipboard
          text={value}
          onCopy={() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
          }}
        >
          <button className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300">
            {copied ? <FaCheck /> : <FaCopy />}
            {copied ? "Copied" : "Copy"}
          </button>
        </CopyToClipboard>
      </div>

      <SyntaxHighlighter
        language={language}
        style={vscDarkPlus}
        customStyle={{
          margin: 0,
          borderRadius: 0,
          fontSize: "14px",
        }}
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
}