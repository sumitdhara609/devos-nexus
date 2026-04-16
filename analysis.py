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
                total_time += int(time_taken)

                # Difficulty count
                if difficulty == "Easy":
                    easy += 1
                elif difficulty == "Medium":
                    medium += 1
                elif difficulty == "Hard":
                    hard += 1

                # 🔥 Time logic
                hour = int(hour)

                if 5 <= hour < 12:
                    time_slots["Morning"] += 1
                elif 12 <= hour < 17:
                    time_slots["Afternoon"] += 1
                elif 17 <= hour < 21:
                    time_slots["Evening"] += 1
                else:
                    time_slots["Night"] += 1

        # 📊 Stats
        print("\n📊 DevOS Insights")
        print("-"*40)
        print(f"Total Solved: {total}")
        print(f"Easy: {easy}, Medium: {medium}, Hard: {hard}")

        if total > 0:
            avg_time = total_time / total
            print(f"⏱ Avg Time per Problem: {avg_time:.2f} minutes")

            if avg_time > 30:
                print("⚠️ You are taking too long.")
            else:
                print("🔥 Good speed!")

        # 🧠 Performance Insights
        print("\n🧠 Performance Insights")
        print("-"*40)

        if medium > easy:
            print("⚠️ You struggle with Medium problems.")

        if hard > easy:
            print("⚠️ Hard problems need more focus.")

        if total > 0:
            if total_time / total > 30:
                print("⏱ You are slower than average.")
            else:
                print("⚡ Your speed is good.")

        # ⏰ Time Intelligence
        print("\n⏰ Performance by Time")
        print("-"*40)

        if total > 0:
            best_time = max(time_slots, key=time_slots.get)
            print(f"🔥 You perform best in: {best_time}")
        else:
            print("No data available.")

        # 🎯 Smart Recommendation System (CORRECT PLACE)
        print("\n🎯 Recommendations")
        print("-"*40)

        if total == 0:
            print("Start solving problems to get insights.")
        else:
            difficulty_map = {
                "Easy": easy,
                "Medium": medium,
                "Hard": hard
            }

            weakest = min(difficulty_map, key=difficulty_map.get)
            strongest = max(difficulty_map, key=difficulty_map.get)

            print(f"📌 Strongest Area: {strongest}")
            print(f"⚠️ Weakest Area: {weakest}")

            if weakest == "Easy":
                print("👉 Build fundamentals. Practice more Easy problems.")
            elif weakest == "Medium":
                print("👉 Focus on Medium problems to improve problem-solving.")
            elif weakest == "Hard":
                print("👉 Challenge yourself with Hard problems regularly.")

    except Exception as e:
        print(f"Error: {e}")