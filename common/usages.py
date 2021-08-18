def printUpdateUsage():
    print("update command must be used as one of the following:")
    print("tu.py update")
    print("  - same as 'update today'")
    print("tu.py update [full|today|-N]")
    print("  - full: update all stocks in all exchanges in the whole history.")
    print("  - today: update all stocks in all exchanges today.")
    print("  - -N: update all stocks in all exchanges in the last N days, today is included.")
    print("tu.py update [stock code]")
    print("  - update specified stock in its whole history.")
    print("tu.py update [stock code] [year]")
    print("  - update specified stock in specified year.")
    print("tu.py update [stock code] [start date]")
    print("  - update specified stock from specified date to today.")
    print("tu.py update [stock code] [start date] [end date]")
    print("  - update specified stock in specified date range.")
    print("tu.py update [start date] [end date]")
    print("  - update all stocks in all exchanges in specified date range.")


def printCommands():
    print("tu.py [update]")
