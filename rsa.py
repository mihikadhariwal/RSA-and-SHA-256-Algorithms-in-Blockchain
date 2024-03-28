import streamlit as st
import hashlib

# Functions for RSA encryption and decryption, and key generation 
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1

    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0

    return x1 + m0 if x1 < 0 else x1
def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Commonly used public exponent
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(message, private_key):
    d, n = private_key
    cipher = [pow(ord(char), d, n) for char in message]
    return cipher

def decrypt(cipher, public_key):
    e, n = public_key
    plain = [chr(pow(char, e, n)) for char in cipher]
    return ''.join(plain)

class Block:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.public_key, self.private_key = generate_keypair(61, 53)
        # self.encrypted_amount = encrypt(str(amount), self.public_key)
        # self.decrypted_amount = decrypt(self.encrypted_amount, self.private_key)

        # Hashing and signing using SHA-256
        transaction_data = f"{sender}{receiver}{amount}"
        self.hash = hashlib.sha256(transaction_data.encode()).hexdigest()
        self.signature = encrypt(self.hash, self.private_key)

    def verify_signature(self):
        decrypted_hash = decrypt(self.signature, self.public_key)
        return self.hash == decrypted_hash

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, sender, receiver, amount):
        block = Block(sender, receiver, amount)
        self.chain.append(block)
        
    
    def display_chain(self):
        return self.chain

def main():
    st.title("RSA Encryption in a Simple Blockchain")

    if 'blockchain' not in st.session_state:
        st.session_state.blockchain = Blockchain()
    menu_choice = st.sidebar.selectbox("Menu:", ["Add a Block", "Display Blockchain"])

    if menu_choice == "Add a Block":
        st.subheader("Add a Block")
        sender = st.text_input("Enter sender:")
        receiver = st.text_input("Enter receiver:")
        amount = st.number_input("Enter amount:")

        if st.button("Add Block"):
            st.session_state.blockchain.add_block(sender, receiver, amount)
            st.success("Block added successfully")

    elif menu_choice == "Display Blockchain":
        st.subheader("Blockchain")
        chain = st.session_state.blockchain.display_chain()
        
        if len(chain) == 0:
            st.write("Blockchain is empty.")
        else:
            for index, block in enumerate(chain, start=1):
                st.write(f"Block {index}:")
                st.write(f"Sender: {block.sender}")
                st.write(f"Receiver: {block.receiver}")
                st.write(f"Amount: {block.amount}")
                # st.write(f"Encrypted Amount: {block.encrypted_amount}")
                
                st.write(f"Block Hash: {block.hash}")
                st.write(f"Signature: {block.signature}")
                # st.write(f"Decrypted signature: {block.decrypted_hash}")
                st.write(f"Signature Verified: {block.verify_signature()}")
                st.write("")

if __name__ == "__main__":
    main()
