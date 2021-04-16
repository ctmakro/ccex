
from api import *

def shorter_hash(hash):
    return f'{hash[:4]}...{hash[-4:]}'

class cc_account:
    def __init__(self, pubkey, apikey):
        self.pk = pubkey
        self.ak = apikey

        print(f'trying to verify api_key {shorter_hash(self.ak)}')
        for i in range(3):
            if cc_verify_api_key(self.ak):
                print(f'api_key {shorter_hash(self.ak)} is valid')
                break
            else:
                print(f'api_key {shorter_hash(self.ak)} seems invalid')

        self.load_history()
        print(f'account {shorter_hash(self.pk)} ready ({len(self.incomings)} in {len(self.outgoings)} out)')
        
        self.calc_balance()
        print(f'balance is {self.balance}')

    def load_history(self):
        print(f'trying to load history from {shorter_hash(self.pk)}')
        incomings = cc_get_incomings(self.pk)
        outgoings = cc_get_outgoings(self.pk)
        print(f'account got {len(incomings)} incoming(s) and {len(outgoings)} outgoing(s)')

        self.incomings = incomings
        self.outgoings = outgoings

    def calc_balance(self):
        balance = 0
        for i in self.incomings:
            if 'amount_received' in i:
                balance+=i['amount_received']

        for i in self.outgoings:
            if 'amount_sent' in i:
                balance-=i['amount_sent']

        self.balance = balance

    def send(self, dest, amount, memo):
        print(f'trying to send {amount} to {dest} ({memo})...')
        res = cc_send(dest, amount, self.ak, memo)
        print(f'successfully sent.')
        return res

    # check if payment with a certain prefix in memo is sent
    def checksent(self, prefix):
        for i in self.outgoings:
            if 'memo' in i and i['memo'].startswith(prefix):
                return i
        return False

    # check if payment with a certain prefix in memo is received
    def checkrecv(self, prefix):
        for i in self.incomings:
            if 'memo' in i and i['memo'].startswith(prefix):
                return i
        return False

if __name__ == '__main__':
    import time
    from creds import apikey, pubkey, myaddr, authoraddr

    cca = cc_account(pubkey, apikey)

    # result = cca.send(authoraddr, 1.0, 'experiment #1')
    # print(result)
    # time.sleep(1)
    print(cca.checksent('experiment #1'))
