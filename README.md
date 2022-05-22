# Name Selector

Small application to make the selection of names (e.g. for babies, pets, etc.) more interactive.

## Description

This program will make choosing names more interactive and fun. Instead of reading through endless lists of names in books etc, you can feed lists of names into the program which then shows you the names one by one and let you decide 'yes' or 'no'. The result is stored in a .csv file which you can then open in e.g. Excel or Numbers to filter for your preferred name selections.

## Getting Started

### Dependencies

Pre-compiled versions available for
* Windows 10

For running the application as source code (see [below](#development-in-local-environment)):
* Python 3.9 (or newer)

### Installing

* TODO: How/where to download your program
* TODO: Any modifications needed to be made to files/folders

### Configure settings
* TODO: settings.yaml

### Executing program

* TODO:

## Development in local environment

### Prerequisites:

* Python 3.9 (or newer)
* virtualenv package (Install with `pip install virtualenv`)

### Installation

1. Move to desired parent directory and clone the repo
    ```
    git clone https://github.com/christoph110/name-selector.git
    ```
2. Move to cloned repository and install virtual environment
    ```
    cd name-selector
    virtualenv venv
    ```
3. Activate virtual environment
(Windows):
    ```
    source venv/Scripts/activate
    ```

4. Install requirements
    ```
    pip install -r requirements.txt
    ```

### Run
```
python src/main.py
```


## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.
