# utils/helpers.py

def generate_mnemonic(tripcode: str) -> str:
    """
    Generates a mnemonic from a tripcode.
    
    Parameters:
        tripcode (str): The user's tripcode.
        
    Returns:
        str: A human-friendly mnemonic derived from the tripcode.
    """
    mnemonic_starts = ['ka', 'shi', 'su', 'se', 'so', 'ta', 'chi', 'tsu', 
                       'te', 'to', 'na', 'ni', 'nu', 'ne', 'no']
    mnemonic_ends = ['a', 'i', 'u', 'e', 'o', 'ya', 'yu', 'yo', 'wa', 
                     'wo', 'ra', 'ri', 'ru', 're', 'ro']
    
    chars = tripcode[:4]
    nums = [ord(c) % len(mnemonic_starts) for c in chars]
    parts = [mnemonic_starts[n % len(mnemonic_starts)] + 
             mnemonic_ends[n % len(mnemonic_ends)] for n in nums]
    mnemonic = ''.join(parts[:2])
    return mnemonic