from rich import print
from rich.panel import Panel
from streak import get_streak  # 🔥 NEW

DATA_FILE = "data.txt"


def show_stats():
    total = 0
    easy = medium = hard = 0
    total_time = 0

    # 🔥 Time tracking
    time_slots = {
        "Morning": 0,
        "Afternoon": 0,
        "Evening": 0,
        "Night": 0
    }

    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")

                if len(parts) != 6:
                    continue

                _, difficulty, time_taken, status, _, hour = parts

                if status.lower() != "solved":
                    continue

                total += 1

                # 🛡️ Safe conversion
                try:
                    total_time += int(time_taken)
                    hour = int(hour)
                except:
                    continue

                # Difficulty count
                if difficulty == "Easy":
                    easy += 1
                elif difficulty == "Medium":
                    medium += 1
                elif difficulty == "Hard":
                    hard += 1

                # ⏰ Time logic
                if 5 <= hour < 12:
                    time_slots["Morning"] += 1
                elif 12 <= hour < 17:
                    time_slots["Afternoon"] += 1
                elif 17 <= hour < 21:
                    time_slots["Evening"] += 1
                else:
                    time_slots["Night"] += 1

        # 📊 Dashboard
        print(Panel.fit("📊 [bold green]DevOS Insights[/bold green]"))

        print(f"[bold yellow]Total Solved:[/bold yellow] {total}")
        print(f"[green]Easy:[/green] {easy}   [yellow]Medium:[/yellow] {medium}   [red]Hard:[/red] {hard}")

        # 🔥 Streak Display
        streak = get_streak()
        print(f"\n🔥 [bold red]Current Streak:[/bold red] {streak} days")

        # 🎯 Progress Bar
        if total > 0:
            goal = 100
            progress = int((total / goal) * 20)
            bar = "█" * progress + "-" * (20 - progress)
            print(f"\n🎯 Progress: [{bar}] {total}/100")

        # ⏱ Speed Analysis
        if total > 0:
            avg_time = total_time / total
            print(f"\n⏱ Avg Time: {avg_time:.2f} minutes")

            if avg_time > 45:
                print("[red]🚨 Too slow — improve efficiency[/red]")
            elif avg_time > 30:
                print("[yellow]⚠️ Slightly slow — work on speed[/yellow]")
            else:
                print("[green]🔥 Excellent speed![/green]")

        # 🧠 Performance Insights
        print("\n🧠 [bold]Performance Insights[/bold]")
        print("-" * 40)

        if medium > easy:
            print("[yellow]⚠️ You struggle with Medium problems[/yellow]")

        if hard > easy:
            print("[red]⚠️ Hard problems need more focus[/red]")

        if total > 0:
            if total_time / total > 30:
                print("[yellow]⏱ You are slower than average[/yellow]")
            else:
                print("[green]⚡ Your speed is good[/green]")

        # ⏰ Time Intelligence
        print("\n⏰ [bold]Performance by Time[/bold]")
        print("-" * 40)

        if total > 0:
            best_time = max(time_slots, key=time_slots.get)
            print(f"[cyan]🔥 You perform best in: {best_time}[/cyan]")
        else:
            print("No data available.")

        # 🎯 Smart Recommendations
        print("\n🎯 [bold]Smart Recommendations[/bold]")
        print("-" * 40)

        if total == 0:
            print("Start solving problems to get insights.")
        else:
            if easy > medium and easy > hard:
                print("👉 You are in comfort zone. Try Medium problems.")

            if medium >= easy:
                print("👉 Good progress. Start pushing Hard problems.")

            if hard > 0 and hard < medium:
                print("👉 Increase Hard problem practice.")

            if total_time / total > 35:
                print("👉 Optimize your solving approach.")

            if total >= 50:
                print("[green]🚀 Strong consistency![/green]")

        # 🔥 Consistency Check
        print("\n🔥 [bold]Consistency Check[/bold]")
        print("-" * 40)

        if total >= 1:
            print("You're building a strong habit.")
        if total >= 20:
            print("[green]💪 Great consistency![/green]")
        if total >= 50:
            print("[bold green]🏆 Elite discipline level![/bold green]")

    except FileNotFoundError:
        print("[red]No data file found.[/red]")
    except Exception as e:
        print(f"[red]Error: {e}[/red]")