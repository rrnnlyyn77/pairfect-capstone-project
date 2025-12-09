
# About this Project
Pairfect is an online application that helps people make safer and smarter skincare decisions. The project will examine the compatibility of active ingredients versus using multiple products together, as most existing apps and tools do not consider compatibility when products are used together in their functionality. 

This lightweight web application can be utilized by users to determine the compatibility of the active ingredients within their current skincare products. This compatibility evaluation will be done using a research-based table for evaluating ingredient combinations and will provide a user-friendly output, including an overall Synergy Score and rationale.

The application supports:
- Manual ingredient entry (fully functional on deployment)
- OCR ingredient extraction (functional only in local environments)
<br> Due to hosting limitations, OCR is disabled on deployed versions, but works when running the app locally.

# Features
1. Ingredient Synergy Analysis
- Performs pairwise compatibility checks between all selected active ingredients.
- Uses a dermatology-informed compatibility table.
- Generates:
  - Synergy score (0–100)
  - Good pair list
  - Bad pair list
  - Written explanation
2. Manual Ingredient Entry
- Users select product type and active ingredient.
- Supports up to ten products per evaluation.
3. OCR-Based Ingredient Extraction (Local Version Only)
- Preprocessing using OpenCV
- Text extraction using EasyOCR
- Regex-based ingredient matching
- Normalization of detected ingredient names
4. Skincare Literacy Pages
- Skin type information
- Ingredient descriptions
- Ingredient compatibility visual references
5. Clean and Responsive Interface
- Minimalistic layout
- Clear navigation
- Mobile-friendly styling

# System Architecture
1. Frontend
- HTML5: used for page structure.
- CSS3: manages layout design, page styling, and visual components.
- JavaScript: handles minor dynamic elements (if used).
- Jinja2 Templates: integrates Python with HTML to render dynamic content.
2. Backend
Python 3.10+
- Flask: used as the primary web framework for routing, session handling, and template rendering.
- EasyOCR: handles text extraction from preprocessed images.
- OpenCV: performs image preprocessing (grayscale conversion, thresholding, sharpening).
- NumPy: used for image matrix operations.
- Regular Expressions (re module): used for text cleaning and ingredient pattern matching.
3. OCR Pipeline (Local Only)
- Image preprocessing
  - Grayscale conversion
  - Histogram equalization
  - Adaptive thresholding
  - Sharpening
- OCR extraction via EasyOCR
- Ingredient matching via regex patterns
- Selection of first detected active ingredient

# Installation and Setup
1. Clone Repository _(preferrably using GitHub Desktop)_
- 'git clone https://github.com/rrnnlyyn77/pairfect-capstone-project'
- 'cd Pairfect' 
2. Create and activate virtual environment _(this ensures that the dependencies area isolated)_
- 'python -m venv venv'
3. Activate the environment
- (For Windows users)
  - 'venv\Scripts\activate'
- (For Mac/Linux users)
  - 'source venv/bin/activate'
4. Install dependencies _(Install all required Python packages using the provided requirements.txt file)_
- 'pip install -r requirements.txt'
5. Run the application _(start the Flask server)_
- 'python app.py'
6. Access through your browser
- 'http://127.0.0.1:5000/'

# Project Structure
Pairfect/ <br>
│── app.py                               _(Main Flask application)_ <br>
│── pairfect_ocr.py                      _(OCR pipeline (local-only feature))_ <br>
│── requirements.txt                     _(Python dependencies)_  <br>
│── README.md                            _(Project documentation)_  <br>
│  <br>
├── static/                              _(Frontend assets)_  <br>
│   ├── css/                             _(Stylesheets)_  <br>
│   ├── js/                              _(JavaScript files)_  <br>
│   ├── images/                          _(App images and illustrations)_  <br>
│   └── uploads/                         _(Temporary uploaded images (OCR))_  <br>
│  <br>
└── templates/                           _(HTML templates for each page)_  <br>
    ├── base.html  <br>
    ├── landing.html  <br>
    ├── options.html  <br>
    ├── manual_entry.html  <br>
    ├── upload_image.html  <br>
    ├── results.html  <br> 
    ├── skintypes.html  <br>
    ├── ingredients.html  <br>
    └── combos.html  <br>

# Notes on deployment
_The application is deployable on Render, but with modifications._

What Works on Deployment:
- All manual ingredient features
- Synergy score computation
- Ingredient literacy pages
- Navigation and UI system

What Does Not Work on Deployment:
- OCR-based ingredient extraction is not supported due to:
- Lack of GPU acceleration
- EasyOCR library restrictions
- Render's container environment limiting heavy OpenCV processing
- File system access constraints for image manipulation

_*The OCR pipeline should be used locally only. A future version may migrate OCR to a cloud-based GPU service or API-based OCR alternative*_

# Security and Privacy
- No user accounts or databases are used.
- All inputs are handled via temporary sessions.
- Data is cleared after generating results.
- No personally identifiable information is collected.
- If deployed clinically or commercially, compliance with the New Zealand Privacy Act, GDPR, or HIPAA would require encryption, anonymisation, and a privacy impact assessment.

# Acknowledgements
This project makes use of the following tools and resources:
- Flask
- OpenCV
- EasyOCR
- Dermatology research sources used for building the compatibility matrix
- UI inspiration from modern skincare applications

# Author
Ronalyn Ruaro <br>
Bachelor of Software Engineering <br>
Yoobee Colleges <br>

# External Links
- Repository link: https://github.com/rrnnlyyn77/pairfect-capstone-project
- Deployment link _( via Render)_: https://pairfect-application-ii.onrender.com
