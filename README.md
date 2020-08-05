# Notes

There are simulation accounts and other accounts. I don't think I have anything setup with a real account yet.

The simulation accounts expire after 20 days. Go to https://www.developer.saxo/accounts/sim/signup to create a new one.

You can get a 24 hour token here: https://www.developer.saxo/openapi/token put it in .cred/saxo/saxo_token.txt ... I do this probably to make the example notebooks usable.

Go here to try things out:

https://www.developer.saxo/openapi/explorer#/


You can get the account info from the instantiated client ... see `helper.account_info`


# Examples

The following worked.

https://saxo-openapi.readthedocs.io/en/latest/examples/stream_proc.html#subscriptions-using-saxo-openapi

python stream_example.py ctxt_20190311
python price_subscr.py ctxt_20190311 EURJPY EURGBP
