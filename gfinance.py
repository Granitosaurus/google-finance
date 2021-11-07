from xml.dom import NotFoundErr
import asyncclick as click
import re
from aiohttp import ClientSession


async def scrape(exchange, symbol, session):
    """asynchronously scrape current price of EXCHANGE:SYMBOL pair from finance.google.com"""
    resp = await session.get(
        f"https://www.google.com/finance/quote/{symbol.upper()}:{exchange.upper()}"
    )
    try:
        return exchange, symbol, re.search('data-last-price="([\d\.]+)"', await resp.text()).groups()[0]
    except AttributeError:
        raise NotFoundErr(f"value for pair {exchange}:{symbol} not found")


@click.command()
@click.argument("exchange")
@click.argument("symbol")
async def run(exchange: str, symbol: str) -> str:
    """Scrape current exchange:symbol pair price"""
    async with ClientSession() as session:
        try:
            print((await scrape(exchange, symbol, session))[-1])
            exit(0)
        except NotFoundErr:
            print("nothing found")
            exit(1)


if __name__ == "__main__":
    run()
