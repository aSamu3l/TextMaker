# TextMaker

## Description
TextMaker is a Python application that allows you to create text images using custom fonts and colors. The application supports multiple languages and themes.

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)
- Tkinter (Python GUI toolkit)

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/aSamu3l/TextMaker.git
    cd TextMaker
    ```

2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. The application window will open. You can select the text, font, and color to create your text image.

3. Use the menu options to import new fonts and colors, change the theme, and switch languages.

## Configuration

### Language
You can change the language of the application from the settings menu. The available languages are defined in the `lang.json` file.

### Theme
You can change the theme (Light, Dark, System) from the settings menu. The theme setting is saved in the `settings/setting.json` file.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the `Apache-2.0 License`. See the `LICENSE` file for more details.