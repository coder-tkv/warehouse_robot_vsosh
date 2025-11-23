import React, { useEffect, useState } from "react";
import MapGrid from "./components/MapGrid";
import ModeSelector from "./components/ModeSelector";
import ManualControl from "./components/ManualControl";
import AutoControl from "./components/AutoControl";
import { getRobotPosition } from "./api/robotApi";
import "./styles.css";

export default function App() {
    const [mode, setMode] = useState("auto");
    const [selected, setSelected] = useState(null);
    const [robotPos, setRobotPos] = useState(null);

    // запрашиваем позицию робота каждые 700 мс
    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const pos = await getRobotPosition();
                setRobotPos({ x: pos.x, y: pos.y });
            } catch {}
        }, 700);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="app">
            <header className="header">
                <h1>Панель управления роботом</h1>
                <ModeSelector mode={mode} setMode={setMode} />
            </header>

            <main className="main">
                <section className="card">
                    <h2>Карта поля</h2>
                    <MapGrid
                        selected={selected}
                        robotPos={robotPos}
                        onSelect={(x, y) => setSelected({ x, y })}
                    />

                    <p className="coords">
                        {robotPos
                            ? `Робот сейчас: (${robotPos.x}; ${robotPos.y})`
                            : "Позиция робота неизвестна"}
                    </p>
                </section>

                <section className="card">
                    <h2>Управление</h2>

                    {mode === "auto" ? (
                        <AutoControl />
                    ) : (
                        <ManualControl selected={selected} setSelected={setSelected} />
                    )}
                </section>
            </main>
        </div>
    );
}
