import MarkdownRenderer from "./chat/MarkdownRenderer";
import Avatar from "./chat/Avatar";

function Message({ role, text }) {
  const isUser = role === "user";

  return (
    <div
      className={`mb-6 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`flex max-w-5xl items-start gap-3 ${
          isUser ? "flex-row-reverse" : "flex-row"
        }`}
      >
        <Avatar role={role} />

        <div
          className={`rounded-xl px-4 py-3 shadow-md ${
            isUser
              ? "bg-cyan-600 text-white"
              : "bg-slate-800 text-gray-100 border border-slate-700"
          }`}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{text}</p>
          ) : (
            <div className="prose prose-invert max-w-none">
              <MarkdownRenderer content={text} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Message;