import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { loadInitialState } from "./lib/islands";
import { applyClientSkinSettings } from "./lib/theme";
import "./styles/tokens.css";
import "./styles/global.css";
import "./styles/document-content.css";

applyClientSkinSettings();

const initial = loadInitialState();
const container = document.getElementById("ringo-app-root");

if (container) {
    createRoot(container).render(
        <StrictMode>
            <App initial={initial} />
        </StrictMode>,
    );
}
