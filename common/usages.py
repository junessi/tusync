def printUpdateUsage():
    print("Usages:")
    print("tusync update")
    print("  - same as 'update today'")
    print("tusync update [full|today|-N]")
    print("  - full: update all stocks in all exchanges in the whole history.")
    print("  - today: update all stocks in all exchanges today.")
    print("  - -N: update all stocks in all exchanges in the last N days, today is included.")
    print("tusync update [start date]")
    print("  - update all stocks in all exchanges from given date.")
    print("tusync update [start date] [end date]")
    print("  - update all stocks in all exchanges in a date range.")
    print("tusync update [stock code]")
    print("  - update stock from last updated date.")
    print("tusync update [stock code] [year]")
    print("  - update stock in specified year.")
    print("tusync update [stock code] [start date]")
    print("  - update stock from start date to today.")
    print("tusync update [stock code] [start date] [end date]")
    print("  - update stock in a date range.")
    print("tusync update [exchange] [start date]")
    print("  - update all stocks in specified exchange from start date to today.")
    print("tusync update [exchange] [start date] [end date]")
    print("  - update all stocks in specified exchange in a date range.")

def printFetchUsage():
    print("tusync fetch [exchange]")
    print("  - fetch latest stock list of exchagne.")

def printCommands():
    print("tusync [update|fetch]")

def printHelp():
    printCommands()
    printUpdateUsage()
    printFetchUsage()
