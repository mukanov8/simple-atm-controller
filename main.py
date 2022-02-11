# Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

from atm import ATM
from constant import Account, Transaction

if __name__ == "__main__":

    atm = ATM()

    while(True):
        print('\n################### \n')
        print('ATM is running... \n')
        print('################### \n')

        while True:
            print('Please insert your 16-digit card number to start')
            cardNumber = input('****-****-****-****: ')
            if not atm.insertCard(cardNumber):
                print('Error: ', cardNumber, ' is not valid card number.\n')
                continue
            else:
                print('Processing...\n')
                break

        while True:
            print('Please insert your 4-digit pin number')
            pinNumber = input('****: ')
            if not atm.insertPin(pinNumber):
                print('Error: Invalid pin number.\n')
            else:
                print('Processing...\n')
                break

        print('Fetching Accounts...')

        accountsToShow = atm.showAccounts()
        if not accountsToShow:
            print('Error: No accounts found associated with this card number.\n')
            continue
        for account in accountsToShow:
            print('Account: {} '.format(account))

        print('\n')
        print('Please select account for transaction')
        while True:
            accountType = input('{} or {}?: '.format(
                Account['CHECKING'], Account['SAVINGS']))
            if accountType not in Account.values():
                print("Error: Please input valid account type.\n")
            if atm.selectAccount(accountType):
                print('Success: You have selected {} account type.\n'.format(
                    accountType))
                break
            else:
                print("Error: '{}' is not valid account type.\n".format(accountType))

        print('Please choose desired transaction to be performed with this {} account'.format(
            accountType))

        while True:
            transaction = input("{} or {} or {}?: ".format(
                Transaction['BALANCE'], Transaction['DEPOSIT'], Transaction['WITHDRAW']))
            result = atm.executeTransaction(transaction, 0)

            if transaction == Transaction['DEPOSIT'] or transaction == Transaction['WITHDRAW']:
                inputAmount = int(
                    input('Please input the amount to {}: '.format(transaction.lower())))
                result = atm.executeTransaction(transaction, inputAmount)
            elif transaction == Transaction['BALANCE']:
                result = atm.executeTransaction(transaction, 0)
            else:
                print('Error: Please select valid transaction type')
                continue

            print('\n')

            print('{}: {}'.format(result['status'], result['message']))
            print('Account Balance: {}\n'.format(result['balance']))
            break
