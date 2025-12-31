import calendar
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
HISTORY_DIR = BASE_DIR / "history"
README_PATH = BASE_DIR / "README.md"

HISTORY_DIR.mkdir(exist_ok=True)

today = datetime.today()
year = today.year
month = today.month
day = today.day

today_str = today.strftime("%Y-%m-%d")

# 📁 날짜별 디렉토리
YEAR_DIR = BASE_DIR / str(year)
MONTH_DIR = YEAR_DIR / f"{month:02d}"
DAY_FILE = MONTH_DIR / f"{today_str}.md"

cal = calendar.Calendar(firstweekday=0)  # Monday start


def ym(y, m):
    return f"{y}-{m:02d}"


def prev_next(y, m):
    prev_y, prev_m = (y - 1, 12) if m == 1 else (y, m - 1)
    next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)
    return prev_y, prev_m, next_y, next_m


# ----------------------
# 0️⃣ 년 / 월 / 일 디렉토리 & md 생성
# ----------------------
MONTH_DIR.mkdir(parents=True, exist_ok=True)

if not DAY_FILE.exists():
    DAY_FILE.write_text(
        f"""# 📅 {today_str}

## 🛠 프로그래밍 ( 알고리즘 )
- 

## 📘 실습
- 

## 📝 이론
- 
""",
        encoding="utf-8"
    )


# ----------------------
# 1️⃣ history md 생성 (월 네비게이션)
# ----------------------
history_file = HISTORY_DIR / f"{ym(year, month)}.md"

if not history_file.exists():
    py, pm, ny, nm = prev_next(year, month)

    history_file.write_text(
        f"""# 📆 {year}년 {month}월

<p align="center">
<a href="./{ym(py, pm)}.md">⬅ {py}.{pm:02d}</a>
&nbsp;|&nbsp;
<a href="./{ym(ny, nm)}.md">{ny}.{nm:02d} ➡</a>
</p>
""",
        encoding="utf-8"
    )


# ----------------------
# 2️⃣ README 달력 생성 (날짜별 md 링크)
# ----------------------
py, pm, ny, nm = prev_next(year, month)

lines = []
lines.append("# 📚 Daily Engineering Calendar")
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

lines.append("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
lines.append("|----|----|----|----|----|----|----|")

for week in cal.monthdayscalendar(year, month):
    row = []
    for d in week:
        if d == 0:
            row.append(" ")
        else:
            date_str = f"{year}-{month:02d}-{d:02d}"
            link = f"[{d}]({year}/{month:02d}/{date_str}.md)"
            if date_str == today_str:
                row.append(f"**{link} 🔥**")
            else:
                row.append(link)
    lines.append("| " + " | ".join(row) + " |")


# ----------------------
# 3️⃣ History 링크
# ----------------------
lines.append("\n---\n")
lines.append("## 🗂 History")

for m in range(1, 13):
    lines.append(f"- 👉 [{year}년 {m}월](history/{ym(year, m)}.md)")

README_PATH.write_text("\n".join(lines), encoding="utf-8")

print("✅ Calendar, README, Year/Month/Day structure generated")
