from crews import InvestmentCrews

def main():
    # get input from user
    ticker = input("enter ticker: ")
    if len(ticker) == 0:
        print("please enter valid ticker")

    # create crew
    crew = InvestmentCrews()
    result = crew.kickoff_research(ticker=ticker)
    print(result)

if __name__ == '__main__':
    main()