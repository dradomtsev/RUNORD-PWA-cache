import logging
import azure.functions as func
import asyncio
import aiohttp
from . import pwa_cookie_auth
from . import get_table_data
import time
import os

# %%
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    cookiespwa = pwa_cookie_auth()
    # binary_security_token = get_pwa_bin_sec_token()
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     # Get cookies for pwa auth
    #     cookies_future = executor.submit(
    #         get_pwa_auth_cookies, binary_secrurity_token)
    #     cookiespwa = cookies_future.result()
    headers = {'Accept': 'application/json; odata=nometadata'}
    jar = aiohttp.CookieJar(quote_cookie=False)
    cookies = {'rtFa': cookiespwa[0], 'FedAuth': cookiespwa[1]}

    start_time = time.time()
    url = f"https://"+os.environ["PWA_DOMAIN_NAME"]+"/sites/"+os.environ["PWA_SITE_NAME"]+"/_api/ProjectData/[en-US]/Projects?$inlinecount=allpages"
    data = asyncio.run(get_table_data(url, jar, cookies, headers), debug=False)

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
