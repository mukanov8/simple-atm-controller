# Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

# I assume that there are only two bank account types: checking(usual) and savings(deposit)

from constant import Account, Transaction, Status

mockBankDb = {
    '2022-2022-0000-0000': {
        'pin': '0000',
        'accounts': {
            Account['CHECKING']: {
                'balance': 10000,
            },
            Account['SAVINGS']: {
                'balance': 20000,
            },
        },
    },
    '2022-2022-0000-0001': {
        'pin': '0001',
        'accounts': {
            Account['CHECKING']: {
                'balance': 20000,
            },
            Account['SAVINGS']: {
                'balance': 40000,
            },
        },
    },
    '2022-2022-0000-0002': {
        'pin': '0002',
        'accounts': {
            Account['CHECKING']: {
                'balance': 30000,
            },
            Account['SAVINGS']: {
                'balance': 50000,
            },
        },
    },
}


class Bank:
    def __init__(self):
        self.db = mockBankDb

    def validateCard(self, cardNumber: str) -> bool:
        return cardNumber in self.db

    def validatePin(self, cardNumber: str, pinNumber: str) -> bool:
        if self.validateCard(cardNumber):
            return self.db[cardNumber]['pin'] == pinNumber
        return False

    def validateAccount(self, cardNumber: str, account: str) -> bool:
        if self.validateCard(cardNumber):
            return account in self.db[cardNumber]['accounts']
        return False

    def getAccounts(self, cardNumber: str):
        if self.validateCard(cardNumber):
            return self.db[cardNumber]['accounts']
        return None

    def transaction(self, params: dict) -> dict:
        '''
          A method to process transaction,
          params: {
            'cardNumber': cardNumber,
            'account': Account,
            'inputAmount': inputAmount,
            'transaction': Transaction,
            'availableAmount': availableAmount,
            'balance': None,
            'status': None,
            'message': None,
          }
        '''

        cardNumber = params['cardNumber']
        selectedAccount = params['account']
        inputAmount = params['inputAmount']
        account = self.db[cardNumber]['accounts'][selectedAccount]

        if params['inputAmount'] < 0:
            params['status'] = Status['ERROR']
            params['message'] = 'Please input money!'
            # return

        if params['transaction'] == Transaction['BALANCE']:
            params['status'] = Status['SUCCESS']
            params['message'] = 'Displaying current balance...'
        elif params['transaction'] == Transaction['DEPOSIT']:
            if not inputAmount:
                params['status'] = Status['ERROR']
                params['message'] = 'Please input amount to deposit!'
            else:
                params['status'] = Status['SUCCESS']
                params['message'] = '{} completed'.format(
                    Transaction['DEPOSIT'])
                self.db[cardNumber]['accounts'][selectedAccount]['balance'] += inputAmount
                params['availableAmount'] += inputAmount
        elif params['transaction'] == Transaction['WITHDRAW']:
            if not inputAmount:
                params['status'] = Status['ERROR']
                params['message'] = 'Please input amount to withdraw!'
            else:
                if inputAmount > params['availableAmount']:
                    params['status'] = Status['ERROR']
                    params['message'] = 'Insufficient funds in the ATM'
                elif inputAmount > self.db[cardNumber]['accounts'][selectedAccount]['balance']:
                    params['status'] = Status['ERROR']
                    params['message'] = 'Insufficient funds on the account. Available: {}'.format(
                        account['balance'])
                else:
                    self.db[cardNumber]['accounts'][selectedAccount]['balance'] -= inputAmount
                    params['availableAmount'] -= inputAmount
                    params['status'] = Status['SUCCESS']
                    params['message'] = '{} completed'.format(
                        Transaction['WITHDRAW'])

        else:
            params['status'] = Status['ERROR']
            params['message'] = 'Please select valid transaction type'
            return params

        params['balance'] = self.db[cardNumber]['accounts'][selectedAccount]['balance']
        return params
