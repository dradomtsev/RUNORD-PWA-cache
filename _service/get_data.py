import aiohttp
import asyncio
import json

# %%
async def get_response(session, url):
    async with session.get(url) as resp:
        json = await resp.json(content_type=None)
        return json
# %%
async def get_table_data(url, jar, cookies, headers):
    async with aiohttp.ClientSession(cookie_jar=jar, cookies=cookies, headers=headers) as session:
        count = await get_response(session, url)
        print("Number of records: " + count['odata.count'])
        top = len(count['value'])
        if top == 0:
            return None
        else:
            tasks = []
            for skip in range(0, int(count['odata.count']), top):
                urlC = f"{url}&$skip={skip}&$top={top}"
                tasks.append(asyncio.ensure_future(
                    get_response(session, urlC)))
            data = await asyncio.gather(*tasks)
            return data

# %%