export async function sendAuto() {
    const res = await fetch('/auto', { method: 'POST' });
    return res.json();
}

export async function sendManual(x, y) {
    const res = await fetch(`/manual?x=${x}&y=${y}`, { method: 'POST' });
    return res.json();
}

export async function getRobotPosition() {
    const res = await fetch('/position');
    return res.json();
}
