# QR Code Matrix Generation Module: Responsible for constructing the 2D matrix structure of QR code
     
from constant import alig_location, format_info_str, version_info_str, lindex
    
def get_qrmatrix(ver, ecl, bits):
    """
    Generate QR matrix
    ver: QR code version (1-40)
    ecl: Error correction level (L/M/Q/H)
    bits: Final data
    return: QR matrix
    """

    # 1. Initialize matrix
    qrmatrix = initialize_qrmatrix(ver)

    # 2. Add finder patterns and separators
    add_finder_and_separator(qrmatrix)
    
    # 3. Add alignment patterns
    add_alignment(ver, qrmatrix)
    
    # 4. Add timing patterns
    add_timing(qrmatrix)
    
    # 5. Add dark module and reserved areas
    add_dark_and_reserving(ver, qrmatrix)
    
    # Copy matrix as mask base
    maskmatrix = [i[:] for i in qrmatrix]
    
    # 6. Place data bits
    place_bits(bits, qrmatrix)
    
    # 7. Apply data mask
    mask_num, qrmatrix = mask(maskmatrix, qrmatrix)
    
    # 8. Add format information and version information
    add_format_and_version_string(ver, ecl, mask_num, qrmatrix)

    return qrmatrix

def initialize_qrmatrix(ver):
    """
    Initialize QR matrix
    ver: QR code version (1-40)
    return: Initialized QR matrix
    """
    # Calculate QR code size
    num = (ver - 1) * 4 + 21
    # Create an empty matrix, all elements are None
    return [[None] * num for i in range(num)]

def add_finder_and_separator(m):             
    """
    Add finder patterns and separators
    m: QR matrix
    """
    # Add finder patterns and separators at the three corners: top-left, top-right, bottom-left
    # Finder pattern is a 7×7 specific pattern, separator is a 1-module wide white space
    for i in range(8):
        for j in range(8):
            if i in (0, 6):
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 0 if j == 7 else 1
            elif i in (1, 5):
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 1 if j in (0, 6) else 0  
            elif i == 7:
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 0
            else:
                m[i][j] = m[-i-1][j] = m[i][-j-1] = 0 if j in (1, 5, 7) else 1
    
    return m
    
def add_alignment(ver, m):
    """
    Add alignment patterns
    ver: QR code version (1-40)
    m: QR matrix
    """
    # Version 1 has no alignment pattern
    if ver > 1:
        # Get alignment pattern coordinates for current version
        coordinates = alig_location[ver-2]
        # Add alignment pattern at each specified coordinate, but don't overwrite existing functional areas
        for i in coordinates:
            for j in coordinates:
                if m[i][j] is None:
                    add_an_alignment(i, j, m)
            
def add_an_alignment(row, column, m):
    """
    Add one alignment pattern
    row: Row
    column: Column
    m: QR matrix
    """
    for i in range(row-2, row+3):
        for j in range(column-2, column+3):
            m[i][j] = 1 if i in (row-2, row+2) or j in (column-2, column+2) else 0
    m[row][column] = 1
    
def add_timing(m):
    """
    Add timing patterns
    m: QR matrix
    """
    for i in range(8, len(m)-8):
        m[i][6] = m[6][i] = 1 if i % 2 ==0 else 0
    
def add_dark_and_reserving(ver, m): 
    """
    Add dark module and reserved areas
    ver: QR code version (1-40)
    m: QR matrix
    """
    # Add format information area (reserved area) around finder patterns
    for j in range(8):
        m[8][j] = m[8][-j-1] = m[j][8] = m[-j-1][8] = 0
    m[8][8] = 0
    m[8][6] = m[6][8] = m[-8][8] = 1
    
    # Add version information area for version 7 and above
    if ver > 6:
        # Reserve version information area near bottom-left and top-right finder patterns
        for i in range(6):
            for j in (-9, -10, -11):
                m[i][j] = m[j][i] = 0
                
def place_bits(bits, m):
    """
    Place data bits
    bits: Final data
    m: QR matrix
    """
    bit = (int(i) for i in bits)

    # Data filling direction, starting from bottom right, alternating upward/downward snake pattern
    up = True  # Initial direction is up
    
    # Traverse columns from right to left, processing two columns at a time
    for a in range(len(m)-1, 0, -2):
        a = a-1 if a <= 6 else a
        irange = range(len(m)-1, -1, -1) if up else range(len(m))
        for i in irange:
            for j in (a, a-1):
                if m[i][j] is None:
                    m[i][j] = next(bit)
                    
        # Change direction after processing two columns (up becomes down, down becomes up)
        up = not up
  
def mask(mm_base, data_matrix_to_be_masked):
    """
    Data masking
    mm_base: Base matrix for generating mask patterns (should not contain data bits, usually the state at the end of step 2)
    data_matrix_to_be_masked: Matrix with data already filled, mask will be applied to this matrix (usually the state at the end of step 3)
    return: (Index of best mask, Data matrix with best mask applied)
    """
    # Ensure mm_base is not modified, create a copy
    mm_copy = [row[:] for row in mm_base]
    
    # Get 8 mask patterns
    mask_patterns = get_mask_patterns(mm_copy) # get_mask_patterns should also ensure not to modify its input
    
    # Store score and masked matrix for each mask pattern
    scores = []
    masked_data_matrices = []

    # Try each mask pattern
    for i in range(len(mask_patterns)):
        pattern = mask_patterns[i]
        current_masked_data = [row[:] for row in data_matrix_to_be_masked]
        
        # Apply mask
        for r in range(len(current_masked_data)):
            for c in range(len(current_masked_data[r])):
                # Only apply mask in data area (functional areas already defined in mm_base)
                # And only XOR 1 or 0 in data matrix, not None
                if mm_base[r][c] is None:  # Identify data area
                    if current_masked_data[r][c] is not None:  # Ensure data is filled
                         # Apply mask using XOR operation
                         current_masked_data[r][c] = current_masked_data[r][c] ^ pattern[r][c]
        
        # Calculate score for this mask pattern
        scores.append(compute_score(current_masked_data))
        masked_data_matrices.append(current_masked_data)
    
    # Select mask with lowest (best) score
    best_mask_index = scores.index(min(scores))
    return best_mask_index, masked_data_matrices[best_mask_index]
    
def get_mask_patterns(mm_input):
    """
    Get mask patterns
    mm_input: Base QR matrix (usually the state at the end of step 2, defining functional areas)
              This function should not modify mm_input.
    return: List of 8 mask patterns, each pattern same size as mm_input,
             with 0 or 1 calculated according to mask formula only at positions where mm_input is None (data area).
    """
    mm = [row[:] for row in mm_input]

    # Create mask template, marking data area and functional area
    # Treat None positions in mm as data area, other functional areas remain 0 when generating mask patterns
    data_area_mask_template = [[0] * len(mm[0]) for _ in range(len(mm))]
    for r in range(len(mm)):
        for c in range(len(mm[r])):
            if mm[r][c] is None:  # If it's data area
                data_area_mask_template[r][c] = None  # Mark as position needing mask value calculation
            # Functional areas remain 0 in data_area_mask_template

    # Define 8 mask formulas
    def formula(i, row, column):
        """
        Implement 8 mask formulas defined in QR code standard
        i: Mask pattern index (0-7)
        row, column: Module coordinates
        return: Whether the coordinate needs to be set to 1
        """
        if i == 0:  # (row + column) mod 2 == 0
            return (row + column) % 2 == 0
        elif i == 1:
            return row % 2 == 0
        elif i == 2:
            return column % 3 == 0
        elif i == 3:
            return (row + column) % 3 == 0
        elif i == 4:
            return (row // 2 + column // 3) % 2 == 0
        elif i == 5:
            return ((row * column) % 2) + ((row * column) % 3) == 0
        elif i == 6:
            return (((row * column) % 2) + ((row * column) % 3)) % 2 == 0
        elif i == 7:
            return     (((row + column) % 2) + ((row * column) % 3)) % 2 == 0

    # Generate 8 mask patterns
    mask_patterns_list = []
    for i in range(8):
        # Each mask pattern is based on data_area_mask_template
        pattern = [row[:] for row in data_area_mask_template]
        
        # Calculate mask value for each data area position according to current mask formula
        for r in range(len(pattern)):
            for c in range(len(pattern[r])):
                if pattern[r][c] is None:  # Only calculate mask value in data area
                    pattern[r][c] = 1 if formula(i, r, c) else 0
                # Functional areas remain 0
        
        mask_patterns_list.append(pattern)
        
    return mask_patterns_list
            
def compute_score(m):
    """
    Calculate mask pattern score (lower is better)
    m: QR matrix
    return: Total score (sum of four evaluation criteria)
    """
    def evaluation1(m):
        """
        Evaluation criterion 1: Same color consecutive modules in row/column
        m: QR matrix
        return: Penalty score
        """
        def ev1(ma):
            """
            Calculate penalty for consecutive modules in a single direction (row or column)
            ma: QR matrix (row or column direction)
            return: Penalty score
            """
            sc = 0
            for mi in ma:
                j = 0
                while j < len(mi)-4:
                    n = 4
                    while mi[j:j+n+1] in [[1]*(n+1), [0]*(n+1)]:
                        n += 1
                    (sc, j) = (sc+n-2, j+n) if n > 4 else (sc, j+1)
            return sc
        return ev1(m) + ev1(list(map(list, zip(*m))))
        
    def evaluation2(m):
        """
        Evaluation criterion 2: 2×2 same color blocks
        m: QR matrix
        return: Penalty score
        """
        sc = 0
        for i in range(len(m)-1):
            for j in range(len(m)-1):
                sc += 3 if m[i][j] == m[i+1][j] == m[i][j+1] == m[i+1][j+1] else 0
        return sc
        
    def evaluation3(m):
        """
        Evaluation criterion 3: Specific patterns (patterns similar to finder patterns)
        m: QR matrix
        return: Penalty score
        """
        def ev3(ma):
            """
            Search for specific patterns in rows/columns
            ma: QR matrix (row or column direction)
            return: Penalty score
            """
            sc = 0
            for mi in ma:
                j = 0
                while j < len(mi)-10:
                    if mi[j:j+11] == [1,0,1,1,1,0,1,0,0,0,0]:
                        sc += 40
                        j += 7
                    elif mi[j:j+11] == [0,0,0,0,1,0,1,1,1,0,1]:
                        sc += 40
                        j += 4
                    else:
                        j += 1
            return sc
        return ev3(m) + ev3(list(map(list, zip(*m))))
        
    def evaluation4(m):
        """
        Evaluation criterion 4: Dark module ratio imbalance
        m: QR matrix
        return: Penalty score
        """ 
        darknum = 0
        for i in m:
            darknum += sum(i)
        percent = darknum  / (len(m)**2) * 100
        s = int((50 - percent) / 5) * 5
        return 2*s if s >=0 else -2*s

    # Calculate total score
    score = evaluation1(m) + evaluation2(m) + evaluation3(m) + evaluation4(m)
    return score
    
def add_format_and_version_string(ver, ecl, mask_num, m):
    """
    Add format information and version information
    ver: QR code version (1-40)
    ecl: Error correction level (L/M/Q/H)
    mask_num: Best mask
    m: QR matrix
    """
    # Get format information string corresponding to error correction level and mask pattern
    fs = [int(i) for i in format_info_str[lindex[ecl]][mask_num]]
    for j in range(6):
        m[8][j] = m[-j-1][8] = fs[j]
        m[8][-j-1] = m[j][8] = fs[-j-1]
    m[8][7] = m[-7][8] = fs[6]
    m[8][8] = m[8][-8] = fs[7]
    m[7][8] = m[8][-7] = fs[8]
    
    # Add version information for version 7 and above
    if ver > 6:
        # Get version information bits
        vs = (int(i) for i in version_info_str[ver-7])
        for j in range(5, -1, -1):
            for i in (-9, -10, -11):
                m[i][j] = m[j][i] = next(vs)