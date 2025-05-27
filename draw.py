# QR Code Drawing Module: Converts QR matrix to visual image, supporting various custom styles

from PIL import Image, ImageDraw, ImageFilter
import os

def draw_qrcode(abspath, qrmatrix, **kwargs):
    """
    Draw QR code with customizable appearance
    
    Parameters:
    abspath: Folder to save the QR code
    qrmatrix: QR matrix
    
    Custom parameters:
    background_color: Background color, default white
    foreground_color: Foreground color, default black
    module_shape: Module shape, options 'square', 'circle', 'diamond'
    border_size: Border size, default 4 units
    unit_size: Size of each module, default 3 pixels
    frame: Whether to add a frame, default True
    margin: Margin size, default 4 units
    filter_name: Image filter, options 'none', 'edge_enhance', 'smooth'
    
    return: Path where QR code is saved
    """
    # Get custom parameters
    background_color = kwargs.get('background_color', 'white')
    foreground_color = kwargs.get('foreground_color', 'black')
    module_shape = kwargs.get('module_shape', 'square')
    border_size = kwargs.get('border_size', 4)
    unit_size = kwargs.get('unit_size', 3)
    frame = kwargs.get('frame', True)
    margin = kwargs.get('margin', 4)
    filter_name = kwargs.get('filter_name', 'none')
    
    # Calculate QR code size
    qr_width = len(qrmatrix)
    total_size = (qr_width + 2 * margin) * unit_size
    
    # Create image
    pic = Image.new('RGB', [total_size, total_size], background_color)
    draw = ImageDraw.Draw(pic)
    
    # Draw each module of the QR code
    for y in range(qr_width):
        for x in range(qr_width):
            if qrmatrix[y][x]:
                # Calculate module coordinates
                x_pos = (x + margin) * unit_size
                y_pos = (y + margin) * unit_size
                
                # Draw module based on selected shape
                if module_shape == 'square':  # Square module
                    draw.rectangle(
                        [x_pos, y_pos, x_pos + unit_size, y_pos + unit_size],
                        fill=foreground_color
                    )
                elif module_shape == 'circle': # Circle module
                    draw.ellipse(
                        [x_pos, y_pos, x_pos + unit_size, y_pos + unit_size],
                        fill=foreground_color
                    )
                elif module_shape == 'diamond': # Diamond module
                    half_unit = unit_size / 2
                    points = [
                        (x_pos + half_unit, y_pos),
                        (x_pos + unit_size, y_pos + half_unit),
                        (x_pos + half_unit, y_pos + unit_size),
                        (x_pos, y_pos + half_unit)
                    ]
                    draw.polygon(points, fill=foreground_color)
    
    # Add frame
    if frame:
        draw.rectangle(
            [0, 0, total_size - 1, total_size - 1],
            outline=foreground_color,
            width=border_size
        )
    
    # Apply filter
    if filter_name != 'none':
        if filter_name == 'edge_enhance':
            pic = pic.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_name == 'smooth':
            pic = pic.filter(ImageFilter.SMOOTH)
    
    # Save image
    saving = os.path.join(abspath, 'qrcode.png')
    pic.save(saving)
    return saving