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
today_str = today.strftime("%Y-%m-%d")

cal = calendar.Calendar(firstweekday=0)  # Monday start


def ym(y, m):
    return f"{y}-{m:02d}"


def prev_next(y, m):
    prev_y, prev_m = (y - 1, 12) if m == 1 else (y, m - 1)
    next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)
    return prev_y, prev_m, next_y, next_m


# ----------------------
# 1️⃣ history md 생성
# ----------------------
history_file = HISTORY_DIR / f"{ym(year, month)}.md"

if not history_file.exists():
    py, pm, ny, nm = prev_next(year, month)

    history_file.write_text(
        f"""# 📆 {year}년 {month}월
⬅ [{py}.{pm:02d}]({ym(py, pm)}.md) | [{ny}.{nm:02d}]({ym(ny, nm)}.md) ➡

## {today_str}
- 
""",
        encoding="utf-8"
    )

# ----------------------
# 2️⃣ README 달력 생성
# ----------------------
py, pm, ny, nm = prev_next(year, month)

lines = []
lines.append("# 📚 Daily Engineering Calendar")
lines.append("> One commit a day, one step closer.\n")
lines.append("---\n")
lines.append("## 🗓 Current Month")
lines.append(f"### 📆 {year}년 {month}월")
lines.append(
    f"⬅ [{py}.{pm:02d}](history/{ym(py, pm)}.md) | "
    f"[{ny}.{nm:02d}](history/{ym(ny, nm)}.md) ➡\n"
)

lines.append("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
lines.append("|-----|-----|-----|-----|-----|-----|-----|")

for week in cal.monthdayscalendar(year, month):
    row = []
    for day in week:
        if day == 0:
            row.append(" ")
        else:
            date_anchor = f"{year}-{month:02d}-{day:02d}"
            link = f"[{day}](history/{ym(year, month)}.md#{date_anchor})"
            if date_anchor == today_str:
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

print("✅ Calendar & README generated")
