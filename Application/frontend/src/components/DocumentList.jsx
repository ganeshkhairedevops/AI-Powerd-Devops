import { useEffect, useState } from "react";
import api from "../services/api";
import { useChatContext } from "../context/ChatContext";


function DocumentList({ refreshKey = 0 }) {

    const {
        currentChatId,
    } = useChatContext();


    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(false);

    const [deleting, setDeleting] = useState(null);

    const [error, setError] = useState("");


    // =====================================================
    // Load Documents
    // =====================================================

    async function loadDocuments() {

        if (!currentChatId) {

            setDocuments([]);

            return;
        }


        setLoading(true);
        setError("");


        try {

            const response = await api.get(
                `/documents/${currentChatId}`
            );


            if (response.data.success) {

                setDocuments(
                    response.data.documents || []
                );

            } else {

                setError(
                    "Unable to load documents."
                );

            }

        } catch (err) {

            console.error(
                "Document loading error:",
                err
            );

            setError(
                err.response?.data?.message ||
                "Unable to load documents."
            );

        } finally {

            setLoading(false);

        }

    }


    // =====================================================
    // Load when:
    //
    // 1. Chat changes
    // 2. New document is uploaded
    // =====================================================

    useEffect(() => {

        loadDocuments();

    }, [
        currentChatId,
        refreshKey,
    ]);


    // =====================================================
    // Delete Document
    // =====================================================

    async function deleteDocument(filename) {

        if (!currentChatId) {

            return;

        }


        const confirmed = window.confirm(
            `Delete ${filename}?`
        );


        if (!confirmed) {

            return;

        }


        setDeleting(filename);
        setError("");


        try {

            const response = await api.delete(
                `/documents/${currentChatId}/${encodeURIComponent(filename)}`
            );


            if (response.data.success) {

                setDocuments(
                    previous =>
                        previous.filter(
                            document =>
                                document.filename !== filename
                        )
                );

            } else {

                setError(
                    response.data.message ||
                    "Unable to delete document."
                );

            }

        } catch (err) {

            console.error(
                "Document deletion error:",
                err
            );


            setError(
                err.response?.data?.message ||
                "Unable to delete document."
            );

        } finally {

            setDeleting(null);

        }

    }


    // =====================================================
    // No Chat Selected
    // =====================================================

    if (!currentChatId) {

        return null;

    }


    // =====================================================
    // Render
    // =====================================================

    return (

        <div className="px-6 pb-3">

            <div
                className="
                    border
                    border-slate-800
                    rounded-xl
                    bg-slate-950
                    p-4
                "
            >

                {/* ------------------------------------------------
                    Header
                ------------------------------------------------- */}

                <div
                    className="
                        flex
                        items-center
                        justify-between
                        mb-3
                    "
                >

                    <div>

                        <p className="text-sm font-medium text-gray-300">
                            Uploaded Documents
                        </p>

                        <p className="text-xs text-gray-500">
                            Documents for this chat
                        </p>

                    </div>


                    {!loading &&
                        documents.length > 0 && (

                        <span className="text-xs text-gray-500">

                            {documents.length}

                            {" "}

                            {documents.length === 1
                                ? "file"
                                : "files"}

                        </span>

                    )}

                </div>


                {/* ------------------------------------------------
                    Loading
                ------------------------------------------------- */}

                {loading && (

                    <p className="text-sm text-gray-500">
                        Loading documents...
                    </p>

                )}


                {/* ------------------------------------------------
                    Error
                ------------------------------------------------- */}

                {error && (

                    <p className="text-sm text-red-400 mb-2">
                        {error}
                    </p>

                )}


                {/* ------------------------------------------------
                    Empty State
                ------------------------------------------------- */}

                {!loading &&
                    !error &&
                    documents.length === 0 && (

                    <p className="text-sm text-gray-500">
                        No documents uploaded to this chat.
                    </p>

                )}


                {/* ------------------------------------------------
                    Document List
                ------------------------------------------------- */}

                {!loading &&
                    documents.length > 0 && (

                    <div className="space-y-2">

                        {documents.map(
                            document => (

                            <div
                                key={document.filename}
                                className="
                                    flex
                                    items-center
                                    justify-between
                                    gap-3
                                    rounded-lg
                                    border
                                    border-slate-800
                                    bg-slate-900
                                    px-3
                                    py-2
                                "
                            >

                                {/* File information */}

                                <div className="min-w-0">

                                    <p
                                        className="
                                            text-sm
                                            text-gray-300
                                            truncate
                                        "
                                        title={
                                            document.filename
                                        }
                                    >

                                        <span className="text-cyan-400 mr-2">
                                            FILE
                                        </span>

                                        {document.filename}

                                    </p>


                                    <p className="text-xs text-gray-500">

                                        {document.chunks}

                                        {" "}

                                        {document.chunks === 1
                                            ? "chunk"
                                            : "chunks"}

                                    </p>

                                </div>


                                {/* Delete button */}

                                <button
                                    type="button"
                                    onClick={() =>
                                        deleteDocument(
                                            document.filename
                                        )
                                    }
                                    disabled={
                                        deleting ===
                                        document.filename
                                    }
                                    className="
                                        shrink-0
                                        rounded-md
                                        border
                                        border-red-900
                                        px-2
                                        py-1
                                        text-xs
                                        text-red-400
                                        hover:bg-red-500/10
                                        hover:text-red-300
                                        disabled:opacity-50
                                        disabled:cursor-not-allowed
                                    "
                                    title="Delete document"
                                >

                                    {deleting ===
                                    document.filename
                                        ? "Deleting..."
                                        : "Delete"}

                                </button>

                            </div>

                        ))}

                    </div>

                )}

            </div>

        </div>

    );

}


export default DocumentList;