# 🆔 PAN Card Tampering Detection

A comprehensive computer vision project that detects tampering in PAN cards using **Structural Similarity Index (SSIM)**. This project provides both a standalone Python script and a modern Flask web application with a beautiful, responsive UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [Standalone Python Script](#standalone-python-script)
  - [Flask Web Application](#flask-web-application)
- [How It Works](#how-it-works)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project helps organizations detect whether a PAN card provided by employees, customers, or users is original or tampered. It uses advanced image comparison techniques to calculate the structural similarity between an original PAN card and a user-uploaded PAN card.

### Key Capabilities

- ✅ **Format-Independent**: Supports JPG, JPEG, PNG, WEBP, BMP, GIF, TIFF formats
- ✅ **Accurate Detection**: Uses SSIM algorithm for precise tampering detection
- ✅ **Visual Analysis**: Provides difference maps and threshold images
- ✅ **Modern UI**: Beautiful, responsive web interface
- ✅ **Real-time Processing**: Fast image analysis and comparison

## ✨ Features

### Standalone Script
- Download images from URLs
- Compare original vs tampered images
- Visualize differences with bounding boxes
- Display comprehensive comparison results

### Flask Web Application
- **Modern UI**: Glassmorphism design with smooth animations
- **Drag & Drop**: Easy file upload interface
- **Image Preview**: See uploaded images before processing
- **Multiple Format Support**: Accepts various image formats
- **Visual Results**: 
  - Original vs Uploaded comparison
  - Difference map visualization
  - Threshold image analysis
  - Similarity score with color-coded badges
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Image Modal**: Click images to view in full size

## 🛠 Technology Stack

- **Python 3.8+**: Core programming language
- **Flask 3.1.2**: Web framework
- **OpenCV 4.12.0**: Image processing
- **scikit-image 0.25.2**: Structural Similarity Index (SSIM)
- **Pillow 12.1.0**: Image manipulation
- **NumPy 2.2.6**: Numerical operations
- **imutils 0.5.4**: Image utilities

## 📁 Project Structure

```
PanCard_Tampering_Detection/
│
├── main.py                          # Standalone Python script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── pan_card_tampering/              # Standalone script resources
│   └── image/
│       ├── original.png
│       └── tampered.png
│
└── pan_card_tampering_Flask/        # Flask web application
    ├── app.py                       # Flask application entry point
    ├── config.py                    # Configuration settings
    │
    └── app/
        ├── __init__.py             # Flask app initialization
        ├── views.py                 # Route handlers and image processing
        │
        ├── static/                  # Static files
        │   ├── css/
        │   │   └── style.css        # Custom styles
        │   ├── js/                  # JavaScript files
        │   ├── uploads/             # User uploaded images
        │   ├── original/            # Original PAN card images
        │   └── generated/           # Generated comparison images
        │
        └── templates/
            └── index.html           # Main HTML template
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/PanCard_Tampering_Detection.git
cd PanCard_Tampering_Detection
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import cv2, flask, skimage; print('All packages installed successfully!')"
```

## 📖 Usage

### Standalone Python Script

The standalone script (`main.py`) downloads images from URLs and compares them locally.

#### Step 1: Prepare Your Images

You have two options:

**Option A: Use Default URLs (Already configured)**
- The script downloads images from predefined URLs
- No additional setup needed

**Option B: Use Local Images**
1. Place your original PAN card image in `pan_card_tampering/image/original.png`
2. Place the image to compare in `pan_card_tampering/image/tampered.png`
3. Modify `main.py` to use local files instead of URLs

#### Step 2: Run the Script

```bash
python main.py
```

#### Step 3: View Results

The script will:
1. Download/load images
2. Resize them to a standard size (250x160)
3. Calculate SSIM score
4. Display comparison window with:
   - Original and tampered images side by side
   - Difference map
   - Threshold image
   - SSIM score in console

**Example Output:**
```
Original Image Format : JPEG
Tampered Image Format : PNG
Original Image Size : (250, 160)
Tampered Image Size : (250, 160)
SSIM: 0.87654321
```

#### Customizing the Script

To use local images instead of URLs, modify `main.py`:

```python
# Replace URL downloads with local file loading
original = Image.open("pan_card_tampering/image/original.png")
tampered = Image.open("pan_card_tampering/image/tampered.png")
```

### Flask Web Application

The Flask application provides a web-based interface for PAN card tampering detection.

#### Step 1: Prepare Original Image

1. Place your original PAN card image in `pan_card_tampering_Flask/app/static/original/`
2. Name it `image.jpg`, `image.png`, `image.jpeg`, `image.webp`, or `image.bmp`
3. The application will automatically detect the format

**Example:**
```bash
# Copy your original PAN card image
cp /path/to/your/pan_card.jpg pan_card_tampering_Flask/app/static/original/image.jpg
```

#### Step 2: Configure Application (Optional)

Edit `pan_card_tampering_Flask/config.py` if needed:

```python
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
```

For production, set environment variable:
```bash
export SECRET_KEY='your-production-secret-key'
```

#### Step 3: Run the Flask Application

**Option A: Using app.py (Recommended)**
```bash
cd pan_card_tampering_Flask
python app.py
```

**Option B: Using Flask CLI**
```bash
cd pan_card_tampering_Flask
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

**Option C: Using Python Module**
```bash
cd pan_card_tampering_Flask
python -m flask run
```

#### Step 4: Access the Web Interface

1. Open your web browser
2. Navigate to: `http://127.0.0.1:5000` or `http://localhost:5000`
3. You should see the PAN Card Tampering Detection interface

#### Step 5: Upload and Analyze

1. **Upload Image**: 
   - Click "Choose File" or drag & drop a PAN card image
   - Supported formats: JPG, JPEG, PNG, WEBP, BMP, GIF, TIFF

2. **Process**: 
   - Click "Check for Tampering" button
   - Wait for analysis (usually 1-3 seconds)

3. **View Results**:
   - Similarity score percentage
   - Color-coded badge (Authentic/Suspicious/Tampered)
   - Four comparison images:
     - Original Image
     - Uploaded Image
     - Difference Map
     - Threshold Image

#### Running on Different Port

```bash
# Change port to 8080
flask run --port=8080

# Or in app.py, modify:
# app.run(debug=True, port=8080)
```

#### Running on Network (Access from other devices)

```bash
flask run --host=0.0.0.0
```

Then access from other devices using: `http://YOUR_IP_ADDRESS:5000`

## 🔬 How It Works

### Structural Similarity Index (SSIM)

SSIM measures similarity between two images based on:
1. **Luminance (Brightness)**: Compares overall brightness
2. **Contrast**: Compares difference between dark and light regions
3. **Structure**: Compares patterns, text, and layout

**SSIM Score Interpretation:**
- **0.90 - 1.00**: Very similar (likely authentic) ✅
- **0.70 - 0.89**: Some discrepancies (suspicious) ⚠️
- **0.00 - 0.69**: Significant differences (likely tampered) ❌

### Processing Pipeline

1. **Image Loading**: 
   - Supports multiple formats (PNG, JPG, WEBP, etc.)
   - Format-independent processing using OpenCV

2. **Preprocessing**:
   - Convert to RGB color space
   - Resize to standard dimensions (250x160)
   - Handle transparency (RGBA → RGB with white background)

3. **Comparison**:
   - Convert to grayscale
   - Calculate SSIM score
   - Generate difference map
   - Apply thresholding

4. **Visualization**:
   - Draw bounding boxes around differences
   - Generate comparison images
   - Display results with similarity score

### Why Format-Independent?

The application uses OpenCV's `imread()` and `imdecode()` functions which:
- Read raw pixel data without format-specific color space conversions
- Bypass PIL's format-specific handling (gamma correction, color profiles)
- Ensure PNG and JPG versions of the same image produce identical results

## 📡 API Documentation

### Flask Routes

#### `GET /`
- **Description**: Display the main upload interface
- **Response**: HTML page with upload form

#### `POST /`
- **Description**: Process uploaded PAN card image
- **Request**: 
  - `Content-Type`: `multipart/form-data`
  - `file_upload`: Image file (JPG, PNG, WEBP, etc.)
- **Response**: 
  - HTML page with results
  - `pred`: Similarity score (e.g., "97.58% correct")

### Response Format

```html
<!-- Success Response -->
<div class="results-section show">
  <div class="result-card">
    <!-- Similarity score and visualizations -->
  </div>
</div>

<!-- Error Response -->
<div class="alert alert-danger">
  Error message here
</div>
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional) or set environment variables:

```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
```

### File Paths Configuration

Paths are automatically configured relative to the project root:

- **Uploads**: `pan_card_tampering_Flask/app/static/uploads/`
- **Original Images**: `pan_card_tampering_Flask/app/static/original/`
- **Generated Images**: `pan_card_tampering_Flask/app/static/generated/`

### Image Size Configuration

Default resize dimensions: **250x160 pixels**

To change, modify in `pan_card_tampering_Flask/app/views.py`:

```python
img_bgr_resized = cv2.resize(img_bgr_cv, (250, 160), interpolation=cv2.INTER_LANCZOS4)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. **ModuleNotFoundError: No module named 'cv2'**

**Solution:**
```bash
pip install opencv-python
```

#### 2. **Original image not found**

**Solution:**
- Ensure an image exists in `pan_card_tampering_Flask/app/static/original/`
- Supported names: `image.jpg`, `image.png`, `image.jpeg`, `image.webp`, `image.bmp`
- Check file permissions

#### 3. **Port already in use**

**Solution:**
```bash
# Use a different port
flask run --port=8080

# Or kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill
```

#### 4. **Images not displaying**

**Solution:**
- Check browser console for errors
- Verify static files are being served
- Clear browser cache
- Check file permissions in `static/` directories

#### 5. **Different scores for same image in different formats**

**Solution:**
- This should be fixed in the latest version
- Ensure you're using the updated `views.py` with OpenCV-based processing
- Clear browser cache and try again

#### 6. **Permission Denied errors**

**Solution:**
```bash
# Linux/Mac: Add write permissions
chmod -R 755 pan_card_tampering_Flask/app/static/

# Windows: Run as administrator or check folder permissions
```

### Debug Mode

Enable debug mode for detailed error messages:

```python
# In app.py or config.py
app.run(debug=True)
```

## 🧪 Testing

### Test with Sample Images

1. Use the sample images in `pan_card_tampering_Flask/sample_data/`
2. Copy one to `app/static/original/image.jpg`
3. Upload the other through the web interface

### Manual Testing

```python
# Test image processing function
from app.views import process_image
import cv2

# Test with a sample image
img_bgr, img_pil = process_image('path/to/image.jpg', is_file_path=True)
print(f"Image shape: {img_bgr.shape}")
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Update README.md for new features
- Test thoroughly before submitting PR

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **LuciferCorp** - Initial work

## 🙏 Acknowledgments

- scikit-image team for SSIM implementation
- OpenCV community for excellent image processing tools
- Flask team for the web framework

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## 🔮 Future Enhancements

- [ ] Batch processing support
- [ ] API endpoint for programmatic access
- [ ] Database integration for storing results
- [ ] User authentication
- [ ] Advanced tampering detection algorithms
- [ ] Support for other document types (Aadhaar, Driver's License, etc.)

---

**Made with ❤️ by LuciferCorp**

