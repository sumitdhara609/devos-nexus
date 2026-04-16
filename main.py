from storage import add_entry, get_entries
from analysis import show_stats

def show_menu():
    print("\n" + "="*40)
    print("        ⚡ DevOS Dashboard")
    print("="*40)
    print("1. Log Coding Session")
    print("2. View Logs")
    print("3. Show Insights")
    print("4. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            entries = get_entries()
            if not entries:
                print("No logs found.")
            else:
                for i, e in enumerate(entries, 1):
                    print(f"{i}. {e}")
        elif choice == "3":
            show_stats()
        elif choice == "4":
            print("🚀 Keep improving daily!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()