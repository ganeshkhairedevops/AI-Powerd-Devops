import { useState } from "react";
import MarkdownRenderer from "./chat/MarkdownRenderer";
import Avatar from "./chat/Avatar";
import {
  FaFileAlt,
  FaChevronDown,
  FaChevronRight,
  FaDatabase,
  FaRoute,
  FaListOl,
  FaChartLine,
} from "react-icons/fa";

function Message({
  role,
  text,
  sources = [],
  retrieval = null,
  route = null,
}) {
  const isUser = role === "user";

  const [showDetails, setShowDetails] =
    useState(false);

  const hasSources =
    !isUser &&
    Array.isArray(sources) &&
    sources.length > 0;

  const hasRetrieval =
    !isUser &&
    route === "rag" &&
    retrieval &&
    typeof retrieval === "object" &&
    Array.isArray(retrieval.results) &&
    retrieval.results.length > 0;

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
              : "border border-slate-700 bg-slate-800 text-gray-100"
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

          {/* ================================================= */}
          {/* RAG Debug / Retrieval Details */}
          {/* ================================================= */}

          {hasRetrieval && (
            <div className="mt-3 border-t border-slate-700 pt-3">

              {/* Details Header */}

              <button
                type="button"
                onClick={() =>
                  setShowDetails(
                    previous => !previous
                  )
                }
                className="
                  flex
                  w-full
                  items-center
                  justify-between
                  rounded-lg
                  px-2
                  py-2
                  text-left
                  transition
                  hover:bg-slate-900
                "
              >
                <div className="flex items-center gap-2">

                  <FaDatabase className="text-cyan-400" />

                  <span className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                    RAG Details
                  </span>

                </div>

                {showDetails ? (
                  <FaChevronDown className="text-xs text-slate-500" />
                ) : (
                  <FaChevronRight className="text-xs text-slate-500" />
                )}

              </button>


              {/* Details Content */}

              {showDetails && (
                <div className="mt-3 space-y-3">

                  {/* Route */}

                  <div className="flex items-center justify-between rounded-lg bg-slate-900 px-3 py-2">

                    <div className="flex items-center gap-2">

                      <FaRoute className="text-cyan-400" />

                      <span className="text-xs text-slate-400">
                        Route
                      </span>

                    </div>

                    <span className="text-xs font-medium uppercase text-cyan-400">
                      {route || "rag"}
                    </span>

                  </div>


                  {/* Chunks Retrieved */}

                  <div className="flex items-center justify-between rounded-lg bg-slate-900 px-3 py-2">

                    <div className="flex items-center gap-2">

                      <FaListOl className="text-cyan-400" />

                      <span className="text-xs text-slate-400">
                        Chunks Retrieved
                      </span>

                    </div>

                    <span className="text-xs font-medium text-slate-200">
                      {retrieval.chunks_retrieved ??
                        retrieval.results.length}
                    </span>

                  </div>


                  {/* Retrieval Results */}

                  <div className="rounded-lg bg-slate-900 p-3">

                    <div className="mb-2 flex items-center gap-2">

                      <FaChartLine className="text-cyan-400" />

                      <span className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                        Retrieval Results
                      </span>

                    </div>


                    <div className="space-y-2">

                      {retrieval.results.map(
                        (result, index) => (
                          <div
                            key={`${result.filename}-${result.chunk}-${index}`}
                            className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2"
                          >

                            <div className="flex items-center justify-between gap-3">

                              <div className="flex min-w-0 items-center gap-2">

                                <FaFileAlt className="shrink-0 text-slate-500" />

                                <span className="truncate text-xs text-slate-300">
                                  {result.filename}
                                </span>

                              </div>

                              <span className="shrink-0 text-xs text-slate-500">
                                Chunk{" "}
                                {result.chunk}
                              </span>

                            </div>


                            {/* Score */}

                            {result.score !== null &&
                              result.score !== undefined && (
                                <div className="mt-2 flex items-center justify-between">

                                  <span className="text-xs text-slate-500">
                                    Distance Score
                                  </span>

                                  <span className="font-mono text-xs text-cyan-400">
                                    {Number(
                                      result.score
                                    ).toFixed(4)}
                                  </span>

                                </div>
                              )}

                          </div>
                        )
                      )}

                    </div>

                  </div>

                </div>
              )}

            </div>
          )}

        </div>
      </div>
    </div>
  );
}

export default Message;