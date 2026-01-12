# Important imports
from app import app
from flask import request, render_template
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import numpy as np

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original'
app.config['GENERATED_FILE'] = 'app/static/generated'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

    # Execute if request is GET
    if request.method == "GET":
        return render_template("index.html")

    # Execute if request is POST
    if request.method == "POST":
        # Get uploaded image
        file_upload = request.files['file_upload']
        filename = file_upload.filename
        
        # Get file extension and determine format
        file_ext = os.path.splitext(filename)[1].lower()
        supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif']
        
        # Validate file format
        if file_ext not in supported_formats:
            return render_template('index.html', error=f"Unsupported file format: {file_ext}. Please upload: {', '.join(supported_formats)}")
        
        # Helper function to process image consistently - COMPLETELY format-independent
        def process_image(image_input, is_file_path=False):
            """
            Process image consistently regardless of format.
            Returns numpy array in BGR format (for OpenCV) and PIL Image for saving.
            This ensures PNG and JPG of the same image produce IDENTICAL pixel values.
            """
            # CRITICAL: Load image directly using OpenCV first to bypass PIL's format-specific handling
            # OpenCV reads raw pixel data without format-specific color space conversions
            if is_file_path:
                # Read directly with OpenCV (bypasses PIL's color space handling)
                img_bgr_cv = cv2.imread(image_input, cv2.IMREAD_COLOR)
                if img_bgr_cv is None:
                    # Fallback to PIL if OpenCV fails
                    img_pil = Image.open(image_input)
                    img_array = np.array(img_pil)
                    if len(img_array.shape) == 2:
                        img_array = np.stack([img_array] * 3, axis=-1)
                    elif img_array.shape[2] == 4:
                        alpha = img_array[:, :, 3:4] / 255.0
                        rgb = img_array[:, :, :3]
                        white_bg = np.ones_like(rgb) * 255
                        img_array = (rgb * alpha + white_bg * (1 - alpha)).astype(np.uint8)
                    img_bgr_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                # For file objects, read raw bytes and decode with OpenCV
                # This completely bypasses PIL's format-specific color space handling
                image_input.seek(0)  # Reset file pointer
                file_bytes = np.asarray(bytearray(image_input.read()), dtype=np.uint8)
                img_bgr_cv = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                
                if img_bgr_cv is None:
                    # Fallback to PIL if OpenCV decode fails
                    image_input.seek(0)
                    img_pil = Image.open(image_input)
                    img_array = np.array(img_pil, dtype=np.uint8)
                    
                    # Handle different modes
                    if len(img_array.shape) == 2:
                        img_array = np.stack([img_array] * 3, axis=-1)
                    elif img_array.shape[2] == 4:
                        # RGBA - convert to RGB with white background
                        alpha = img_array[:, :, 3:4].astype(np.float32) / 255.0
                        rgb = img_array[:, :, :3].astype(np.float32)
                        white_bg = np.ones_like(rgb) * 255.0
                        img_array = (rgb * alpha + white_bg * (1 - alpha)).astype(np.uint8)
                    elif img_array.shape[2] == 2:
                        img_array = np.stack([img_array[:, :, 0]] * 3, axis=-1)
                    
                    # Ensure exactly 3 channels
                    if img_array.shape[2] != 3:
                        img_array = img_array[:, :, :3]
                    
                    # Convert RGB to BGR for OpenCV
                    img_bgr_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # CRITICAL: Now resize using OpenCV's INTER_LANCZOS4 for pixel-perfect consistency
            # This ensures both PNG and JPG are resized identically
            img_bgr_resized = cv2.resize(img_bgr_cv, (250, 160), interpolation=cv2.INTER_LANCZOS4)
            
            # Convert back to RGB for PIL (for saving)
            img_rgb_resized = cv2.cvtColor(img_bgr_resized, cv2.COLOR_BGR2RGB)
            img_pil_resized = Image.fromarray(img_rgb_resized, mode='RGB')
            
            return img_bgr_resized, img_pil_resized
        
        # Process uploaded image
        try:
            uploaded_bgr, uploaded_pil = process_image(file_upload, is_file_path=False)
            # Save for display purposes only
            uploaded_pil.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'), 'JPEG', quality=100, optimize=False)
        except Exception as e:
            return render_template('index.html', error=f"Error processing uploaded image: {str(e)}")

        # Find original image file (support multiple formats)
        original_file_path = None
        original_formats = ['image.jpg', 'image.jpeg', 'image.png', 'image.webp', 'image.bmp']
        
        for orig_format in original_formats:
            potential_path = os.path.join(app.config['EXISTNG_FILE'], orig_format)
            if os.path.exists(potential_path):
                original_file_path = potential_path
                break
        
        if not original_file_path:
            return render_template('index.html', error="Original image not found. Please ensure an image file exists in the original folder.")
        
        # Process original image using the same function
        try:
            original_bgr, original_pil = process_image(original_file_path, is_file_path=True)
            # Save for display purposes only
            original_pil.save(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'), 'JPEG', quality=100, optimize=False)
        except Exception as e:
            return render_template('index.html', error=f"Error processing original image: {str(e)}")

        # Use the processed numpy arrays directly (no JPEG compression artifacts)
        original_image = original_bgr.copy()
        uploaded_image = uploaded_bgr.copy()
        
        # Verify images are the same size
        if original_image.shape != uploaded_image.shape:
            return render_template('index.html', error=f"Image size mismatch. Original: {original_image.shape}, Uploaded: {uploaded_image.shape}")

        # Convert image into grayscale
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
        
        # CRITICAL: Ensure both grayscale images are identical in data type
        # Use uint8 to match what structural_similarity expects by default
        # This ensures format consistency while maintaining compatibility
        original_gray = original_gray.astype(np.uint8)
        uploaded_gray = uploaded_gray.astype(np.uint8)

        # Calculate structural similarity
        # data_range=255 specifies the range of pixel values (0-255 for uint8)
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True, data_range=255)
        diff = (diff * 255).astype("uint8")

        # Calculate threshold and contours
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # Draw contours on image
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save all output images (if required)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
        
        return render_template('index.html', pred=str(round(score*100,2)) + '%' + ' correct')

       
# Main function
if __name__ == '__main__':
    app.run(debug=True)
