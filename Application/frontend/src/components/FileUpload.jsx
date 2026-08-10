import { useRef, useState } from "react";
import api from "../services/api";

function FileUpload() {
    const fileInputRef = useRef(null);

    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    async function handleFile(file) {
        if (!file) {
            return;
        }

        setUploading(true);
        setMessage("");
        setError("");

        const formData = new FormData();

        formData.append("file", file);

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

            if (response.data.success) {
                setMessage(
                    `${response.data.filename} uploaded successfully (${response.data.chunks} chunks)`
                );
            } else {
                setError(
                    response.data.message ||
                    "File upload failed."
                );
            }

        } catch (err) {
            console.error("Upload error:", err);

            setError(
                err.response?.data?.message ||
                "Unable to upload file."
            );

        } finally {
            setUploading(false);
        }
    }

    function handleFileChange(event) {
        const file = event.target.files?.[0];

        handleFile(file);
    }

    function openFilePicker() {
        fileInputRef.current?.click();
    }

    return (
        <div className="px-6 pb-3">

            <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileChange}
            />

            <div
                onClick={openFilePicker}
                className="
                    border border-dashed
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
                            ?? Upload DevOps File
                        </p>

                        <p className="text-xs text-gray-500 mt-1">
                            YAML, JSON, Dockerfile, Terraform,
                            Markdown, logs and more
                        </p>
                    </>
                )}

            </div>

            {message && (
                <p className="text-sm text-green-400 mt-2">
                    {message}
                </p>
            )}

            {error && (
                <p className="text-sm text-red-400 mt-2">
                    {error}
                </p>
            )}

        </div>
    );
}

export default FileUpload;