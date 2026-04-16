from streak import update_streak
from datetime import datetime
from rich import print

DATA_FILE = "data.txt"


def add_entry():
    problem = input("Problem name: ").strip()

    # 🔥 Validate difficulty
    while True:
        difficulty = input("Difficulty (Easy/Medium/Hard): ").strip().capitalize()
        if difficulty in ["Easy", "Medium", "Hard"]:
            break
        else:
            print("[red]⚠️ Enter only Easy / Medium / Hard[/red]")

    # 🔥 Validate time
    while True:
        time_taken = input("Time taken (minutes): ").strip()
        if time_taken.isdigit():
            break
        else:
            print("[red]⚠️ Please enter a valid number.[/red]")

    # 🔥 Validate status
    while True:
        status = input("Status (Solved/Unsolved): ").strip().capitalize()
        if status in ["Solved", "Unsolved"]:
            break
        else:
            print("[red]⚠️ Enter only Solved / Unsolved[/red]")

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    hour = now.hour

    with open(DATA_FILE, "a") as f:
        f.write(f"{problem},{difficulty},{time_taken},{status},{date},{hour}\n")

    print("[green]✅ Entry added successfully![/green]")

    # 🔥 Update streak only if solved
    if status == "Solved":
        update_streak()


def get_entries():
    try:
        with open(DATA_FILE, "r") as f:
            entries = [line.strip() for line in f if line.strip()]

            formatted = []
            for e in entries:
                parts = e.split(",")

                if len(parts) == 6:
                    name, diff, time, status, date, hour = parts

                    formatted.append(
                        f"[cyan]{name}[/cyan] | "
                        f"[green]{diff}[/green] | "
                        f"[yellow]{time} min[/yellow] | "
                        f"[magenta]{status}[/magenta] | "
                        f"{date}"
                    )
                else:
                    formatted.append(e)

            return formatted

    except FileNotFoundError:
        return []