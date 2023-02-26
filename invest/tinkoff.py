from typing import List

from tinkoff.invest import Account, Client


def get_subaccounts(token: str) -> List[Account]:
    with Client(token) as client:
        accounts = client.users.get_accounts()
    return accounts.accounts
