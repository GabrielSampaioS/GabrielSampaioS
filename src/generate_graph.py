from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from leetcode_api import get_calendar

USERNAME = "gabrielsampaios"
YEAR = datetime.now(timezone.utc).year

CELL = 10
GAP = 3
STEP = CELL + GAP
PAD = 12

# Paleta monocromática
BACKGROUND = "#0a0a0a"
EMPTY = "#1a1a1a"
LEVELS = ["#0e4429", "#006d32", "#26a641", "#39d353"]


def color_for(count: int) -> str:
    if count == 0:
        return EMPTY
    if count <= 1:
        return LEVELS[0]
    if count <= 2:
        return LEVELS[1]
    if count <= 5:
        return LEVELS[2]
    return LEVELS[3]


calendar = get_calendar(USERNAME, YEAR)

# Converte timestamps Unix em datas
daily: dict[date, int] = {}
for timestamp, count in calendar.items():
    day = datetime.fromtimestamp(int(timestamp), timezone.utc).date()
    daily[day] = daily.get(day, 0) + int(count)

# Organiza os dias do ano em semanas
start = date(YEAR, 1, 1)
end = date(YEAR, 12, 31)
first_day = start - timedelta(days=start.weekday())

cells = []
current = first_day

while current <= end:
    if current >= start:
        count = daily.get(current, 0)
        x = PAD + ((current - first_day).days // 7) * STEP
        y = PAD + current.weekday() * STEP
        label = "submissão" if count == 1 else "submissões"
        cells.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{color_for(count)}">'
            f"<title>{current}: {count} {label}</title></rect>"
        )
    current += timedelta(days=1)

columns = ((end - first_day).days // 7) + 1
width = PAD * 2 + columns * STEP - GAP
height = PAD * 2 + 7 * STEP - GAP

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
    f'height="{height}" viewBox="0 0 {width} {height}">'
    f'<rect width="100%" height="100%" fill="{BACKGROUND}" rx="6"/>'
    f'{"".join(cells)}'
    f"</svg>"
)

# Caminho relativo ao arquivo, funciona de qualquer diretório
assets_dir = Path(__file__).resolve().parent.parent / "assets"
assets_dir.mkdir(exist_ok=True)
(assets_dir / "leetcode-graph.svg").write_text(svg, encoding="utf-8")

print("Gráfico atualizado!")