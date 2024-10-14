# ref: https://github.com/satisfywithmylife/suiwallet-py

from bip_utils import Bip39SeedGenerator, Bip44Coins, Bip44, Bip39Mnemonic
from bech32 import bech32_encode, convertbits


# only support ed25519 schema
class Suiwallet:
    
    def __init__(self, mnemonic, password='') -> None:
        if isinstance(mnemonic, Bip39Mnemonic):
            self.mnemonic = mnemonic.ToStr()
        elif isinstance(mnemonic, str):
            self.mnemonic = mnemonic.strip()
        else:
            raise ValueError("Mnemonic must be a string or Bip39Mnemonic object")
        self.password = password
        self.pk_prefix = 'suiprivkey'
        self.ed25519_schema = '00'
        
    def get_address_pk(self, pk_with_prefix=True):
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate(self.password)
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SUI).DeriveDefaultPath()
        address = bip44_mst_ctx.PublicKey().ToAddress()
        pk = bip44_mst_ctx.PrivateKey().Raw().ToHex() # hex type pk
        
        if pk_with_prefix: # sui official wallet cant import hex type pk to wallet
            pk_bytes_with_schema = bytes.fromhex(f'{self.ed25519_schema}{pk}')
            pk_bit_arr = convertbits(pk_bytes_with_schema, 8, 5)
            pk = bech32_encode(self.pk_prefix, pk_bit_arr) # result like "suiprivkey1q............"
            
        return address, pk

def generate_wallet(mnemonic):
    sw = Suiwallet(mnemonic)
    address, pk = sw.get_address_pk()
    return {
        'mnemonic': sw.mnemonic,
        'address': address,
        'private_key': pk
    }
