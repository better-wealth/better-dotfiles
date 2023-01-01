"""Trending homebrew.

better-dotfiles/lib/trending-homebrew.sh
Requests current analytics data from Homebrew and calculates trends.
https://github.com/better-wealth/better-dotfiles
MIT License
2022 (C) John Patrick Roach
"""

import asyncio
from typing import AsyncGenerator
import aiohttp
from aiomultiprocess import Pool
import numpy as np

DATA_DAY_RANGES: list[str] = ["365", "90", "30"]

CATEGORIES: list[dict[str, str]] = [
    {
        "name": "install",
        "category_data_url": (
            "https://formulae.brew.sh/api/analytics/install/{days}d.json"
        ),
    },
    {
        "name": "install_on_request",
        "category_data_url": (
            "https://formulae.brew.sh/api/analytics/install-on-request/"
            "{days}d.json"
        ),
    },
    {
        "name": "cask_install",
        "category_data_url": (
            "https://formulae.brew.sh/api/analytics/cask-install/{days}d.json"
        ),
    },
    {
        "name": "BuildError",
        "category_data_url": (
            "https://formulae.brew.sh/api/analytics/build-error/{days}d.json"
        ),
    },
]

HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) "
        "Gecko/20100101 Firefox/108.0"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
        "image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://brew.sh/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-User": "?1",
    "If-Modified-Since": "Sat, 31 Dec 2022 00:00:00 GMT",
    "If-None-Match": 'W/"63b09975-27bc"',
}


class Category:
    """Category class."""

    data_day_ranges: list[str] = DATA_DAY_RANGES

    def __init__(self, name: str, category_data_url: str) -> None:
        """Construct the instance."""
        self.name: str = name
        self.data_coverage = 0
        self.category_data_url: str = category_data_url
        self.data: dict = {}
        self.total_counts: dict = {}
        self.items: dict = {}

    async def request_category_data(self) -> AsyncGenerator:
        """Request data for a category and date range from Homebrew."""
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            for data_day_range in self.data_day_ranges:
                async with session.get(
                    self.category_data_url.format(days=data_day_range),
                    headers=HEADERS,
                ) as req:
                    json_body: dict = await req.json()
                    yield data_day_range, json_body

    async def get_windows(self) -> AsyncGenerator:
        """Create an async generator for windows."""
        for window in [
            [i, j]
            for i, j in zip(self.data_day_ranges[:-1], self.data_day_ranges[1:])
        ]:
            yield window

    async def set_windows(self) -> None:
        """Set the window data."""
        async for window in self.get_windows():
            self.total_counts[f"{window[0]}_to_{window[1]}"] = (
                self.total_counts[window[0]] - self.total_counts[window[1]]
            )

    async def get_percents(self) -> AsyncGenerator:
        """Create an async generator for percents."""
        for data_day_range, total_count in self.total_counts.items():

    async def set_percents(self) -> None:
        """Set items percents of total counts."""
        pass

    async def set_category_data(self) -> None:
        """Set the category data."""
        async for data_day_range, json_body in self.request_category_data():
            self.data[data_day_range] = json_body

    async def get_total_counts(self) -> AsyncGenerator:
        """Create an async generator for total counts."""
        for data_day_range in self.data_day_ranges:
            yield data_day_range, self.data[data_day_range]["total_count"]

    async def set_total_counts(self) -> None:
        """Set the total counts."""
        async for data_day_range, total in self.get_total_counts():
            self.total_counts[data_day_range] = total
            self.data_coverage += 1
            if self.data_coverage == len(self.data_day_ranges):
                await self.set_windows()

    async def get_items_by_date_range(self) -> AsyncGenerator:
        """Create an async generator for items by date range."""
        for data_day_range in self.data_day_ranges:
            yield data_day_range, self.data[data_day_range]["items"]

    async def get_items(self) -> AsyncGenerator:
        """Create an async generator for items."""
        async for data_day_range, items in self.get_items_by_date_range():
            for item in items:
                yield data_day_range, item

    async def set_items(self) -> None:
        """Set the item values."""
        async for data_day_range, item in self.get_items():
            item_instance: Item = self.items.setdefault(
                item.get("formula", item.get("cask")),
                Item(item.get("formula", item.get("cask"))),
            )
            item_instance.counts[data_day_range] = int(
                item["count"].replace(",", "")
            )
            item_instance.data_coverage += 1
            if item_instance.data_coverage == len(self.data_day_ranges):
                await item_instance.set_windows()



class Item:
    """Item class."""

    data_day_ranges: list[str] = DATA_DAY_RANGES

    def __init__(self, item_name: str) -> None:
        """Construct the Item instance."""
        self.item_name: str = item_name
        self.data_coverage: int = 0
        self.counts: dict = {}
        self.percents: dict = {}
        self.trend: int = 0

    async def get_windows(self) -> AsyncGenerator:
        """Create an async generator for windows."""
        for window in [
            [i, j]
            for i, j in zip(self.data_day_ranges[:-1], self.data_day_ranges[1:])
        ]:
            yield window

    async def set_windows(self) -> None:
        """Set the window data."""
        async for window in self.get_windows():
            self.counts[f"{window[0]}_to_{window[1]}"] = (
                self.counts[window[0]] - self.counts[window[1]]
            )

    async def set_trend(self) -> None:
        """Set item trend value."""
        percs = [
            self.percents["365_to_90"],
            self.percents["90_to_30"],
            self.percents["30"],
        ]
        if percs[0] == 0:
            percs = percs[1:]
        windows = range(len(percs))
        self.trend = np.polyfit(windows, percs, 1)[0]


async def get_category(category: dict) -> Category:
    """Get category."""
    category_instance: Category = Category(
        category["name"], category["category_data_url"]
    )
    await category_instance.set_category_data()
    await category_instance.set_total_counts()
    await category_instance.set_items()
    return category_instance


# for formula, values in formulae.items():
#    formulae[formula]["percent_90_to_365"] = formulae[formula]["count_90_to_365"] / total_90_to_365
#    formulae[formula]["percent_30_to_90"] = formulae[formula]["count_30_to_90"] / total_30_to_90
#    formulae[formula]["percent_30"] = values["count_30"] / total_30


# formulae = sorted(formulae.items(), key=lambda item: item[1]["trend"], reverse=True)

# top_10 = formulae[0:10]
# bottom_10 = formulae[-10:]

# print("TOP 10:")
# for t in top_10:
#    print("\n")
#    print(t)
#    print("\n")

# print("BOTTOM 10:")
# for b in bottom_10:
#    print("\n")
#    print(b)
#    print("\n")


async def main() -> None:
    """Execute the main code."""
    async with Pool() as pool:
        async for category in pool.map(get_category, CATEGORIES):
            print("\n")
            print(category.name)
            print(category.total_counts)
            print("\n")
            try:
                print(category.items.get("xz").counts)
            except Exception as err:
                print("Skipping")
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())
