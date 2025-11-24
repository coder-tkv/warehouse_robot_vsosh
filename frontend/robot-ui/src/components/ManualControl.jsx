import React, { useState } from "react";
import { sendManual } from "../api/robotApi";

export default function ManualControl({ selected, setSelected }) {
    const [status, setStatus] = useState("");

    const sendCommand = async () => {
        if (!selected) {
            setStatus("Выберите клетку на карте.");
            return;
        }

        try {
            await sendManual(selected.x, selected.y);
            setStatus(`Команда отправлена! (x=${selected.x}, y=${selected.y})`);
        } catch (e) {
            setStatus("Ошибка отправки.");
        }
    };

    return (
        <>
            <p className="mode-description">
                Нажмите на клетку на поле.
            </p>

            <button className="btn-primary" onClick={sendCommand}>
                Отправить координаты
            </button>

            <p className="status">{status}</p>
        </>
    );
}
