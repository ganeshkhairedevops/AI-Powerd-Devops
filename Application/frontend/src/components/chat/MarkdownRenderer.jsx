import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CodeBlock from "./CodeBlock";

export default function MarkdownRenderer({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code({ inline, className, children }) {
          const match = /language-(\w+)/.exec(className || "");

          if (!inline) {
            return (
              <CodeBlock
                language={match?.[1]}
                value={String(children).replace(/\n$/, "")}
              />
            );
          }

          return (
            <code className="rounded bg-slate-800 px-1 py-0.5 text-cyan-300">
              {children}
            </code>
          );
        },
      }}
    >
      {content}
    </ReactMarkdown>
  );
}