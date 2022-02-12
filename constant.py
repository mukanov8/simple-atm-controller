# simple constant dictionaries for account, transaction, and status types, I assume there are only 2 types of bank accounts: checking and savings (https://www.forbes.com/advisor/banking/what-are-the-different-types-of-bank-accounts/)

Account = {
    'CHECKING': 'Checking',
    'SAVINGS': 'Savings',
}

Transaction = {
    'DEPOSIT': 'Deposit',
    'WITHDRAW': 'Withdraw',
    'BALANCE': 'Balance',
}

Status = {
    'ERROR': 'Error',
    'SUCCESS': 'Success',
}

INITIAL_AVAILABLE_AMOUNT = 30000
