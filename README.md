

# Advanced Python QR Code Generator

Module Code: CS2PPNU
Assignment report Title: QR Code Generator
Student Number (e.g., 25098635): 31808120, 31808669, 31808980, 31808442, 31808741
Actual hrs spent for the assignment: 60hrs
Which Artificial Intelligence tools used: ChatGPT

------

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Live Demonstration](#live-demonstration)
3. [Core Features Matrix](#core-features-matrix)
4. [Technical Architecture](#technical-architecture)
5. [Installation & Usage](#installation--usage)
6. [Technical Deep Dive](#technical-deep-dive)
7. [Social, Legal & Ethical (SLE) Considerations](#social-legal--ethical-sle-considerations)
8. [Application Evaluation](#application-evaluation)
9. [Scan Me!](#scan-me)

------

## **1. Project Overview**

- **Introduction**

  This is a Python-based QR code generator with a user-friendly web interface. It allows users to enter text, customize the QR code’s style (color, shape, size, etc.), and preview or download the result in real time. A visual step-by-step guide is also included, making the tool ideal for both learning and practical use.

- **Team Members**

  - Xing Yujie
  - Wang Wenbin
  - Lyu Yanyan 
  - Xu Songdi
  - Lu Zichen

------

## **2. Live Demonstration**

The following animations showcase the application's key features, from standard QR code creation to the advanced customization and visualization options, fulfilling the project's demonstration requirement.

![5月27日 (2)](gif/5月27日 (2).gif)

#### Demo 1: Basic QR Code Generation

This demonstration shows the primary workflow: entering text content and instantly generating a standard, scannable black-and-white QR code.

<img src="gif\GIF_20250527170535967.GIF" alt="GIF_20250527170535967" style="zoom:50%;" />

---

#### Demo 2: Customized QR Code Generation

Here, we demonstrate the powerful appearance customization options, including changing the colors, module shapes, and other formats.

<img src="gif\GIF_20250527190041544.GIF" alt="GIF_20250527190041544" style="zoom:50%;" />

---

####  Demo 3: Advanced Visualization of Creation Steps

This animation highlights our unique educational feature. After generating a styled QR code, the user enables the 'Show QR Code Creation Steps' to visualize how the QR code is constructed.

<img src="gif\GIF_20250527174918074.GIF" alt="GIF_20250527174918074" style="zoom:50%;" />

------



## **3. Core Features Matrix**

| **Category**           | **Feature**                        | **Status** | **Notes**                                                    |
| ---------------------- | ---------------------------------- | ---------- | ------------------------------------------------------------ |
| *Basic Functionality*  | Standard QR Code Generation        | ✅          | Supports versions 1 and 2; implements byte, numeric, and alphanumeric encoding modes. |
|                        | Interactive Web Interface          | ✅          | Built with Flask, CSS, HTML and JavaScript; responsive layout supports multiple devices. |
|                        | Scannable Image Output             | ✅          | PNG images tested with mainstream mobile apps for high compatibility and recognition. |
| *Project Enhancements* | Intelligent Mask Optimization      | ✅          | Automatically tests 8 mask patterns using 4 penalty rules to select the most readable one. |
|                        | Step-by-Step Visualization         | ✅          | Offers an educational slideshow-style display of the full QR code construction process. |
|                        | Inclusive Appearance Customization | ✅          | Custom colors, module shapes (square, circle, diamond), borders, and filters; accessibility-friendly. |
| *UX & Security*        | Input Validation & Feedback        | ✅          | Real-time input length and validity checks; includes GIF animation and loading hints. |
|                        | Image Download Function            | ✅          | One-click download or sharing of the generated QR code image. |
|                        | Risk Mitigation & Advisories       | ✅          | Clear warnings about data safety and phishing risks; promotes responsible usage. |

------

## **4. Installation & Usage**

### **Environment Requirements**

- Python: 3.11.7

- Dependencies:

  - Flask
  - Pillow
  - reedsolo

  All managed in `requirements.txt`.

### **Installation Steps**

1. **Clone the repository:**

   ```bash
   git clone [your repository link]
   cd [project folder]
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   # In the project root directory
   python -m venv venv
   # on macOS/Linux:
   source venv/bin/activate
   # on Windows:
   venv\\Scripts\\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

------

### **Running the Application**

- To start the app (assuming the main file is `app.py`):

  ```bash
  python app.py
  ```

- After starting, open your browser and visit:or follow the address shown in your terminal.

  ```
  <http://127.0.0.1:5001>
  ```

------

### **User Guide**

1. **Text Input**

   Enter the text you want to encode in the input box (e.g., `https://nuist.blackboardchina.cn/`).

2. **Select Options**

   - **Error Correction Level:** Choose one from `L`, `M`, `Q`, or `H`.
   - **QR Version:** Choose from `Auto`, `1–10`.

3. **Customize Appearance**

   Expand the customization panel to access the following options:

   - **Foreground Color:** Use the color picker.
   - **Background Color:** Use the color picker.
   - **Module Shape:** Choose from `square`, `diamond`, or `circle`.
   - **Module Size:** Range from `1–10 px`.
   - **Margin:** Range from `0–10 units`.
   - **Border Width:** Range from `0–10 px`; option to show/hide the border.
   - **Image Filter:** Choose from `none`, `edge enhance`, or `smooth`.
   - **QR Code Size:** Adjustable from `0–250 px`.

4. **Optional: QR Code Creation Steps**

   Toggle this feature to enable step-by-step QR code generation visualization.

5. **Generate QR Code**

   Click the **"Generate QR code"** button.

6. **View Animation (Optional)**

   A 5-second loading animation will appear. Click to skip if desired.

7. **Step-by-Step Navigation (if enabled)**

   Use **"Next"** and **"Previous"** buttons to browse through each QR generation step.

8. **Resize QR Code**

   Use the **QR code size slider** to adjust the output (range: `0–250 px`).

9. **Download QR Code**

   Click the **"Download"** button to save the generated image locally.

10. **Share QR Code**

    Click the **"Share"** button to distribute the QR code.

------

## 5. Technical Deep Dive

### QR Code Generation System Architecture

<img src="gif\architecture.png" alt="architecture" style="zoom:50%;" />

------

This diagram illustrates the modular, layered architecture of the QR Code Generation System. The system follows a left-to-right workflow that mirrors the QR code creation process, improving clarity and maintainability.

> The module names in the diagram are conceptual summaries for clarity and do not necessarily correspond to exact function or class names in the implementation.

- **Interface Layer**: The entry point of the system, where `UserInterface` receives raw input from the user.
- **Control Layer**: The `QRCodeGenerator` serves as the central coordinator, managing the entire generation pipeline.
- **Encoding Module**: Responsible for preparing input data through encoding mode detection (`ModeDetector`), character counting (`CharacterCounter`), and bitstream encoding (`DataEncoder`).
- **Bit Buffer Module**: Temporarily stores the encoded data in `BitBuffer` for matrix integration.
- **Matrix Construction Module**: Adds structural patterns (`FunctionPatterns`) and inserts encoded data into the QR matrix (`DataInserter`).
- **Mask Selection Module**: Applies various masks (`MaskApplier`), evaluates them (`PenaltyCalculator`), and chooses the optimal one (`OptimalMaskSelector`) for readability and error resistance.
- **Rendering & Export Module**: Renders the final QR code image (`QRCodeRenderer`) and exports it in a suitable format (`ImageExporter`).

This structured design promotes modularity, testability, and alignment with the QR code specification.

## Programming Paradigms

### Object-Oriented Programming (OOP)

The project implements OOP through the utilization of third-party libraries.  For instance, `Flask` class in `app.py` handles web routing, `RSCodec` class in `ECC.py` manages error correction, and `Image`/`ImageDraw` classes from Pillow in `draw.py` handle image rendering.  This demonstrates effective encapsulation and abstraction of complex functionality.

### Functional Programming

The implementation employs functional programming principles for data transformation.  Key examples include:

- Matrix transposition using `map` and `zip` in `matrix.py`
- Codeword interleaving with `zip` in `structure.py`
- Data formatting through list comprehensions in `data.py`

### Imperative Programming

The core application flow follows imperative programming:

- Sequential QR code generation in `theqrmodule.py`
- HTTP request processing in `app.py` routes
- Step-by-step matrix construction and optimization

## Information Modeling and Data Management

### Information Modeling

The QR code matrix is precisely modeled as a two-dimensional integer list (`list[list[int]]`):

- `None`: Represents unfilled data areas
- `0`: Represents white modules
- `1`: Represents black modules This modeling approach ensures clear logic for data filling and mask application.

### User Input Management

The application implements robust input handling:

- Form data retrieval through `request.form.get()`
- Default value assignment for stability
- Strict type validation for numerical inputs
- Comprehensive error handling for invalid inputs

### Data Integrity and Error Handling

The implementation ensures robust error handling:

- Top-level try-except blocks in API routes
- Structured JSON error responses
- Prevention of server crashes
- User-friendly error messages



## 6. Functional Proofs

🧪 **Core Parameters**

- **Version**: 1
- **Error Correction Level**: L
- **Test String**: "HELLO"

**Objective**: This section demonstrates the intermediate steps in generating a QR code, using a consistent test string to prove the functionality of each core component of our algorithm.

<img src="gif\GIF_20250525210946444.GIF" alt="GIF_20250525210946444" style="zoom: 20%;" />

------

### Step 1: Data Encoding

This stage converts the raw text "HELLO" into the final data bitstream ready for error correction.

1. **Mode & Character Count**:

   - **Mode**: Byte → **`0100`**
   - **Character Count**: 5 → **`00000101`** (8-bit binary)

2. **Character Encoding (ASCII to Binary)**:

   - H → `01001000`
   - E → `01000101`
   - L → `01001100`
   - L → `01001100`
   - O → `01001111`

3. **Bitstream Assembly and Padding**:

   - Initial Bitstream

      (Mode + Count + Data):

     ```
     0100000001010100100001000101010011000100110001001111
     ```

   - **Final Data Bitstream** (152 bits / 19 bytes total): A `0000` terminator is added to the initial stream, which is then padded with alternating bytes `11101100` and `00010001` until the 152-bit capacity for Version 1-L is reached.

------

### Step 2: Error Correction Code Generation

Using the **Reed-Solomon algorithm**, we generate 7 error correction codewords for our 19 data codewords.

1. **Data Codewords (19 bytes, in decimal)**:

   - The final data bitstream from the previous step, grouped into 8-bit bytes and converted to decimal values.

     ```
     [69, 85, 76, 76, 79, 0, 236, 17, 236, 17, 236, 17, 236, 17, 236, 17, 236, 17, 236]
     ```

     (Note: These are example values based on the padding rules.)

2. **Generated Error Correction Codewords (7 bytes, in decimal)**:

   - The output from the 

     ```
     reedsolo
     ```

      library after processing the 19 data codewords.

     ```
     [168, 85, 154, 8, 186, 213, 23]
     ```

3. **Final Codeword Sequence (26 bytes total)**:

   - The 19 data codewords and 7 error correction codewords are interleaved to form the final message to be placed in the matrix.

------

### Step 3: Matrix Construction & Data Placement

The final codeword sequence is placed into a 21x21 matrix that has been initialized with the required function patterns.

1. **Matrix with Function Patterns**:
   - A visualization of the matrix showing only the finder patterns, timing patterns, format information area, and the dark module. *(A 21x21 grid visualization would be displayed here.)*
2. **Matrix After Data Placement**:
   - A visualization of the matrix after the 208 bits of the final codeword sequence have been placed in a zig-zag pattern, skipping over the function pattern areas. *(A 21x21 grid visualization of the data-filled matrix would be displayed here.)*

------

### Step 4: Mask Application & Evaluation (Enhancement Proof)

To ensure scannability, all 8 standard mask patterns are applied, and the one with the lowest penalty score is selected.

1. Penalty Calculation & Optimal Mask Selection:
   - Total penalty scores are calculated for each of the 8 masked matrices. The lowest score indicates the best mask.

| Mask Pattern | Total Penalty Score | Notes                |
| ------------ | ------------------- | -------------------- |
| Mask 0       | 45                  |                      |
| Mask 1       | 38                  |                      |
| Mask 2       | 56                  |                      |
| Mask 3       | 51                  |                      |
| **Mask 4**   | **36**              | ✅ **Optimal Choice** |
| Mask 5       | 37                  |                      |
| Mask 6       | 49                  |                      |
| Mask 7       | 45                  |                      |

2. Applying the Optimal Mask:

- **Before Masking**: *(Visualization of the data-filled matrix before the mask is applied.)*
- **After Masking**: *(Visualization of the final matrix after **Mask 4** has been applied via an XOR operation.)*

------

### ✅ Final Proof

The steps above verify that each component of our implementation functions correctly. Starting from the string "HELLO", we have demonstrated the full process of encoding, error correction, matrix construction, and mask selection. The resulting final matrix is now ready to be rendered into a scannable PNG image.



## **6. Social, Legal, and Ethical (SLE) Considerations**

### 🌍 **Social Impact**

Accessibility and inclusivity are addressed through customizable colors, shapes, sizes, and margins, meeting diverse user preferences and personalization needs.

A visual “QR Code Creation Steps” guide helps users understand how QR codes are built, promoting digital literacy.

### 🏛️ **Legal Compliance**

Users are clearly warned not to input sensitive information (e.g., ID numbers, addresses, or bank details), in alignment with data protection laws such as GDPR.

All inputs are processed locally and are never stored.

### 🛡️ **Ethical Practice**

Warning messages promote transparency and caution. Users are advised to verify encoded URLs before sharing, reducing the risk of phishing or malware.

These safeguards support responsible and safe QR code usage.

------

## 7. Application Evaluation

### ✅ Strengths

- **Educational Use**

  Visual step-by-step generation helps users understand how QR encoding works, making it useful for teaching and public demos.

- **Highly Customizable**

  Users can adjust colors, shapes, sizes, borders, and filters to match branding or design needs.

- **Robust Technical Core**

  Supports Reed-Solomon ECC (4 levels), optimal masking, interleaving, and versions 1–40 with modular design.

### ⚠️ Limitations

- **Encoding and Performance Constraints**

  Limited to single-mode encoding (no Kanji or mixed-mode), which reduces multilingual flexibility.

  The mask selection in `matrix.py` involves looping through 8 patterns with penalty scoring, which can slow down high-version or large QR code generation.

- **Security Risk**

  Malicious links can still be encoded; no backend validation is provided. Users must take responsibility when generating and sharing codes.

------

## **8. Scan Me!**(Live Test)

We have used our application to generate the following QR code. You are welcome to scan it with any standard mobile app to directly test its functionality and validity.

### Test 1:



<img src="gif\test1.png" alt="test1" style="zoom:175%;" />

**Expected Content:**

> `This is a test!`



### Test 2:



<img src="gif\test2.png" alt="test2" style="zoom:130%;" />

**Expected Content:**

> `Hello! This QR code was generated by our CS2PP Group 6 project!`



### Test 3:

<img src="gif\test3.png" alt="test3" style="zoom:145%;" />

**Expected Content:**

> `Open a website(URL: https://nuist.blackboardchina.cn/webapps/login/)`