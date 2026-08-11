import { useChatContext } from "../context/ChatContext";
import { useRef, useState } from "react";
import api from "../services/api";


function FileUpload({ onUploadSuccess }) {

    const fileInputRef = useRef(null);

    const {
        currentChatId,
    } = useChatContext();

    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");


    // =====================================================
    // Upload File
    // =====================================================

    async function handleFile(file) {

        if (!file) {
            return;
        }


        // -------------------------------------------------
        // Make sure a chat is selected
        // -------------------------------------------------

        if (!currentChatId) {

            setError(
                "Please create or select a chat before uploading a file."
            );

            return;
        }


        setUploading(true);
        setMessage("");
        setError("");


        // -------------------------------------------------
        // Create FormData
        // -------------------------------------------------

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        formData.append(
            "conversation_id",
            String(currentChatId)
        );


        // -------------------------------------------------
        // Upload
        // -------------------------------------------------

        try {

            const response = await api.post(
                "/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );


            // -------------------------------------------------
            // Upload successful
            // -------------------------------------------------

            if (response.data.success) {

                setMessage(
                    `${response.data.filename} uploaded successfully (${response.data.chunks} chunks)`
                );


                // Tell ChatWindow that upload completed.
                // DocumentList will refresh automatically.

                if (onUploadSuccess) {

                    onUploadSuccess();

                }

            } else {

                setError(
                    response.data.message ||
                    "File upload failed."
                );

            }

        } catch (err) {

            console.error(
                "Upload error:",
                err
            );


            setError(
                err.response?.data?.message ||
                "Unable to upload file."
            );

        } finally {

            setUploading(false);


            // Allow selecting the same file again.

            if (fileInputRef.current) {

                fileInputRef.current.value = "";

            }

        }

    }


    // =====================================================
    // File Selection
    // =====================================================

    function handleFileChange(event) {

        const file =
            event.target.files?.[0];

        handleFile(file);

    }


    // =====================================================
    // Open File Picker
    // =====================================================

    function openFilePicker() {

        if (!currentChatId) {

            setError(
                "Please create or select a chat before uploading a file."
            );

            return;
        }


        setError("");

        fileInputRef.current?.click();

    }


    // =====================================================
    // Render
    // =====================================================

    return (

        <div className="px-6 pb-3">

            {/* Hidden file input */}

            <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileChange}
            />


            {/* Upload area */}

            <div
                onClick={openFilePicker}
                className="
                    border
                    border-dashed
                    border-slate-700
                    rounded-xl
                    p-4
                    text-center
                    cursor-pointer
                    hover:border-cyan-500
                    hover:bg-slate-900
                    transition
                "
            >

                {uploading ? (

                    <p className="text-cyan-400">
                        Uploading and indexing...
                    </p>

                ) : (

                    <>

                        <p className="text-gray-300">
                            Upload DevOps File
                        </p>

                        <p className="text-xs text-gray-500 mt-1">
                            YAML, JSON, Dockerfile, Terraform,
                            Markdown, logs and more
                        </p>

                    </>

                )}

            </div>


            {/* Success message */}

            {message && (

                <p className="text-sm text-green-400 mt-2">
                    {message}
                </p>

            )}


            {/* Error message */}

            {error && (

                <p className="text-sm text-red-400 mt-2">
                    {error}
                </p>

            )}

        </div>

    );

}


export default FileUpload;