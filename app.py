from flask import Flask, render_template, request, jsonify, send_file, url_for
import os
import time
import theqrmodule # Import custom QR code generation module
import base64

app = Flask(__name__) # Create Flask application instance

# Define the storage folder for generated QR code images
GENERATED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'generated')

# Ensure the generated folder exists
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Website entry point, renders index.html template when accessing the root URL
@app.route('/')
def index():
    """Render the homepage"""
    # Get the URL for the background image
    header_bg_url = url_for('static', filename='header-bg.jpg')
    return render_template('index.html', header_bg_url=header_bg_url)

# QR code generation API endpoint, called when user submits the form
@app.route('/generate', methods=['POST'])
def generate_qrcode():
    """API endpoint: Generate QR code"""
    try:
        # Get form data
        content = request.form.get('content', '') # QR code content
        if not content:
            return jsonify({'success': False, 'error': 'Please enter content'}), 400
        
        # Get error correction level
        ecl = request.form.get('ecl', 'L') # Default is L level
        if ecl not in ['L', 'M', 'Q', 'H']:
            ecl = 'L' 
        
        # Get version number, if not specified or invalid, version is automatically selected
        try:
            version = int(request.form.get('version', '0')) # 0 means auto-select version
            if version < 0 or version > 40: # Version range 1-40, 0 means auto
                version = 0 
        except ValueError:
            version = 0 
        
        # Get custom appearance parameters
        foreground_color = request.form.get('foreground_color', 'black') # Foreground color
        background_color = request.form.get('background_color', 'white') # Background color
        module_shape = request.form.get('module_shape', 'square') # Module shape
        if module_shape not in ['square', 'circle', 'diamond']:
            module_shape = 'square' # Default is square
            
        # Get custom size and border parameters
        try:
            unit_size = int(request.form.get('unit_size', '3')) # Pixel size of each module
            if unit_size < 1 or unit_size > 10:
                unit_size = 3 
        except ValueError:
            unit_size = 3
            
        try:
            border_size = int(request.form.get('border_size', '4')) # Border size (space from QR code to image edge)
            if border_size < 0 or border_size > 10: # In draw.py this is actually quiet_zone
                border_size = 4 
        except ValueError:
            border_size = 4
            
        try:
            margin = int(request.form.get('margin', '4')) # Internal margin when drawing QR code
            if margin < 0 or margin > 10:
                margin = 4 
        except ValueError:
            margin = 4
        
        # Get whether to add extra frame (at drawing level)
        frame = request.form.get('frame', 'true').lower() == 'true'
        
        # Get image filter
        filter_name = request.form.get('filter_name', 'none') # Image filter name
        if filter_name not in ['none', 'blur', 'edge_enhance', 'smooth']:
            filter_name = 'none' # Default is no filter
        
        # Generate unique filename
        timestamp = int(time.time())
        filename = f"qrcode_{timestamp}.png"
        # save_path = os.path.join(GENERATED_FOLDER, filename) # save_path is handled in theqrmodule
        
        # Call QR code generation module, passing custom parameters
        ver, qrcode_path = theqrmodule.get_qrcode(
            version, 
            ecl, 
            content, 
            GENERATED_FOLDER, # Pass the save folder path
            foreground_color=foreground_color,
            background_color=background_color,
            module_shape=module_shape,
            unit_size=unit_size,
            border_size=border_size, # This border_size corresponds to quiet_zone in draw.py
            margin=margin,           # This margin corresponds to margin in draw.py
            frame=frame,
            filter_name=filter_name
        )
        
        # Read the generated image and convert to base64 for direct display on the webpage
        with open(qrcode_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Return results
        return jsonify({
            'success': True, 
            'version': ver, # Return the actual version used
            'image_base64': f"data:image/png;base64,{encoded_string}", # Base64 encoded image data
            'image_url': url_for('static', filename=f'generated/{os.path.basename(qrcode_path)}') # Image download URL
        })
    
    except Exception as e:
        # Catch exceptions and return error message
        return jsonify({'success': False, 'error': str(e)}), 500

# API endpoint to get QR code creation steps
@app.route('/get_qr_steps', methods=['POST'])
def get_qr_steps():
    """API endpoint: Get QR code creation steps"""
    try:
        # Get form data
        content = request.form.get('content', '') # QR code content
        if not content:
            return jsonify({'success': False, 'error': 'Please enter content'}), 400
        
        # Get error correction level
        ecl = request.form.get('ecl', 'L') # Default is L level
        if ecl not in ['L', 'M', 'Q', 'H']:
            ecl = 'L' 
        
        # Get version number, if not specified or invalid, version is automatically selected
        try:
            version = int(request.form.get('version', '0')) # 0 means auto-select version
            if version < 0 or version > 40:
                version = 0
        except ValueError:
            version = 0
        
        # Call QR code steps generation function
        steps = theqrmodule.get_qr_steps(version, ecl, content)
        
        # Return results
        return jsonify({
            'success': True, 
            'steps': steps # List containing step descriptions and images
        })
    
    except Exception as e:
        # Catch exceptions and return error message
        return jsonify({'success': False, 'error': str(e)}), 500

# API endpoint to download generated QR code image, called when user clicks download button
@app.route('/download/<filename>')
def download_file(filename):
    """Download generated QR code image"""
    try:
        # Send file for download
        return send_file(os.path.join(GENERATED_FOLDER, filename), as_attachment=True)
    except Exception as e:
        # If file not found or other error occurs, return 404 or error message
        return jsonify({'success': False, 'error': str(e)}), 404

# Application startup configuration
if __name__ == '__main__':
    # Start Flask application, listen on all network interfaces on port 5002, and enable debug mode
    app.run(host='0.0.0.0', port=5002, debug=True)
