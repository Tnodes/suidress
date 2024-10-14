from lib.convert import generate_wallet
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum
import json
import os
from lib.merger import merge_addresses

def generate_mnemonic():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    return mnemonic.ToStr()  # Convert Bip39Mnemonic to string

def generate_and_print_wallet(index=None):
    mnemonic = generate_mnemonic()
    wallet_info = generate_wallet(mnemonic)
    
    wallet_data = {
        "mnemonic": mnemonic,
        "sui_address": wallet_info['address'],
        "private_key": wallet_info['private_key']
    }
    
    print(f"\nGenerated Wallet{f' #{index}' if index else ''}:")
    print(f"12-word mnemonic: {mnemonic}")
    print(f"SUI official wallet address: {wallet_info['address']}")
    print(f"Private key: {wallet_info['private_key']}")
    print("-" * 50)
    
    return wallet_data

def save_wallets_to_json(wallets):
    while True:
        filename = input("Enter the file name to save the wallets (without extension): ").strip()
        if filename:
            if not filename.lower().endswith('.json'):
                filename += '.json'
            
            if os.path.exists(filename):
                overwrite = input(f"The file '{filename}' already exists. Do you want to overwrite it? (y/n): ").lower()
                if overwrite != 'y':
                    continue
            
            with open(filename, "w") as f:
                json.dump(wallets, f, indent=2)
            print(f"Wallets saved to {filename}")
            break
        else:
            print("Please enter a valid file name.")

def save_merged_addresses(merged_addresses):
    output_base = input("Enter the base name for the output file (without extension): ")
    
    # Save only as TXT in the current working directory
    txt_output = f"{output_base}.txt"
    
    with open(txt_output, 'w') as txt_file:
        for address in merged_addresses:
            txt_file.write(f"{address}\n")
    
    print(f"Merged SUI addresses saved to {txt_output}")

def banner():
    print("""
    SUIDRESS                                       @Tnodes
    ------------------------------------------------------
     A CLI tool for generating and merging SUI addresses
    ------------------------------------------------------                                    
    """)

def main():
    while True:
        banner()
        print("Wallet Generator Menu:")
        print("1. Generate a single wallet")
        print("2. Generate multiple wallets")
        print("3. Merge SUI addresses from existing JSON files")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            wallet = generate_and_print_wallet()
            save_wallets_to_json({"1": wallet})
        elif choice == '2':
            try:
                num_wallets = int(input("How many wallets do you want to generate? "))
                wallets = {}
                for i in range(1, num_wallets + 1):
                    wallet = generate_and_print_wallet(i)
                    wallets[str(i)] = wallet
                save_wallets_to_json(wallets)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == '3':
            merged_addresses = merge_addresses()
            if merged_addresses:
                save_merged_addresses(merged_addresses)
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
