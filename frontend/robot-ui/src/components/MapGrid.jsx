import React from "react";
import "./MapGrid.css";

const cols = 4;
const rows = 2;

export default function MapGrid({ selected, robotPos, onSelect }) {

    const cells = [];
    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const id = y * cols + x;
            const isSelected = selected && selected.x === x && selected.y === y;
            const isRobot = robotPos && robotPos.x === x && robotPos.y === y;

            cells.push(
                <div
                    key={id}
                    className={
                        "cell" +
                        (isSelected ? " selected" : "") +
                        (isRobot ? " robot-pos" : "")
                    }
                    data-id={id}
                    onClick={() => onSelect(x, y)}
                />
            );
        }
    }

    return (
        <div className="map-wrapper">
            <div
                className="map"
                style={{ backgroundImage: "url(/robot-field.png)" }}
            >
                <div className="grid-overlay">
                    {cells}
                </div>
            </div>
        </div>
    );
}

