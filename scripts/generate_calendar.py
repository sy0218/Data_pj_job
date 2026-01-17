import calendar
from datetime import datetime
from pathlib import Path

# ----------------------
# 기본 경로 설정
# ----------------------
BASE_DIR = Path(__file__).resolve().parents[1]
HISTORY_DIR = BASE_DIR / "history"
README_PATH = BASE_DIR / "README.md"

HISTORY_DIR.mkdir(exist_ok=True)

today = datetime.today()
year, month, day = today.year, today.month, today.day
today_str = today.strftime("%Y-%m-%d")

# 날짜별 경로
YEAR_DIR = BASE_DIR / str(year)
MONTH_DIR = YEAR_DIR / f"{month:02d}"
DAY_FILE = MONTH_DIR / f"{today_str}.md"

# ----------------------
# 유틸 함수
# ----------------------
def ym(y, m):
    return f"{y}-{m:02d}"

def prev_next(y, m):
    prev_y, prev_m = (y - 1, 12) if m == 1 else (y, m - 1)
    next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)
    return prev_y, prev_m, next_y, next_m

def render_month_calendar(year, month, today_str=None, base_path=""):
    cal = calendar.Calendar(firstweekday=0)
    prefix = f"{base_path}/" if base_path else ""

    lines = []
    lines.append("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
    lines.append("|----|----|----|----|----|----|----|")

    for week in cal.monthdayscalendar(year, month):
        row = []
        for d in week:
            if d == 0:
                row.append(" ")
            else:
                date_str = f"{year}-{month:02d}-{d:02d}"
                link = f"[{d}]({prefix}{year}/{month:02d}/{date_str}.md)"
                if today_str and date_str == today_str:
                    row.append(f"**{link} 🔥**")
                else:
                    row.append(link)
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)

# ----------------------
# 0️⃣ 연/월 디렉토리 & 일별 md 생성
# ----------------------
MONTH_DIR.mkdir(parents=True, exist_ok=True)

if not DAY_FILE.exists():
    DAY_FILE.write_text(
        f"""# 📅 {today_str}

## 🛠 프로그래밍 (알고리즘)
- 

## 📘 실습
- 

## 📝 이론
- 
""",
        encoding="utf-8"
    )

# ----------------------
# 1️⃣ history/YYYY-MM.md 생성 (상대경로 달력)
# ----------------------
history_file = HISTORY_DIR / f"{ym(year, month)}.md"

py, pm, ny, nm = prev_next(year, month)
calendar_md = render_month_calendar(year, month, base_path="..")

history_file.write_text(
    f"""# 📆 {year}년 {month}월

<p align="center">
<a href="./{ym(py, pm)}.md">⬅ {py}.{pm:02d}</a>
&nbsp;|&nbsp;
<a href="./{ym(ny, nm)}.md">{ny}.{nm:02d} ➡</a>
</p>

{calendar_md}
""",
    encoding="utf-8"
)

# ----------------------
# 2️⃣ README.md 생성 (절대 기준 달력 + 🔥)
# ----------------------
lines = []
lines.append("# 📚 하루 한 줄 개발 기록")
lines.append("> One commit a day, one step closer.\n")
lines.append("---\n")
lines.append("## 🗓 Current Month")
lines.append(f"### 📆 {year}년 {month}월\n")

lines.append(
    f'<p align="center">'
    f'<a href="history/{ym(py, pm)}.md">⬅ {py}.{pm:02d}</a>'
    f' &nbsp;|&nbsp; '
    f'<a href="history/{ym(ny, nm)}.md">{ny}.{nm:02d} ➡</a>'
    f'</p>\n'
)

lines.append(render_month_calendar(year, month, today_str))

README_PATH.write_text("\n".join(lines), encoding="utf-8")

print("✅ README, history, Year/Month/Day 구조 생성 완료")
