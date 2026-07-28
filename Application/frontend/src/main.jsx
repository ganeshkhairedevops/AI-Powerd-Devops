import React from "react";
import ReactDOM from "react-dom/client";

import "./index.css";
import App from "./App";

import { ChatProvider } from "./context/ChatContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChatProvider>
      <App />
    </ChatProvider>
  </React.StrictMode>
);