# Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

from bank import Bank
from constant import INITIAL_AVAILABLE_AMOUNT, Account, Transaction, Status


class ATM:
    def __init__(self):
        # self.id = id
        # self.coordinates = coordinates  # (latitude, longitude)
        self.bank = Bank()
        self.availableAmount = INITIAL_AVAILABLE_AMOUNT
        self.card = None
        self.selectedAccount = None
        self.isAuthenticated = False

    def insertCard(self, cardNumber: str) -> bool:
        if self.bank.validateCard(cardNumber):
            self.card = cardNumber
            return True
        self.card = None
        return False

    def insertPin(self, pinNumber: str) -> bool:
        if self.bank.validatePin(self.card, pinNumber):
            self.isAuthenticated = True
            return True
        self.isAuthenticated = False
        return False

    def showAccounts(self) -> dict:
        if self.isAuthenticated:
            return self.bank.getAccounts(self.card)
        return None

    def selectAccount(self, account: Account) -> bool:
        if self.isAuthenticated and self.bank.validateAccount(self.card, account):
            self.selectedAccount = account
            return True
        self.selectedAccount = None
        return False

    def executeTransaction(self, transaction: Transaction, inputAmount: int) -> dict:

        params = {
            'cardNumber': self.card,
            'account': self.selectedAccount,
            'inputAmount': inputAmount,
            'transaction': transaction,
            'availableAmount': self.availableAmount,
            'balance': None,
            'status': None,
            'message': None,
        }
        if (not self.isAuthenticated) and (transaction not in Transaction):
            params['message'] = 'Invalid transaction type or card is not authenticated'
            params['status'] = Status['ERROR']
        else:
            tempParams = self.bank.transaction(params)
            self.availableAmount = tempParams["availableAmount"]
        return params
