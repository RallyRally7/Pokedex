const HP_KEY = "HP";
const HP_BASE_BONUS = 75;
const OTHER_BASE_BONUS = 20;
const MAX_STAT = 360;
const MAX_TOTAL_POINTS = 66;

const baseStats = JSON.parse(document.getElementById("stat-data").dataset.stats);

function statToColor(value, minVal = 20, maxVal = 360) {
    const stops = [
        [220, 20, 60],   // red
        [255, 140, 0],   // orange
        [255, 215, 0],   // yellow
        [50, 180, 50],   // green
        [90, 170, 255],  // light blue
        [20, 30, 150],   // dark blue
    ];
    let t = (value - minVal) / (maxVal - minVal);
    t = Math.max(0, Math.min(1, t));

    const nSegments = stops.length - 1;
    const segment = t * nSegments;
    let idx = Math.floor(segment);
    if (idx >= nSegments) idx = nSegments - 1;
    const localT = segment - idx;

    const c1 = stops[idx];
    const c2 = stops[idx + 1];
    const r = Math.round(c1[0] + (c2[0] - c1[0]) * localT);
    const g = Math.round(c1[1] + (c2[1] - c1[1]) * localT);
    const b = Math.round(c1[2] + (c2[2] - c1[2]) * localT);
    return `rgb(${r}, ${g}, ${b})`;
}

function baseBonus(statKey) {
    return statKey === HP_KEY ? HP_BASE_BONUS : OTHER_BASE_BONUS;
}

function updateRealRow(statKey, points) {
    const real = baseStats[statKey] + baseBonus(statKey) + points;
    const row = document.querySelector(`#real-section .stat-row[data-stat-key="${statKey}"]`);
    const fill = row.querySelector(".stat-bar-fill");
    const valueLabel = row.querySelector(".stat-value");

    fill.style.width = Math.min(100, (real / MAX_STAT) * 100) + "%";
    fill.style.backgroundColor = statToColor(real);
    valueLabel.textContent = real;
}

function getAllPoints() {
    const points = {};
    document.querySelectorAll(".stat-points-input").forEach(input => {
        points[input.dataset.statKey] = parseInt(input.value, 10) || 0;
    });
    return points;
}

function updateTotal() {
    const points = getAllPoints();
    const total = Object.values(points).reduce((sum, v) => sum + v, 0);
    const totalEl = document.getElementById("points-total");
    totalEl.textContent = `Points used: ${total} / ${MAX_TOTAL_POINTS}`;
    totalEl.classList.toggle("over-limit", total > MAX_TOTAL_POINTS);
}

function setPoints(statKey, points) {
    points = Math.max(0, Math.min(32, points));
    document.querySelectorAll(`.stat-slider[data-stat-key="${statKey}"]`).forEach(el => el.value = points);
    document.querySelectorAll(`.stat-points-input[data-stat-key="${statKey}"]`).forEach(el => el.value = points);
    updateRealRow(statKey, points);
    updateTotal();
}

document.querySelectorAll(".stat-slider").forEach(slider => {
    slider.addEventListener("input", () => {
        setPoints(slider.dataset.statKey, parseInt(slider.value, 10));
    });
});

document.querySelectorAll(".stat-points-input").forEach(input => {
    input.addEventListener("input", () => {
        setPoints(input.dataset.statKey, parseInt(input.value, 10) || 0);
    });
});

document.querySelectorAll("#base-section .stat-row[data-stat-key]").forEach(row => {
    const statKey = row.dataset.statKey;
    const fill = row.querySelector(".stat-bar-fill");
    const valueLabel = row.querySelector(".stat-value");
    const value = baseStats[statKey];
    fill.style.width = Math.min(100, (value / MAX_STAT) * 100) + "%";
    fill.style.backgroundColor = statToColor(value);
    valueLabel.textContent = value;
});

Object.keys(baseStats).forEach(statKey => updateRealRow(statKey, 0));
updateTotal();