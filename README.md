# PyDataMatrix

## Overview
PyDataMatrix is a Python library designed to generate and decode Data Matrix barcodes. A Data Matrix barcode is a two-dimensional code composed of black and white "cells" arranged in either a square or rectangular pattern, also known as a matrix. This project aims to facilitate the use and integration of Data Matrix barcodes in various applications, providing essential functions to create and extract information from these codes.

## Features
- Generate Data Matrix barcodes from given data.
- Decode Data Matrix barcodes to retrieve stored data.
- Supports encoding data in multiple modes, including C40, Text, S01, and S02.
- Handles different character sets for flexibility in data encoding.
- Provides visualization and saving of the generated Data Matrix barcode as an image.

## Installation Instructions
### Prerequisites
- Python 3.x
- PIL (Python Imaging Library) or its fork Pillow for image handling

### Installation Steps
1. **Clone the repository:**
    ```sh
    git clone https://github.com/Yuriy/pydatamatrix.git
    cd pydatamatrix
    ```

2. **Install the required dependencies:**
    It's recommended to use a virtual environment to avoid conflicts with other Python packages.
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install pillow
    ```

3. **Verify the installation:**
    You can verify if everything is set up correctly by running:
    ```sh
    python datamatrix.py
    ```

## Usage Examples
Here's a simple example demonstrating the generation and decoding of a Data Matrix barcode using PyDataMatrix:

### Generating a Data Matrix Barcode
```python
import datamatrix

data = "Hello, PyDataMatrix!"
matrix = datamatrix.generate(data)
matrix.save("output.png")  # Save the generated barcode as an image
```

### Decoding a Data Matrix Barcode
```python
import datamatrix

matrix_image = "input.png"  # Path to the image of the Data Matrix barcode
data = datamatrix.decode(matrix_image)
print(f"Decoded data: {data}")
```

## Code Summary
The core functionality of PyDataMatrix is provided in the `datamatrix.py` file. Here is a brief overview of its contents:

### `datamatrix.py`
- **Imports:** Essential libraries for mathematical operations and image handling.
- **Constants:** C40, Text, and other character sets used in encoding.
- **Functions:** 
  - **generate(data):** Generates a Data Matrix barcode from the provided data.
  - **decode(image_path):** Decodes a Data Matrix barcode from an image file to retrieve the stored data.

## Contributing Guidelines
We welcome contributions from the community. Here's how you can contribute:

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
    ```sh
    git clone https://github.com/YOUR-GITHUB-USERNAME/pydatamatrix.git
    ```
3. **Create a new branch** for your feature or bugfix:
    ```sh
    git checkout -b feature-or-bugfix-name
    ```
4. **Make your changes** and commit them:
    ```sh
    git commit -am "Description of changes"
    ```
5. **Push your changes** to your fork:
    ```sh
    git push origin feature-or-bugfix-name
    ```
6. **Create a pull request** on the original repository.

Please ensure your code follows the project's coding guidelines and includes appropriate tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.