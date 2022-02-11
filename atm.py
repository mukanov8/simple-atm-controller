# Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

from bank import Bank
from constant import Account, Transaction, Status


class ATM:
    def __init__(self):
        # self.id = id
        # self.coordinates = coordinates  # (latitude, longitude)

        self.bank = Bank()
        self.availableAmount = 2000
        self.card = None
        self.accountType = None
        self.isAuthenticated = False

    def insertCard(self, cardNumber: str) -> bool:
        if self.bank.validateCard(cardNumber):
            self.card = cardNumber
            return True
        return False

    def insertPin(self, pinNumber: str) -> bool:
        if self.bank.validatePin(self.card, pinNumber):
            self.isAuthenticated = True
            return True
        self.isAuthenticated = True
        return False

    def showAccounts(self) -> dict:
        if self.isAuthenticated:
            return self.bank.getAccounts(self.card)
        else:
            return None

    def selectAccount(self, accountType: Account) -> bool:
        if self.bank.validateAccount(self.card, accountType):
            self.accountType = accountType
            return True
        else:
            self.accountType = None
            return False

    def executeTransaction(self, transaction: Transaction, inputAmount: int) -> dict:

        params = {
            'cardNumber': self.card,
            'accountType': self.accountType,
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
