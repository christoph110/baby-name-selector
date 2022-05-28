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

No need to install anything. Just unzip the pre-compiled application to the location of your choice, update the user settings (see below) and you are ready to go.

### Configure user settings
Open the `settings.yaml` file and change the configuration to you needs. Replace the user names with your own. Leave the `name` field under `user_2` empty if you want to use the Name Selector as single user. You also can change the keyboard keys to the ones you prefer. The results of your name choices will be saved as .csv file in the `results` folder. Change the name of the `results_file` field to whatever you prefer.

### Executing program
Run the `Name-selector.exe`.
If you run the application for the first time. You will get a welcome message
telling you to add some name lists into the `name_lists` folder. If you do not
have your own name list, you can simply copy one from the `catalog` folder and
paste it into the `name_lists` folder.

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
When running the application from source code, the locations for the name lists, results file and user settings are the following:
- src/name_lists
- src/results
- src/settings.py


## License

This project is licensed under the MIT License - see the LICENSE.txt file for details.
