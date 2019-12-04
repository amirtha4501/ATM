import abc
from abc import ABC, abstractmethod
import json

# Abstract Class
class AbstractTransaction(ABC):
    # Abstract Methods

    @abc.abstractproperty
    def login(self):
        pass
    
    @abc.abstractproperty
    def amount_transfer(self):
        pass

    @abc.abstractproperty
    def credit(self):
        pass

    @abc.abstractproperty
    def debit(self):
        pass


class Account(AbstractTransaction):
    
    def __init__(self):
        
        # Reads the json file 
        with open('details.json','r') as f:
            self.accounts = json.load(f)

        # Variable that can be accessed throughout the program
        self.sender_name = 0
        self.receiver_name = 0
        self.sender_acc = 0
        self.receiver_acc = 0
        self.sender_balance = 0
        self.receiver_balance = 0        
        self.count = 0
        self.deb_count = 0
        self.cre_count = 0
        self.tot_trans = 0
        self.phone = 0
        self.balance = 0        

    # Private method that implements encapsulation to check the account's existance.
    def __check(self):            
        
        if self.sender_acc in self.accounts.keys(): # Checks the accno of sender's presence in dictionary called accounts
        
            if self.upi_accesser in self.accounts[self.sender_acc].values():# Compare the upi of sender with the dictionary which is nested
                return True
        
            else:
                return False
        
        else:
            return False


    # Login method
    def login(self):
        self.sender_acc = input("\nEnter account number: ")
        self.upi_accesser = int(input("Enter Password: "))
           
        a = self.__check()

        if a:
            self.manage_account()
        
        else:
            print("Account number or password is incorrect.")
            self.login()


    # Creates an account
    def register(self):
        # Getting input
        self.sender_acc = input("\nEnter account number: ")
        self.upi_accesser = int(input("Enter password: "))
        self.sender_name = input("Enter your name: ")
        self.sender_balance = int(input("Enter your starting balance: "))
        self.phone = int(input("Enter mobile number: "))

        # Opens file in read mode
        with open('details.json','r') as f:
            self.accounts = json.load(f)

        a = {
            self.sender_acc : {
                'name' : self.sender_name,
                'balance' : self.sender_balance,
                'upi' : self.upi_accesser,
                'phone' : self.phone
            }
        } 

        self.accounts.update(a) # Updates the dictionary

        with open('details.json', 'w') as f:
            json.dump(self.accounts, f, indent=4)


    # Transfers money from one user to another
    def amount_transfer(self):       
        self.sender_balance = self.accounts[self.sender_acc]['balance'] # accesses sender's balance
        self.money_value = int(input("\nEnter amount to transfer: "))

        if self.money_value < self.sender_balance: 
            self.receiver_acc = input("\nEnter receiver's account number: ")

            if self.receiver_acc in self.accounts.keys(): # Receiver's account presence in accounts dict 
                self.sender_balance = self.sender_balance - self.money_value
                self.receiver_balance = self.accounts[self.receiver_acc]['balance'] #accesses receiver's balance
                self.receiver_balance = self.receiver_balance + self.money_value
                self.sender_name = self.accounts[self.sender_acc]['name'].title()
                self.receiver_name = self.accounts[self.receiver_acc]['name'].title() 
                self.accounts[self.sender_acc]['balance'] = self.sender_balance
                self.accounts[self.receiver_acc]['balance'] = self.receiver_balance

                with open('details.json','w') as f:
                    json.dump(self.accounts, f, indent=4)

                print("\n\n__________________________________________________")
                print("\n**************Transaction successful**************")
                print("__________________________________________________\n")
                print("\nYour current balance is:  ", self.sender_balance,"\n")
                self.count = self.count + 1

            else:
                print("__________________________________________________\n")
                print("\nDear Customer!\n\t\tReceiver's Account number is incorrect.")

        else:
            print("\n__________________________________________________")
            print("\n\t\tTRANSACTION FAILED")        
            print("__________________________________________________\n")
            print("Dear customer,\n\tTransaction is failed since you have insufficient balance.")
        print("\n__________________________________________________\n")


    # To find mini statement
    def miniStatement(self):
        print("\n\n__________________________________________________")
        print("\t\tMINI STATEMENT")
        print("__________________________________________________\n")
        print("Hi",self.accounts[self.sender_acc]['name'].title()+"!\n",)
        print("Amount transfer count : ", self.count)
        print("Debit :", self.deb_count)
        print("Credit :", self.cre_count)
        self.tot_trans = self.count + self.deb_count + self.cre_count
        print("Total Transaction : ", self.tot_trans)
        print("\n__________________________________________________\n")


    # Withdrawing the amount
    def debit(self):
        debit_val = int(input("\nEnter amount to withdraw: "))
        self.sender_balance = self.accounts[self.sender_acc]['balance']

        if(debit_val <= self.sender_balance):
            print("\n__________________________________________________")
            print("\n\t\tDEBIT SUCCESSFUL")        
            print("__________________________________________________\n")
            self.sender_balance = self.sender_balance - debit_val
            print("\nDear", self.accounts[self.sender_acc]['name'].title() + "!\n\n\tYour current balance is: ",self.sender_balance)            
            self.deb_count = self.deb_count + 1
            self.accounts[self.sender_acc]['balance'] = self.sender_balance

            with open('details.json','w') as f:
                json.dump(self.accounts, f, indent=4)

        else:
            print("\n__________________________________________________")
            print("\n\t\tDEBIT FAILED")        
            print("__________________________________________________\n")
            print("\nDear customer, Transaction is failed since you have insufficient balance.")
        print("\n__________________________________________________\n")


    # Deposit the amount
    def credit(self):
        self.sender_balance = self.accounts[self.sender_acc]['balance']
        credit_val = int(input("\n\nEnter amount to deposit: "))

        if credit_val > 1:
            self.sender_balance = self.sender_balance + credit_val
            print("\n__________________________________________________")
            print("\n\t\tCREDIT SUCCESSFUL")
            print("__________________________________________________\n")
            print("\nDear", self.accounts[self.sender_acc]['name'].title() + "!\n\n\tYour current balance is: ",self.sender_balance)
            self.cre_count = self.cre_count + 1
            self.accounts[self.sender_acc]['balance'] = self.sender_balance

            with open('details.json','w') as f:
                json.dump(self.accounts, f, indent=4)

        else:
            print("\n__________________________________________________")
            print("\n\t\tDECLINED")
            print("__________________________________________________\n")
            print("Credit amount is not sufficient.")
        print("\n__________________________________________________\n")


    # Method that call the methods for operation
    def manage_account(self):
        while True:

            try:
                print("\n\t\t1. Amount transfer\n\t\t2. Debit\n\t\t3. Credit\n\t\t4. Ministatement\n\t\t5. Exit")
                ch = int(input("\nEnter your choice: "))

                if ch == 1:
                    self.amount_transfer()

                elif ch == 2:
                    self.debit()    

                elif ch == 3:
                    self.credit()

                elif ch == 4:
                    self.miniStatement()

                elif ch == 5:
                    break 

                else:
                    print("\nEnter valid choice")      

            except:
                print("\nEnter valid choice")       

    # Method for login or register option
    def choose(self):
        print("\n==================================================\n\t\tWELCOME TO BANKING\n==================================================")
        while True:

            try:
                print("\n\t1. Login\n\t2. Register\t\n\t3. Quit\n")
                cho = int(input("Your choice: "))

                if cho == 1:
                    self.login()

                elif cho == 2:
                    self.register()

                elif cho == 3:
                    break

                else:
                    print("\nEnter valid choice")

            except:
                print("\nInvalid entry")


ac = Account()
ac.choose()