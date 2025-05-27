# QR Code Error Correction Code Generation Module: Generate error correction codes using Reed-Solomon algorithm

from constant import ecc_num_per_block, lindex
from reedsolo import RSCodec

def encode(ver, ecl, data_codewords):
    """
    Generate error correction codewords
    Args:
        ver: QR code version (1-40)
        ecl: Error correction level (L/M/Q/H)
        data_codewords: List of data codewords, each element is a data block
    Returns:
        ecc: List of error correction codewords, corresponding one-to-one with input data blocks
    """
    # Get the number of error correction codewords needed per block
    ecc_num = ecc_num_per_block[ver-1][lindex[ecl]]
    
    # Initialize Reed-Solomon encoder
    rs = RSCodec(ecc_num)
    
    # Generate corresponding error correction codes for each data block
    ecc = []
    for dc in data_codewords:
        # Convert data block to bytes array
        data_bytes = bytes(dc)
        
        # Encode and get error correction part
        encoded = rs.encode(data_bytes)
        
        # Only take the error correction part (remove the original data part)
        ecc_bytes = encoded[-ecc_num:]
        
        # Convert to integer list and add to result
        ecc.append(list(ecc_bytes))
    
    return ecc

# Code for testing
if __name__ == '__main__':
    # Example: Version 1, M level error correction, containing one data block
    ver = 1
    ecl = 'M'
    test_data = [[32, 65, 205, 69, 41, 220, 46, 128, 236]]
    
    ecc = encode(ver, ecl, test_data)
    print(f"Input data block: {test_data[0]}")
    print(f"Generated ECC: {ecc[0]}")