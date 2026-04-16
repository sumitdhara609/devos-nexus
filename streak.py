from datetime import datetime

STREAK_FILE = "streak.txt"


def update_streak():
    today = datetime.today().strftime("%Y-%m-%d")

    try:
        with open(STREAK_FILE, "r") as f:
            streak, last_date = f.read().split(",")

        streak = int(streak)

        if last_date == today:
            return  # already counted today

        last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
        today_obj = datetime.strptime(today, "%Y-%m-%d")

        diff = (today_obj - last_date_obj).days

        if diff == 1:
            streak += 1
        else:
            streak = 1

    except:
        streak = 1

    with open(STREAK_FILE, "w") as f:
        f.write(f"{streak},{today}")


def get_streak():
    try:
        with open(STREAK_FILE, "r") as f:
            streak, _ = f.read().split(",")
            return int(streak)
    except:
        return 0