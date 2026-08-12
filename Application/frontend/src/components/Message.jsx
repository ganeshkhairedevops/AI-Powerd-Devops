import MarkdownRenderer from "./chat/MarkdownRenderer";
import Avatar from "./chat/Avatar";
import { FaFileAlt } from "react-icons/fa";

function Message({
  role,
  text,
  sources = [],
}) {
  const isUser = role === "user";

  const hasSources =
    !isUser &&
    Array.isArray(sources) &&
    sources.length > 0;

  return (
    <div
      className={`mb-6 flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`flex max-w-5xl items-start gap-3 ${
          isUser
            ? "flex-row-reverse"
            : "flex-row"
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
          {/* ================================================= */}
          {/* Message */}
          {/* ================================================= */}

          {isUser ? (
            <p className="whitespace-pre-wrap">
              {text}
            </p>
          ) : (
            <div className="prose prose-invert max-w-none">
              <MarkdownRenderer
                content={text}
              />
            </div>
          )}

          {/* ================================================= */}
          {/* RAG Sources */}
          {/* ================================================= */}

          {hasSources && (
            <div className="mt-4 border-t border-slate-700 pt-3">

              <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                Sources
              </p>

              <div className="space-y-2">

                {sources.map(
                  (source, index) => (
                    <div
                      key={`${source.filename}-${source.chunk}-${index}`}
                      className="flex items-center gap-3 rounded-lg bg-slate-900 px-3 py-2"
                    >

                      <FaFileAlt className="text-cyan-400" />

                      <div className="flex flex-col">

                        <span className="text-sm text-slate-200">
                          {source.filename}
                        </span>

                        <span className="text-xs text-slate-500">
                          Document Chunk{" "}
                          {source.chunk}
                        </span>

                      </div>

                    </div>
                  )
                )}

              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Message;