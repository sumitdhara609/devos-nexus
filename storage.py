from datetime import datetime

DATA_FILE = "data.txt"

def add_entry():
    problem = input("Problem name: ").strip()
    difficulty = input("Difficulty (Easy/Medium/Hard): ").strip().capitalize()
    
    # 🔥 FIX: Ensure valid time input
    while True:
        time_taken = input("Time taken (minutes): ").strip()
        if time_taken.isdigit():
            break
        else:
            print("⚠️ Please enter a valid number.")

    status = input("Status (Solved/Unsolved): ").strip().capitalize()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    hour = now.hour

    with open(DATA_FILE, "a") as f:
        f.write(f"{problem},{difficulty},{time_taken},{status},{date},{hour}\n")

    print("✅ Entry added successfully!")

def get_entries():
    try:
        with open(DATA_FILE, "r") as f:
            entries = [line.strip() for line in f if line.strip()]
            
            # 🔥 Optional: Make output cleaner
            formatted = []
            for e in entries:
                parts = e.split(",")
                if len(parts) == 6:
                    name, diff, time, status, date, hour = parts
                    formatted.append(f"{name} | {diff} | {time} min | {status} | {date}")
                else:
                    formatted.append(e)

            return formatted

    except FileNotFoundError:
        return []