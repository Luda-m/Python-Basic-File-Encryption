from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
            
        print(f"-> New key generated and saved as '{KEY_FILE}'.")
    else:
        print(f"-> Using existing key found in '{KEY_FILE}'.")

def load_key():
    if not os.path.exists(KEY_FILE):
        print("Error: Key file not found! Please generate a key first.")
        
        return None
    
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_file(filename, key):
    f = Fernet(key)

    try:
        with open(filename, "rb") as file:
            original_data = file.read()

        encrypted_data = f.encrypt(original_data)

        new_filename = filename + ".encrypted"
        
        with open(new_filename, "wb") as file:
            file.write(encrypted_data)
            
        print(f"Success! Encrypted file saved as: {new_filename}")
        
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decrypt_file(filename, key):
    f = Fernet(key)

    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = f.decrypt(encrypted_data)

        if filename.endswith(".encrypted"):
            original_filename = filename[:-10]
        else:
            original_filename = "decrypted_" + filename

        with open(original_filename, "wb") as file:
            file.write(decrypted_data)

        print(f"Success! File restored as: {original_filename}")

    except Exception as e:
        print("Error: Decryption failed. Are you using the correct key?")

def main():
    print("-------------------------------------")
    print("     🔒 Secure File Encryptor"       )
    print("-------------------------------------")
    
    generate_key()
    key = load_key()

    while True:
        print("\nOPTIONS:")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")
        
        choice = input("Select (1-3): ")

        if choice == '1':
            fname = input("Enter filename to encrypt (e.g., mydata.txt): ").strip()
            encrypt_file(fname, key)
            
        elif choice == '2':
            fname = input("Enter filename to decrypt (e.g., mydata.txt.encrypted): ").strip()
            decrypt_file(fname, key)
            
        elif choice == '3':
            print("Exiting program...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()