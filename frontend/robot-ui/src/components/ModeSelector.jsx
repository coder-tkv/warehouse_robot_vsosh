import React from "react";

export default function ModeSelector({ mode, setMode }) {
    return (
        <div className="mode-toggle">
            <button
                className={`mode-btn ${mode === "auto" ? "active" : ""}`}
                onClick={() => setMode("auto")}
            >
                ⚡ Авто
            </button>

            <button
                className={`mode-btn ${mode === "manual" ? "active" : ""}`}
                onClick={() => setMode("manual")}
            >
                🎮 Ручной
            </button>
        </div>
    );
}
