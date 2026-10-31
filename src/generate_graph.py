
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import calendar

from leetcode_api import get_calendar

USERNAME = "gabrielsampaios"

TODAY = datetime.now(timezone.utc).date()
END = TODAY
START = (END.replace(day=1) - timedelta(days=335)).replace(day=1)

CELL = 10
GAP = 3
STEP = CELL + GAP
MONTH_GAP = 12
PAD = 12

BACKGROUND = "#0a0a0a"
EMPTY = "#1a1a1a"
LEVELS = ["#0e4429", "#006d32", "#26a641", "#39d353"]

TEXT_COLOR = "#8b949e"
FONT_SIZE = 10


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


# Busca os dados dos anos necessários
years = range(START.year, END.year + 1)

daily: dict[date, int] = {}

for year in years:
    calendar_data = get_calendar(USERNAME, year)

    for timestamp, count in calendar_data.items():
        day = datetime.fromtimestamp(
            int(timestamp), timezone.utc
        ).date()

        if START <= day <= END:
            daily[day] = daily.get(day, 0) + int(count)


# Primeiro dia da semana (segunda-feira)
first_day = START - timedelta(days=START.weekday())

# Lista dos meses no intervalo
months = []
current_month = START.replace(day=1)

while current_month <= END:
    months.append(current_month)
    if current_month.month == 12:
        current_month = date(current_month.year + 1, 1, 1)
    else:
        current_month = date(
            current_month.year,
            current_month.month + 1,
            1
        )


# Calcula os índices das semanas de cada mês
month_positions = {}

for month in months:
    month_start = max(month, START)
    month_end = min(
        date(month.year, month.month,
             calendar.monthrange(month.year, month.month)[1]),
        END
    )

    first_week = (month_start - first_day).days // 7
    last_week = (month_end - first_day).days // 7

    month_positions[month.month, month.year] = (
        first_week,
        last_week
    )


# Posição horizontal com espaçamento entre meses
def x_position(day: date) -> int:
    week = (day - first_day).days // 7

    month_index = next(
        i for i, month in enumerate(months)
        if month.year == day.year and month.month == day.month
    )

    return PAD + week * STEP + month_index * MONTH_GAP


cells = []

current = START

while current <= END:
    x = x_position(current)
    y = PAD + current.weekday() * STEP

    count = daily.get(current, 0)
    label = "submissão" if count == 1 else "submissões"

    cells.append(
        f'<rect x="{x}" y="{y}" '
        f'width="{CELL}" height="{CELL}" rx="2" '
        f'fill="{color_for(count)}">'
        f'<title>{current}: {count} {label}</title>'
        f'</rect>'
    )

    current += timedelta(days=1)


# Labels dos meses
month_labels = []

for month in months:
    month_start = max(month, START)

    if month.month == 12:
        next_month = date(month.year + 1, 1, 1)
    else:
        next_month = date(month.year, month.month + 1, 1)

    month_end = min(next_month - timedelta(days=1), END)

    first_x = x_position(month_start)
    last_x = x_position(month_end)

    center = (first_x + last_x + CELL) / 2

    month_name = calendar.month_abbr[month.month].upper()

    month_labels.append(
        f'<text x="{center}" y="{PAD + 7 * STEP + 14}" '
        f'text-anchor="middle" '
        f'font-family="Arial, sans-serif" '
        f'font-size="{FONT_SIZE}" '
        f'fill="{TEXT_COLOR}">{month_name}</text>'
    )


# Dimensões
last_x = x_position(END)

width = last_x + CELL + PAD
height = PAD * 2 + 7 * STEP + 24

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{width}" height="{height}" '
    f'viewBox="0 0 {width} {height}">'
    f'<rect width="100%" height="100%" '
    f'fill="{BACKGROUND}" rx="6"/>'
    f'{"".join(cells)}'
    f'{"".join(month_labels)}'
    f'</svg>'
)

assets_dir = Path(__file__).resolve().parent.parent / "assets"
assets_dir.mkdir(exist_ok=True)

(assets_dir / "leetcode-graph.svg").write_text(
    svg, encoding="utf-8"
)

print(f"Gráfico atualizado! {START} até {END}")
