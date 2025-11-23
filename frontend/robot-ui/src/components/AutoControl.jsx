import React, { useState } from "react";
import { sendAuto } from "../api/robotApi";

export default function AutoControl() {
    const [status, setStatus] = useState("");

    const startAuto = async () => {
        try {
            await sendAuto();
            setStatus("Авто-режим запущен!");
        } catch (e) {
            setStatus("Ошибка.");
        }
    };

    return (
        <>
            <p className="mode-description">
                Робот сам определяет цель и маршрут.
            </p>

            <button className="btn-primary" onClick={startAuto}>
                Запустить авто-режим
            </button>

            <p className="status">{status}</p>
        </>
    );
}
