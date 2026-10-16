from crews import InvestmentCrews
from rich.console import Console
from rich.markdown import Markdown

def main():
    # get input from user
    ticker = input("enter ticker: ")
    if len(ticker) == 0:
        print("please enter valid ticker")

    # create the console
    console = Console()

    # create crew
    crew = InvestmentCrews()
    result = crew.kickoff_research(ticker=ticker)
    console.print(result)

if __name__ == '__main__':
    main()