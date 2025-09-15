"""
Zakat Blockchain Web Dashboard
Built with Streamlit

source blockchain_env/bin/activate
pip install -r requirements.txt
streamlit run streamlit_dashboard.py
"""

import streamlit as st
import hashlib
import time
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Zakat Blockchain",
    page_icon="⛓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .block-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .user-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .transaction-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .sidebar .stSelectbox {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

class Block:
    def __init__(self, index, transactions, previous_hash, roll_number_seed):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.roll_number_seed = roll_number_seed
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = str(self.index) + str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.roll_number_seed)
        return hashlib.sha256(block_string.encode()).hexdigest()

class User:
    def __init__(self, name, roll_number, balance):
        self.name = name
        self.roll_number = roll_number
        self.balance = balance

class Blockchain:
    def __init__(self):
        self.chain = []
        self.users = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0", "GENESIS")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_user(self, name, roll_number, balance):
        if roll_number in self.users:
            return False, "User with this roll number already exists."
        self.users[roll_number] = User(name, roll_number, balance)
        return True, f"User {name} (Roll: {roll_number}) created with {balance} coins."

    def calculate_zakat(self, balance):
        return round(balance * 0.025, 2)

    def make_transaction(self, sender_roll, receiver_roll, amount):
        if sender_roll not in self.users or receiver_roll not in self.users:
            return False, "Sender or receiver does not exist."
        
        sender = self.users[sender_roll]
        receiver = self.users[receiver_roll]
        
        if sender.balance < amount:
            return False, "Sender has insufficient balance."

        zakat = 0
        if sender.balance > 1000:
            zakat = self.calculate_zakat(sender.balance)
            if sender.balance < (amount + zakat):
                return False, "Sender does not have enough balance for transaction and Zakat."
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
        return True, f"{amount} coins sent from {sender.name} to {receiver.name}. Zakat deducted: {zakat}"

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
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Initialize blockchain in session state
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

# Main header
st.markdown('<h1 class="main-header">⛓️ Zakat Blockchain System</h1>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Navigation")
page = st.sidebar.selectbox("Choose Action", [
    "🏠 Dashboard", 
    "👤 Create User", 
    "💸 Make Transaction", 
    "👥 View Users", 
    "⛓️ View Blockchain", 
    "📊 Transaction History", 
    "✅ Validate Chain"
])

blockchain = st.session_state.blockchain

if page == "🏠 Dashboard":
    st.header("📊 Blockchain Overview")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Users</h3>
            <h2>{len(blockchain.users)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⛓️ Total Blocks</h3>
            <h2>{len(blockchain.chain)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_coins = sum(user.balance for user in blockchain.users.values())
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Total Coins</h3>
            <h2>{total_coins}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_transactions = sum(len(block.transactions) for block in blockchain.chain)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Transactions</h3>
            <h2>{total_transactions}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent transactions
    st.subheader("🔥 Recent Transactions")
    recent_blocks = blockchain.chain[-3:] if len(blockchain.chain) > 1 else blockchain.chain[1:]
    
    for block in reversed(recent_blocks):
        if block.transactions:
            for tx in block.transactions:
                st.markdown(f"""
                <div class="transaction-card">
                    <strong>💸 {tx['sender']} → {tx['receiver']}</strong><br>
                    Amount: {tx['amount']} coins | Zakat: {tx['zakat_deducted']} coins<br>
                    Time: {datetime.fromtimestamp(tx['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}
                </div>
                """, unsafe_allow_html=True)

elif page == "👤 Create User":
    st.header("👤 Create New User")
    
    with st.form("create_user"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("📝 User Name", placeholder="Enter full name")
            roll_number = st.text_input("🎯 Roll Number", placeholder="Enter roll number")
        
        with col2:
            balance = st.number_input("💰 Initial Coins", min_value=0.0, value=200.0, step=10.0)
        
        submitted = st.form_submit_button("🚀 Create User")
        
        if submitted:
            if name and roll_number:
                success, message = blockchain.add_user(name, roll_number, balance)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("❌ Please fill all fields!")

elif page == "💸 Make Transaction":
    st.header("💸 Make Transaction")
    
    if len(blockchain.users) < 2:
        st.warning("⚠️ Need at least 2 users to make transactions!")
    else:
        with st.form("make_transaction"):
            col1, col2 = st.columns(2)
            
            user_options = list(blockchain.users.keys())
            
            with col1:
                sender = st.selectbox("📤 Sender Roll Number", user_options)
                amount = st.number_input("💰 Amount to Send", min_value=0.1, step=10.0)
            
            with col2:
                receiver_options = [u for u in user_options if u != sender]
                receiver = st.selectbox("📥 Receiver Roll Number", receiver_options)
            
            # Show sender balance
            if sender:
                sender_balance = blockchain.users[sender].balance
                st.info(f"💳 Sender Balance: {sender_balance} coins")
                
                if sender_balance > 1000:
                    zakat = blockchain.calculate_zakat(sender_balance)
                    st.warning(f"⚠️ Zakat will be deducted: {zakat} coins (Balance > 1000)")
            
            submitted = st.form_submit_button("🚀 Send Transaction")
            
            if submitted:
                success, message = blockchain.make_transaction(sender, receiver, amount)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")

elif page == "👥 View Users":
    st.header("👥 All Users")
    
    if not blockchain.users:
        st.info("ℹ️ No users found. Create some users first!")
    else:
        for user in blockchain.users.values():
            st.markdown(f"""
            <div class="user-card">
                <h3>👤 {user.name}</h3>
                <p><strong>Roll Number:</strong> {user.roll_number}</p>
                <p><strong>Balance:</strong> {user.balance} coins</p>
                <p><strong>Zakat Eligible:</strong> {'✅ Yes' if user.balance > 1000 else '❌ No'}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "⛓️ View Blockchain":
    st.header("⛓️ Blockchain Structure")
    
    for i, block in enumerate(blockchain.chain):
        st.markdown(f"""
        <div class="block-card">
            <h3>🔗 Block {block.index}</h3>
            <p><strong>Hash:</strong> {block.hash[:20]}...</p>
            <p><strong>Previous Hash:</strong> {block.previous_hash[:20]}...</p>
            <p><strong>Timestamp:</strong> {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Transactions:</strong> {len(block.transactions)}</p>
            <p><strong>Seed:</strong> {block.roll_number_seed}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if block.transactions:
            with st.expander(f"📊 View {len(block.transactions)} Transaction(s)"):
                for tx in block.transactions:
                    st.json(tx)

elif page == "📊 Transaction History":
    st.header("📊 Transaction History")
    
    all_transactions = []
    for block in blockchain.chain[1:]:  # Skip genesis
        for tx in block.transactions:
            all_transactions.append(tx)
    
    if not all_transactions:
        st.info("ℹ️ No transactions found!")
    else:
        for i, tx in enumerate(reversed(all_transactions)):
            st.markdown(f"""
            <div class="transaction-card">
                <h4>🔄 Transaction #{len(all_transactions) - i}</h4>
                <p><strong>From:</strong> {tx['sender']} <strong>To:</strong> {tx['receiver']}</p>
                <p><strong>Amount:</strong> {tx['amount']} coins</p>
                <p><strong>Zakat Deducted:</strong> {tx['zakat_deducted']} coins</p>
                <p><strong>Sender Balance After:</strong> {tx['sender_balance']} coins</p>
                <p><strong>Receiver Balance After:</strong> {tx['receiver_balance']} coins</p>
                <p><strong>Time:</strong> {datetime.fromtimestamp(tx['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "✅ Validate Chain":
    st.header("✅ Blockchain Validation")
    
    if st.button("🔍 Validate Blockchain"):
        is_valid = blockchain.is_chain_valid()
        
        if is_valid:
            st.success("✅ Blockchain is valid! All blocks are properly linked and secure.")
        else:
            st.error("❌ Blockchain is invalid! Someone may have tampered with the data.")
        
        # Show detailed validation info
        st.subheader("🔍 Detailed Validation Report")
        
        for i in range(1, len(blockchain.chain)):
            current = blockchain.chain[i]
            previous = blockchain.chain[i-1]
            
            hash_valid = current.hash == current.compute_hash()
            link_valid = current.previous_hash == previous.hash
            
            status = "✅" if (hash_valid and link_valid) else "❌"
            
            st.markdown(f"""
            <div class="block-card">
                <h4>{status} Block {current.index} Validation</h4>
                <p>Hash Valid: {'✅' if hash_valid else '❌'}</p>
                <p>Link Valid: {'✅' if link_valid else '❌'}</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🔗 **Zakat Blockchain System** - Built with ❤️ using Streamlit")
