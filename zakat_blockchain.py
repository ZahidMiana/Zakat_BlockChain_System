
import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash, roll_number_seed):
        self.index = index  
        self.timestamp = time.time() 
        self.transactions = transactions 
        self.previous_hash = previous_hash  
        self.roll_number_seed = roll_number_seed
        self.hash = self.compute_hash() 

    def compute_hash(self):
        # Block ki sari info ko string bana ke hash nikalte hain
        block_string = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.roll_number_seed)
        return hashlib.sha256(block_string.encode()).hexdigest()

class User:
    def __init__(self, name, roll_number, balance):
        self.name = name  
        self.roll_number = roll_number  
        self.balance = balance 

class Blockchain:
    def __init__(self):
        self.chain = []  # Blockchain ki list
        self.users = {}  # Sare users (roll_number: User object)
        self.create_genesis_block()

    def create_genesis_block(self):
    
        genesis_block = Block(0, [], "0", "GENESIS")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_user(self, name, roll_number, balance):
        if roll_number in self.users:
            print("User with this roll number already exists.")
            return False
        self.users[roll_number] = User(name, roll_number, balance)
        print(f"User {name} (Roll: {roll_number}) created with {balance} coins.")
        return True

    def calculate_zakat(self, balance):
        return round(balance * 0.025, 2)

    def make_transaction(self, sender_roll, receiver_roll, amount):
        if sender_roll not in self.users or receiver_roll not in self.users:
            print("Sender or receiver does not exist.")
            return False
        sender = self.users[sender_roll]
        receiver = self.users[receiver_roll]
        if sender.balance < amount:
            print("Sender has insufficient balance.")
            return False

        zakat = 0

        if sender.balance > 1000:
            zakat = self.calculate_zakat(sender.balance)
            if sender.balance < (amount + zakat):
                print("Sender does not have enough balance for transaction and Zakat.")
                return False
            sender.balance -= zakat  
        sender.balance -= amount  
        receiver.balance += amount  

        transaction = {
            'sender': sender_roll,  
            'receiver': receiver_roll,  
            'amount': amount,  
            'zakat_deducted': zakat,  
            'sender_balance': sender.balance,  
            'receiver_balance': receiver.balance, 
            'timestamp': time.time() 
        }
        self.add_block([transaction], sender_roll)  
        print(f"{amount} coins sent from {sender.name} to {receiver.name}. Zakat deducted: {zakat}. Sender balance: {sender.balance}, Receiver balance: {receiver.balance}")
        return True

    def add_block(self, transactions, roll_number_seed):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=transactions,
            previous_hash=last_block.hash,
            roll_number_seed=roll_number_seed
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.compute_hash():
                print(f"Block {i} hash mismatch!")
                return False
            if current.previous_hash != previous.hash:
                print(f"Block {i} previous hash mismatch!")
                return False
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Transactions: {block.transactions}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Hash: {block.hash}\n")

    def print_transaction_history(self):
    
        print("Transaction History:")
        for block in self.chain[1:]:  
            for tx in block.transactions:
                print(tx)

    def print_users(self):
       
        print("\nUsers:")
        for user in self.users.values():
            print(f"Name: {user.name}, Roll: {user.roll_number}, Balance: {user.balance}")

if __name__ == "__main__":
    blockchain = Blockchain()
    print("\n" + "="*40)
    print("{:^40}".format("Zakat Block Chain System"))
    print("="*40)
    while True:
        print("\nPlease select an option:")
        print("  1. Create User  # Naya user banao")
        print("  2. Make Transaction  # Paise bhejo")
        print("  3. Print Users  # Sare users dekho")
        print("  4. Print Blockchain  # Blockchain dekho")
        print("  5. Print Transaction History  # Transactions dekho")
        print("  6. Validate Blockchain  # Chain sahi hai ya nahi")
        print("  7. Exit  # Bahar niklo")
        choice = input("\nEnter your choice (1-7): ")
        if choice == '1':
            name = input("    Enter user name: ")  
            roll = input("    Enter roll number: ")  
            try:
                balance = float(input("    Enter initial coin amount: "))  
                if balance < 0:
                    print("    Initial coin amount must be non-negative.")
                    continue
            except ValueError:
                print("    Invalid coin amount.")
                continue
            blockchain.add_user(name, roll, balance)
        elif choice == '2':
            sender = input("    Enter sender's roll number: ")  
            receiver = input("    Enter receiver's roll number: ") 
            try:
                amount = float(input("    Enter amount to send: ")) 
                if amount <= 0:
                    print("    Amount must be positive.")
                    continue
            except ValueError:
                print("    Invalid amount.")
                continue
            blockchain.make_transaction(sender, receiver, amount)
        elif choice == '3':
            blockchain.print_users() 
        elif choice == '4':
            blockchain.print_chain()
        elif choice == '5':
            blockchain.print_transaction_history()
        elif choice == '6':
            if blockchain.is_chain_valid():
                print("Blockchain is valid.")
            else:
                print("Blockchain is invalid!")
        elif choice == '7':
            print("Exiting Zakat Block Chain System. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
