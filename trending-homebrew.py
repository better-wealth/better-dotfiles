import asyncio
import aiohttp
import numpy as np
from aiomultiprocess import Pool

# CONSTANTS

# CATEGORIES
CATEGORIES = [
    {"category": "install", "category_data_url": "https://formulae.brew.sh/api/analytics/install/{days}d.json"},
    {"category": "install_on_request", "category_data_url": "https://formulae.brew.sh/api/analytics/install-on-request/{days}d.json"},
    {"category": "cask_install", "category_data_url": "https://formulae.brew.sh/api/analytics/cask-install/{days}d.json"},
    {"category": "BuildError", "category_data_url": "https://formulae.brew.sh/api/analytics/build-error/{days}d.json"}
]

# HEADERS
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
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
    "If-None-Match": "W/\"63b09975-27bc\""
}


# CATEGORY BASE CLASS
class Category:
    def __init__(self, category: str, category_data_url: str):
        self.category = category
        self.category_data_url = category_data_url
        self.data_day_ranges = ["30", "90", "365"]
        self.data = {}
        self.total_counts = {}
        self.items = {}

    async def request_category_data(self) -> (str, dict):
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            for data_day_range in self.data_day_ranges:
                async with session.get(self.category_data_url.format(days=data_day_range), headers=HEADERS) as req:
                    json_body = await req.json()
                    yield data_day_range, json_body
    
    async def set_category_data(self) ->  dict:
        async for data_day_range, json_body in self.request_category_data():
            self.data[data_day_range] = json_body

    async def get_total_counts(self) -> (str, int):
        for data_day_range in self.data_day_ranges:
            yield data_day_range, self.data[data_day_range]["total_count"]    

    async def set_total_counts(self):
        async for data_day_range, total in self.get_total_counts():
            self.total_counts[data_day_range] = total
        self.total_counts["365_to_90"] = self.total_counts["365"] - self.total_counts["90"]
        self.total_counts["90_to_30"] = self.total_counts["90"] - self.total_counts["30"]
    
    async def get_items_by_date_range(self):
        for data_day_range in self.data_day_ranges:
            yield data_day_range, self.data[data_day_range]["items"]

    async def get_items(self):
        async for data_day_range, items in self.get_items_by_date_range():
            for item in items:
                yield data_day_range, item

    async def set_items(self):
        async for data_day_range, item in self.get_items():
            item = Item(item.get("forumla", item.get("cask")))



# ITEM BASE CLASS
class Item:
    def __init__(self, item_name: str):
        self.item_name = item_name
        self.counts = {}
        self.percents = {}
        self.trend = 0
    
    async def get_counts(self):
        self.counts["365_to_90"] = self.counts["365"] - self.counts["90"]
        self.counts["90_to_30"] = self.counts["90"] - self.counts["30"]
    
    async def set_percents(self):
        self.counts["365_to_90"] = self.counts["365"] - self.counts["90"]
        self.counts["90_to_30"] = self.counts["90"] - self.counts["30"]


async def get_category(category: dict) -> Category:
    category = Category(category["category"], category["category_data_url"])
    await category.set_category_data()
    await category.set_total_counts()
    return category




# EX: {"name": [] }
#names_365 = [i["formula"] for i in formulae_365]
#names_90 = [i["formula"] for i in formulae_90]
#names_30 = [i["formula"] for i in formulae_30]
#formulae = {
#    i: DATA
#    for i in list(set(names_365 + names_90 + names_30))
#}


#for (a, b, c) in zip(formulae_365, formulae_90, formulae_30):
#    formulae[a["formula"]]["count_365"] = a["count"]
#    formulae[b["formula"]]["count_90"] = b["count"]
#    formulae[c["formula"]]["count_30"] = c["count"]

#for formula, values in formulae.items():
#    formulae[formula]["count_90_to_365"] = values["count_365"] - values["count_90"]
#    formulae[formula]["count_30_to_90"] = values["count_90"] - values["count_30"]
#    formulae[formula]["percent_90_to_365"] = formulae[formula]["count_90_to_365"] / total_90_to_365
#    formulae[formula]["percent_30_to_90"] = formulae[formula]["count_30_to_90"] / total_30_to_90
#    formulae[formula]["percent_30"] = values["count_30"] / total_30


#for formula, values in formulae.items():
#    y = [values["percent_90_to_365"], values["percent_30_to_90"], values["percent_30"]]
#    if y[0] == 0:
#        y = y[1:]
#    x = range(0, len(y))
#    formulae[formula]["trend"] = np.polyfit(x,y,1)[0]

#formulae = sorted(formulae.items(), key=lambda item: item[1]["trend"], reverse=True)

#top_10 = formulae[0:10]
#bottom_10 = formulae[-10:]

#print("TOP 10:")
#for t in top_10:
#    print("\n")
#    print(t)
#    print("\n")

#print("BOTTOM 10:")
#for b in bottom_10:
#    print("\n")
#    print(b)
#    print("\n")

async def main():
    async with Pool() as pool:
        async for category in pool.map(
            get_category, 
            CATEGORIES
        ):
            print(category.category, category.total_counts)

if __name__ == '__main__':
    asyncio.run(main())