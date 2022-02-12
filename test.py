import unittest
from atm import ATM
from bank import Bank
from constant import INITIAL_AVAILABLE_AMOUNT, Account, Status, Transaction


class AtmTest(unittest.TestCase):
    def testAtm(self):
        atm = ATM()
        self.assertEqual(atm.availableAmount, INITIAL_AVAILABLE_AMOUNT)

    def testCard(self):
        atm = ATM()

        # if card is inserted and not valid
        isCardInserted = atm.insertCard('2022-2022-0000-0005')
        self.assertEqual(isCardInserted, False)
        self.assertEqual(atm.card, None)

        # if card is inserted and valid
        isCardInserted = atm.insertCard('2022-2022-0000-0000')
        self.assertEqual(isCardInserted, True)
        self.assertEqual(atm.card, '2022-2022-0000-0000')

    def testAuth(self):
        atm = ATM()

        # if inserted PIN is not valid
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('1111')
        self.assertEqual(atm.isAuthenticated, False)

        # if inserted PIN is valid
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('0000')
        self.assertEqual(atm.isAuthenticated, True)

    def testAccounts(self):
        atm = ATM()
        bank = Bank()

        # if inserted PIN is not valid
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('1111')
        self.assertEqual(atm.showAccounts(), None)

        # if inserted card number is not valid
        atm.insertCard('2022-2022-0000-0010')
        atm.insertPin('0000')
        self.assertEqual(atm.showAccounts(), None)

        # valid card and valid PIN
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('0000')
        self.assertEqual(atm.showAccounts(),
                         bank.getAccounts('2022-2022-0000-0000'))

    def testSelectAccount(self):
        atm = ATM()

        # # if inserted card number is not valid
        atm.insertCard('2022-2022-0000-0010')
        atm.insertPin('0000')
        self.assertEqual(atm.selectAccount(Account['CHECKING']), False)
        self.assertEqual(atm.selectedAccount, None)

        # if inserted PIN is not valid
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('1111')
        self.assertEqual(atm.selectAccount(Account['CHECKING']), False)
        self.assertEqual(atm.selectedAccount, None)

        # if selected account is not valid
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('0000')
        self.assertEqual(atm.selectAccount('Debit'), False)
        self.assertEqual(atm.selectedAccount, None)

        # valid card and valid PIN and valid account
        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('0000')
        self.assertEqual(atm.selectAccount(Account['CHECKING']), True)
        self.assertEqual(atm.selectedAccount, Account['CHECKING'])

    def testExecuteTransaction(self):
        atm = ATM()

        atm.insertCard('2022-2022-0000-0000')
        atm.insertPin('0000')
        accounts = atm.showAccounts()

        # check validity for each account
        for account in accounts:
            atm.selectAccount(account)

            # all transactions valid for each account
            for transaction in Transaction.values():
                transactionResult = atm.executeTransaction(
                    transaction, 0 if transaction == Transaction['BALANCE'] else 10000)
                self.assertEqual(
                    transactionResult['status'], Status['SUCCESS'])

            # invalid transaction type
            transactionResult = atm.executeTransaction(
                'Remittance', 10000)
            self.assertEqual(
                transactionResult['status'], Status['ERROR'])

            # invalid requested amount (not enough money on account or in atm)
            transactionResult = atm.executeTransaction(
                Transaction['WITHDRAW'], 10000000)
            self.assertEqual(
                transactionResult['status'], Status['ERROR'])


if __name__ == "__main__":
    unittest.main()
