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
        
def cmd_stream(args, db: Database):
    from feed import Feed
    from signals import SignalGenerator
    from rich.console import Console

    console = Console()
    feed = Feed(db, args.ticker, speed=args.speed)
    gen = SignalGenerator()

    for bar in feed.stream():
        sig = gen.evaluate(bar)
        line = f"[grey]{bar['date']}[/]  C:{bar['close']:.2f}"
        if bar['rsi_14']:
            line += f"  SMA20:{bar['sma_20']:.2f}  RSI:{bar['rsi_14']:.1f}"
        if sig:
            line += f"  [bold yellow]► {sig['side']} — {sig['reason']}[/]"
        console.print(line)

def cmd_pipe(args, db: Database):
    from feed import Feed
    from signals import SignalGenerator
    from pipe import CppPipe

    feed = Feed(db, args.ticker, speed=args.speed)
    gen = SignalGenerator()
    cpp = CppPipe(args.binary)

    for bar in feed.stream():
        sig = gen.evaluate(bar)
        if sig:
            fill = cpp.send_signal(args.ticker.upper(), sig["side"], 100, sig["price"])
            print(f"→ sent {sig['side']} @ {sig['price']:.2f} | fill: {fill}")

    cpp.close()def cmd_pipe(args, db: Database):
    from feed import Feed
    from signals import SignalGenerator
    from pipe import CppPipe

    feed = Feed(db, args.ticker, speed=args.speed)
    gen = SignalGenerator()
    cpp = CppPipe(args.binary)

    for bar in feed.stream():
        sig = gen.evaluate(bar)
        if sig:
            fill = cpp.send_signal(args.ticker.upper(), sig["side"], 100, sig["price"])
            print(f"→ sent {sig['side']} @ {sig['price']:.2f} | fill: {fill}")

    cpp.close()
def cmd_fetch(args, db: Database):
    ticker = args.ticker.upper()
    print(f"Fetching {ticker} for period {args.period}...")
    try:
        bars = Fetcher(ticker).fetch(args.period)
    except ValueError as e:
        print(f"Error: {e}")
        return
    # ...rest unchanged