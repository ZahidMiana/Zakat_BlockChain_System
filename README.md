# 🕌 Zakat Blockchain System

A comprehensive blockchain-based system for managing Zakat (Islamic charitable giving) transactions with automatic calculation and secure transaction tracking.

## 🌟 Features

### Core Functionality
- **Blockchain Implementation**: Complete blockchain with genesis block, hash validation, and chain integrity
- **Automatic Zakat Calculation**: 2.5% Zakat automatically deducted for users with balance > 1000 coins
- **User Management**: Create and manage users with unique roll numbers
- **Secure Transactions**: SHA-256 hash-based security for all blocks and transactions
- **Transaction History**: Complete audit trail of all transactions
- **Balance Validation**: Prevents insufficient balance transactions

### Two Interface Options
1. **Command Line Interface**: Interactive terminal-based application
2. **Web Dashboard**: Modern, responsive Streamlit web application

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ZahidMiana/Zakat_BlockChain_System.git
   cd Zakat_BlockChain_System
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv blockchain_env
   source blockchain_env/bin/activate  # On Windows: blockchain_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Option 1: Command Line Interface
Run the terminal-based application:
```bash
python zakat_blockchain.py
```

#### Available Commands:
1. **Create User** - Add new users to the system
2. **Make Transaction** - Send coins between users (with automatic Zakat)
3. **Print Users** - View all registered users and their balances
4. **Print Blockchain** - Display complete blockchain structure
5. **Print Transaction History** - Show all past transactions
6. **Validate Blockchain** - Verify blockchain integrity
7. **Exit** - Close the application

### Option 2: Web Dashboard
Launch the Streamlit web interface:
```bash
streamlit run streamlit_dashboard.py
```

#### Web Features:
- 🏠 **Dashboard**: Overview with key metrics and statistics
- 👥 **User Management**: Create and view users with interactive forms
- 💸 **Transactions**: Send money with real-time balance updates
- ⛓️ **Blockchain Explorer**: Visualize blocks and their contents
- 📊 **Transaction History**: Browse complete transaction timeline
- ✅ **Validation Tool**: Check blockchain integrity with detailed reports

## 📊 How Zakat Works

### Zakat Calculation Rules
- **Threshold**: Users with balance > 1000 coins
- **Rate**: 2.5% of the sender's balance
- **Deduction**: Automatically applied during transactions
- **Validation**: Ensures sufficient balance for both transaction and Zakat

### Example Transaction
```
User A Balance: 2000 coins
Sending: 500 coins to User B
Zakat: 2000 × 0.025 = 50 coins
Final: User A = 1450 coins, User B = +500 coins
```

## 🔧 System Architecture

### Classes

#### `Block`
- **Attributes**: index, timestamp, transactions, previous_hash, roll_number_seed, hash
- **Methods**: compute_hash()

#### `User`
- **Attributes**: name, roll_number, balance
- **Purpose**: Store user information and account balance

#### `Blockchain`
- **Core Methods**:
  - `create_genesis_block()`: Initialize blockchain
  - `add_user()`: Register new users
  - `make_transaction()`: Process payments with Zakat
  - `calculate_zakat()`: Compute 2.5% charitable contribution
  - `is_chain_valid()`: Verify blockchain integrity
  - `add_block()`: Append new blocks securely

### Security Features
- **SHA-256 Hashing**: Each block is cryptographically secured
- **Chain Validation**: Prevents tampering with transaction history
- **Balance Verification**: Ensures no double-spending
- **Immutable Records**: Transaction history cannot be altered

## 📁 Project Structure

```
Zakat_BlockChain_System/
│
├── zakat_blockchain.py      # Core blockchain implementation & CLI
├── streamlit_dashboard.py   # Web interface application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── blockchain_env/         # Virtual environment (if created)
```

## 🧪 Testing the System

### Sample Workflow
1. **Create Users**:
   - Alice (Roll: 001, Balance: 2000)
   - Bob (Roll: 002, Balance: 500)

2. **Make Transaction**:
   - Alice sends 300 to Bob
   - Zakat: 50 coins deducted from Alice
   - Result: Alice=1650, Bob=800

3. **Validate**:
   - Check blockchain integrity
   - View transaction history

## 🛠️ Dependencies

```
streamlit==1.28.1
hashlib2==1.0.1
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Zahid Miana**
- GitHub: [@ZahidMiana](https://github.com/ZahidMiana)
- Repository: [Zakat_BlockChain_System](https://github.com/ZahidMiana/Zakat_BlockChain_System)

## 🙏 Acknowledgments

- Islamic principles of Zakat (charitable giving)
- Blockchain technology for secure transactions
- Streamlit for beautiful web interfaces
- Python cryptographic libraries

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/ZahidMiana/Zakat_BlockChain_System/issues) section
2. Create a new issue with detailed description
3. Contact the author through GitHub

---

**Built with ❤️ for the blockchain and Islamic finance community**

## 🎯 Future Enhancements

- [ ] Multiple cryptocurrency support
- [ ] Advanced user authentication
- [ ] Mobile application
- [ ] Integration with real Islamic banks
- [ ] Smart contract implementation
- [ ] Multi-language support (Arabic, Urdu)
- [ ] Advanced analytics dashboard
- [ ] Export/Import functionality