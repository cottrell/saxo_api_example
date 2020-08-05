#!/usr/bin/env python
import json
import asyncio
import websockets
from saxo_openapi.contrib.ws import stream
import argh
import sys
from my.gym.saxo import get_token
import saxo_openapi.contrib.session as session
from saxo_openapi import API
from saxo_openapi.endpoints import chart, apirequest, decorators, portfolio, \
    referencedata, trading, valueadd, eventnotificationservices, rootservices, accounthistory


async def echo(ContextId, token):
    hdrs = {
        "Authorization": "Bearer {}".format(token),
    }
    URL = "wss://streaming.saxotrader.com/sim/openapi/streamingws/connect?" + \
          "contextId={ContextId}".format(ContextId=ContextId)
    async with websockets.connect(URL, extra_headers=hdrs) as websocket:
        async for message in websocket:
            print(stream.decode_ws_msg(message))

def read_sub(context_id):
    token = get_token()
    asyncio.get_event_loop().run_until_complete(echo(ContextId=context_id, token=token))

def create_price_sub(context_id, *instruments):
    """fetch instrument data by the name of the instrument and extract the Uic (Identifier)
    and use that to subscribe for prices.
    Use the name of the instrument as reference.
    """
    token = get_token()
    client = API(access_token=token)
    account_info = session.account_info(client=client)

    # body template for price subscription
    body = {
       "Arguments": {
           "Uic": "",
           "AssetType": "FxSpot"
       },
       "ContextId": "",
       "ReferenceId": ""
    }
    body['ContextId'] = context_id

    for instrument in instruments:
        params = {'AccountKey': account_info.AccountKey,
                  'AssetTypes': 'FxSpot',
                  'Keywords': instrument
                 }
        # create the request to fetch Instrument info
        req = referencedata.instruments.Instruments(params=params)
        rv = client.request(req)
        print(rv)
        rv = [x for x in rv['Data'] if x['Symbol'] == instrument]
        assert len(rv) == 1
        rv = rv[0]
        body['Arguments'].update({'Uic': rv['Identifier']})
        body.update({"ReferenceId": instrument})
        print(json.dumps(body, indent=2))
        # create the request to fetch Instrument info
        req = trading.prices.CreatePriceSubscription(data=body)
        client.request(req)
        status = "succesful" if req.status_code == req.expected_status else "failed"
        print(f"Subscription for instrument: {instrument} {status}")

def delete_price_sub(context_id, *, ref_id=None):
    token = get_token()
    client = API(access_token=token)
    if ref_id is None:
        # delete whole thing
        req = trading.prices.PriceSubscriptionRemoveByTag(context_id)
    else:
        req = trading.prices.PriceSubscriptionRemove(context_id, ref_id)
    client.request(req)
    status = "succesful" if req.status_code == req.expected_status else "failed"
    print(f"price sub delete: {context_id} {ref_id} {status}")

if __name__ == "__main__":
    argh.dispatch_commands([read_sub, create_price_sub, delete_price_sub])

