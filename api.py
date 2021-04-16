'''
you use the API via fetch("https://centralized-coin.com//api/users/send", {
  "method": "POST",
   headers: {
     "Content-Type": "application/json"
     },
  "body": "{\"recipient_email\":\"hi@flurly.com\",\"force\":false,\"amount\":\"5\",\"memo\":\"\",\"token\":\"YOUR_TOKEN_HERE\"}",
}).then(x => {
  console.log(x);
});
'''

class ParamException(Exception):
    pass

import requests as r

def raiseif(j):
    if 'error' in j:
        raise ParamException(str(j['error']))

def cc_send(dest, amount, token, memo=''):
    res = r.post(
        'https://centralized-coin.com/api/users/send',
        json = {
            'recipient_email':dest,
            'force':False,
            'amount':str(amount),
            'memo':memo,
            'token':token,
        }
    )
    rj = res.json()
    raiseif(rj)
    return rj

# check if apikey is valid
def cc_verify_api_key(token):
    try:
        cc_send('',0,token)
    except ParamException as e:
        if 'try again later' in str(e):
            # print('api key invalid')
            pass
        else:
            # print('api key valid')
            return True
    return False

def cc_get_incomings(pubkey):
    res = r.get(f'https://www.centralized-coin.com/api/incoming/{pubkey}')
    rj = res.json()
    raiseif(rj)
    return rj['transactions']

def cc_get_outgoings(pubkey):
    res = r.get(f'https://www.centralized-coin.com/api/outgoing/{pubkey}')
    rj = res.json()
    raiseif(rj)
    return rj['transactions']

if __name__ == '__main__':
    # as a test

    from creds import apikey, pubkey, myaddr, authoraddr
    # result = cc_send(myaddr, 1.0, apikey, 'test cc_send()')
    # result = cc_send(authoraddr, "1.0000000000000005", apikey, 'test cc_send()')
    # print(result)

    print(cc_verify_api_key('asdf'))
    print(cc_verify_api_key(apikey))

    incomings = cc_get_incomings(pubkey)
    print(incomings)

    incomings = cc_get_outgoings(pubkey)
    print(incomings)
