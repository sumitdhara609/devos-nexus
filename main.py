from rich import print
from rich.panel import Panel
from rich.table import Table

from storage import add_entry, get_entries
from analysis import show_stats


def show_menu():
    print(Panel.fit("⚡ [bold cyan]DevOS Dashboard[/bold cyan] ⚡"))
    print("[1] 📝 Log Coding Session")
    print("[2] 📂 View Logs")
    print("[3] 📊 Show Insights")
    print("[4] ❌ Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_entry()

        elif choice == "2":
            entries = get_entries()

            if not entries:
                print("[red]No logs found.[/red]")
            else:
                table = Table(title="📂 Your Logs")

                table.add_column("No.", style="cyan")
                table.add_column("Details", style="magenta")

                for i, e in enumerate(entries, 1):
                    table.add_row(str(i), e)

                print(table)

        elif choice == "3":
            show_stats()

        elif choice == "4":
            print("[bold green]🚀 Keep improving daily![/bold green]")
            break

        else:
            print("[red]Invalid choice![/red]")


if __name__ == "__main__":
    main()