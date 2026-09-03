from rich.console import Console
from rich.table import Table

def cmd_list(db: Database):
    symbols = db.list_symbols()
    if not symbols:
        print("No symbols stored. Run: python main.py fetch <TICKER>")
        return
    table = Table(title="Stored Symbols")
    table.add_column("Ticker", style="cyan")
    table.add_column("Bars")
    table.add_column("From")
    table.add_column("To")
    for s in symbols:
        table.add_row(s["ticker"], str(s["bar_count"]), s["from_date"], s["to_date"])
    Console().print(table)
        p_list = sub.add_parser("list")

    args = parser.parse_args()
    db = Database()

    if args.command == "fetch":
        cmd_fetch(args, db)
    elif args.command == "list":
        cmd_list(db)
    else:
        parser.print_help()
