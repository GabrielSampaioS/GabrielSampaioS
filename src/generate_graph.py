
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from leetcode_api import get_calendar

USERNAME = "gabrielsampaios"
YEAR = datetime.now().year 

calendar = get_calendar(USERNAME, YEAR)

# Converte timestamps Unix em datas
daily = {}

for timestamp, count in calendar.items():
    day = datetime.fromtimestamp(
        int(timestamp), timezone.utc
    ).date()

    daily[day] = int(count)

# Organiza os dias do ano em semanas
start = date(YEAR, 1, 1)
end = date(YEAR, 12, 31)

# Completa a primeira semana
first_day = start - timedelta(days=start.weekday())

cells = []

current = first_day

while current <= end:
    count = daily.get(current, 0)

    color = (
        "#161b22" if count == 0 else
        "#0e4429" if count <= 1 else
        "#006d32" if count <= 2 else
        "#26a641" if count <= 5 else
        "#39d353"
    )

    x = ((current - first_day).days // 7) * 13
    y = current.weekday() * 13

    if start <= current <= end:
        cells.append(
            f'<rect x="{x}" y="{y}" width="10" '
            f'height="10" rx="2" fill="{color}">'
            f'<title>{current}: {count} submissões</title>'
            f'</rect>'
        )

    current += timedelta(days=1)

columns = ((end - first_day).days // 7) + 1
width = columns * 13

svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}" height="100">
    <rect width="100%" height="100%" fill="#0d1117" rx="6"/>
    {''.join(cells)}
</svg>
"""

Path("../assets").mkdir(exist_ok=True)
Path("../assets/leetcode-graph.svg").write_text(
    svg, encoding="utf-8"
)

print("Gráfico atualizado!")
