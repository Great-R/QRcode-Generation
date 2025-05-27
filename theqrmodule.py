# QR Code Generation Module: Integrates various components to generate complete QR codes

import data, ECC, structure, matrix, draw  # Import modules required for QR code generation
import base64
from PIL import Image  # For image processing
import io

def get_qrcode(ver, ecl, str, save_place, **kwargs):
    """
    Generate QR code
    ver: QR code version (1-40)
    ecl: Error correction level (L/M/Q/H)
    str: String to encode
    save_place: Folder to save QR code
    
    Custom parameters:
    foreground_color: Foreground color, default 'black'
    background_color: Background color, default 'white'
    module_shape: Module shape, options 'square', 'circle', 'diamond', default 'square'
    unit_size: Unit size, default 3
    border_size: Border width, default 4
    margin: Margin, default 4
    frame: Whether to add a frame, default True
    filter_name: Image filter, options 'none', 'edge_enhance', 'smooth', default 'none'
    """

    # Data encoding
    ver, data_codewords = data.encode(ver, ecl, str)

    # Error correction encoding
    ecc = ECC.encode(ver, ecl, data_codewords)
    
    # Structure final data
    final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
    
    # Generate QR matrix
    qrmatrix = matrix.get_qrmatrix(ver, ecl, final_bits)
        
    # Draw QR code and save, passing custom parameters
    return ver, draw.draw_qrcode(save_place, qrmatrix, **kwargs)

def _matrix_to_base64(matrix, scale=10):
    """
    Convert QR matrix to base64 encoded image
    matrix: QR matrix
    scale: Scale factor
    """
    # Calculate image size
    size = len(matrix) * scale
    
    # Create a new white image
    img = Image.new('1', (size, size), 'white')
    
    # Draw QR matrix
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:  # If it's a black module
                for i in range(scale):
                    for j in range(scale):
                        img.putpixel((x * scale + i, y * scale + j), 0)
    
    # Convert image to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{img_str}"

def get_qr_steps(ver, ecl, content):
    """
    Generate steps for QR code creation
    ver: QR code version (1-40)
    ecl: Error correction level (L/M/Q/H)
    content: Content to encode
    
    Returns a list of steps, each step containing an image and description
    """
    steps = []
    
    try:
        # Data encoding - identical to the final QR code generation process
        ver, data_codewords = data.encode(ver, ecl, content)
        
        # Error correction encoding
        ecc = ECC.encode(ver, ecl, data_codewords)
        
        # Structure final data
        final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
        
        # Step 1: Add Finder and Separator
        qrmatrix_step1 = matrix.initialize_qrmatrix(ver)  # Initialize matrix
        matrix.add_finder_and_separator(qrmatrix_step1)  # Add finder patterns and separators
        steps.append({
            'image': _matrix_to_base64(qrmatrix_step1),  # Convert matrix to Base64 image
            'description': '<h3>Step 1: Add Finder Patterns and Separator</h3><p>Finder patterns are added to the three corners of the QR code with separators. These patterns help scanners determine the orientation and size of the QR code.</p>'
        })
        
        # Step 2: Add alignment, Timing patterns and dark module
        qrmatrix_step2 = [row[:] for row in qrmatrix_step1]
        matrix.add_alignment(ver, qrmatrix_step2)  # Add alignment patterns (version 2+)
        matrix.add_timing(qrmatrix_step2)  # Add timing patterns
        matrix.add_dark_and_reserving(ver, qrmatrix_step2)  # Add dark module and reserved areas
        steps.append({
            'image': _matrix_to_base64(qrmatrix_step2),
            'description': '<h3>Step 2: Add Alignment, Timing Patterns and Dark Module</h3><p>Alignment patterns (version 2+), timing patterns, and the dark module are added. These help with orientation, module positioning, and version identification.</p>'
        })
        
        # Step 3: Fill data (encoded data + error correction codes)
        qrmatrix_step3 = [row[:] for row in qrmatrix_step2]
        # Don't pre-fill None as 0, matrix.place_bits will handle None
        matrix.place_bits(final_bits, qrmatrix_step3)  # Place data bits into matrix
        steps.append({
            'image': _matrix_to_base64(qrmatrix_step3),
            'description': f'<h3>Step 3: Fill Data</h3><p>Encoded data and error correction codewords are placed into the matrix, avoiding functional patterns.</p>'
        })
        
        # Step 4: Apply best mask
        # maskmatrix_base is used to generate mask patterns, should be the matrix state at step 2 (containing functional areas, data areas are None or defined as 0)
        maskmatrix_base = [row[:] for row in qrmatrix_step2]  # Copy step 2 matrix for mask base
        # qrmatrix_step3 is the matrix with data already filled, mask will be applied to this matrix
        mask_num, masked_matrix = matrix.mask(maskmatrix_base, qrmatrix_step3)  # Apply best mask
        steps.append({
            'image': _matrix_to_base64(masked_matrix),
            'description': f'<h3>Step 4: Apply Best Mask (Pattern {mask_num})</h3><p>One of 8 mask patterns is applied to the data area to improve scannability. The pattern ({mask_num}) with the best score is chosen.</p>'
        })
        
        # Step 5: Add format and version information
        final_matrix = [row[:] for row in masked_matrix]  # Deep copy of step 4 matrix
        matrix.add_format_and_version_string(ver, ecl, mask_num, final_matrix)  # Add format and version information
        steps.append({
            'image': _matrix_to_base64(final_matrix),
            'description': '<h3>Step 5: Add Format and Version Information</h3><p>Format information (error correction level, mask pattern) and version information (version 7+) are added to complete the QR code.</p>'
        })
            
    except Exception as e:
        print(f"Error in QR steps generation: {e}")  # Print error message
        # Error handling: If error occurs during step generation, use fallback
        try:
            # Try to generate complete QR code directly as fallback for all steps
            ver, data_codewords = data.encode(ver, ecl, content)
            ecc = ECC.encode(ver, ecl, data_codewords)
            final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
            final_qrcode_fallback = matrix.get_qrmatrix(ver, ecl, final_bits)
            fallback_image = _matrix_to_base64(final_qrcode_fallback)
            
            # Use generated complete QR code as image for all steps
            steps = [
                {'image': fallback_image, 'description': '<h3>Step 1: Add Finder Patterns and Separator (Error Fallback)</h3><p>Error during step generation. Displaying final QR code.</p>'},
                {'image': fallback_image, 'description': '<h3>Step 2: Add Alignment, Timing Patterns and Dark Module (Error Fallback)</h3><p>Error during step generation. Displaying final QR code.</p>'},
                {'image': fallback_image, 'description': '<h3>Step 3: Fill Data (Error Fallback)</h3><p>Error during step generation. Displaying final QR code.</p>'},
                {'image': fallback_image, 'description': '<h3>Step 4: Apply Best Mask (Error Fallback)</h3><p>Error during step generation. Displaying final QR code.</p>'},
                {'image': fallback_image, 'description': '<h3>Step 5: Add Format and Version Information (Error Fallback)</h3><p>Error during step generation. Displaying final QR code.</p>'}
            ]
        except Exception as e2:
            print(f"Error in fallback QR steps generation: {e2}")  # Print fallback error message
            return []  # If all attempts fail, return empty list
    
    return steps  # Return generated steps list
