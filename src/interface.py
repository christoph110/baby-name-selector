"""module for the user interface"""
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import BOTH, ttk
import sys
from functions import add_result_to_db
import settings
from settings import UserSettings
from utils import error_message


class NameSelector:
    """class of the Name Selector user interface"""
    def __init__(self) -> None:
        # name list
        self.name_list: list[str]
        self.index = 0
        self.name_item: dict
        # tkinter widgets
        self.counter_label: tk.Label
        self.name_label: tk.Label
        self.sex_label: tk.Label
        self.user1label: tk.Label
        self.user2label: tk.Label
        self.button1yes: tk.Button
        self.button1no: tk.Button
        self.button2yes: tk.Button
        self.button2no: tk.Button
        # initialize window
        self.root = tk.Tk()
        self.set_window()

    def set_new_name(self, name_list: list[str], index: int) -> dict:
        """sets the next name for the user interface"""
        try:
            name, sex = name_list[index].split(';')
            name_item = {
                'name': name,
                'sex': sex,
                'user1_response': '',
                'user2_response': '',
            }
            return name_item
        except IndexError:
            msgbox.showinfo(
                title='Ende',
                message=('No new names left! :)\n\n'
                         'You have already seen all the names in the from '
                         'the name_lists folder. Maybe add some new ones?'))
            self.root.destroy()
            sys.exit()

    def set_window(self):
        """initializes the user interface main window"""
        self.root.title('Name Selector')
        window_width = 600
        window_height = 400
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.root.geometry(f'{window_width}x{window_height}'
                           f'+{center_x}+{center_y}')
        self.root.minsize(window_width, window_height)
        self.root.bind('<KeyPress>', self.keydown)
        self.root.iconbitmap(settings.ICON_PATH)

    def set_frames(self):
        """initializes the different frames in the main window"""
        counterframe = ttk.Frame(self.root)
        self.set_counterlabel(counterframe)
        counterframe.pack(side=tk.TOP, anchor='ne')

        nameframe = ttk.Frame(self.root)
        self.set_namelabel(nameframe)
        self.set_sexlabel(nameframe)
        nameframe.pack(side=tk.TOP, expand=True)

        user1frame = ttk.Frame(self.root)
        self.user1label, self.button1yes, self.button1no = \
            self.set_usernames(user1frame, UserSettings.user1)
        user1frame.pack(side=tk.LEFT, anchor='sw', fill=BOTH, expand=True)

        if UserSettings.two_users:
            user2frame = ttk.Frame(self.root)
            self.user2label, self.button2yes, self.button2no = \
                self.set_usernames(user2frame, UserSettings.user2)
            user2frame.pack(side=tk.LEFT, anchor='se', fill=BOTH, expand=True)

    def set_counterlabel(self, counterframe: ttk.Frame) -> None:
        """initializes the remaining names counter in the main window"""
        self.counter_label = tk.Label(counterframe,
                                      font=('Helvetica', 10),
                                      fg='snow4')
        self.counter_label.pack(ipadx=15, ipady=10)

    def set_namelabel(self, nameframe: ttk.Frame) -> None:
        """initializes the displayed name widget for the selection"""
        self.name_label = tk.Label(nameframe, font=('Helvetica', 40))
        self.name_label.pack(ipadx=10, ipady=10, anchor='center',)

    def set_sexlabel(self, nameframe: ttk.Frame):
        """initializes the sex label below the name"""
        self.sex_label = tk.Label(nameframe, font=('Helvetica', 10))
        self.sex_label.pack(ipadx=10, anchor='center',)

    def set_usernames(self, nameframe: ttk.Frame, user: dict):
        """initializes the user name(s) labels"""
        userlabel = tk.Label(
            nameframe, text=f'{user["name"]}')
        userlabel.pack(padx=32, side=tk.TOP, expand=True, fill='x')
        xsize = 40
        ysize = 15
        buttonyes = tk.Button(
            nameframe,
            text=f'Yes\n({user["yes_button"]})',
            state=tk.DISABLED,
            relief='groove')
        buttonyes.pack(ipadx=xsize,
                       ipady=ysize,
                       padx=10,
                       pady=20,
                       anchor='se',
                       side=tk.LEFT,
                       expand=True)
        buttonno = tk.Button(
            nameframe,
            text=f'No\n({user["no_button"]})',
            state=tk.DISABLED,
            relief='groove')
        buttonno.pack(ipadx=xsize,
                      ipady=ysize,
                      padx=10,
                      pady=20,
                      anchor='sw',
                      side=tk.LEFT,
                      expand=True)

        return userlabel, buttonyes, buttonno

    def run(self, name_list: list[str]) -> None:
        """start the main window"""
        self.name_list = name_list
        self.index = 0
        self.name_item = self.set_new_name(self.name_list, self.index)
        self.update_window()
        self.root.mainloop()

    def keydown(self, event):
        """event handler for keyboard interaction"""
        if event.char in (UserSettings.user1['yes_button'],
                          UserSettings.user1['no_button']):
            if not self.name_item['user1_response']:
                if event.char == UserSettings.user1['yes_button']:
                    print('valid user input: ' + event.char)
                    self.name_item['user1_response'] = 'yes'
                elif event.char == UserSettings.user1['no_button']:
                    print('valid user input: ' + event.char)
                    self.name_item['user1_response'] = 'no'
                if UserSettings.two_users:
                    self.button1yes.config(bg='snow2')
                    self.button1no.config(bg='snow2')
                self.check_user_input()
            else:
                print(f'Invalid input {event.char}. '
                      f'{UserSettings.user1["name"]} already locked in '
                      f"with '{self.name_item['user1_response']}'.")

        elif (event.char in (UserSettings.user2['yes_button'],
                             UserSettings.user2['no_button'])):
            if UserSettings.two_users:
                if not self.name_item['user2_response']:
                    if event.char == UserSettings.user2['yes_button']:
                        print('valid user input: ' + event.char)
                        self.name_item['user2_response'] = 'yes'
                    elif event.char == UserSettings.user2['no_button']:
                        print('valid user input: ' + event.char)
                        self.name_item['user2_response'] = 'no'
                    self.button2yes.config(bg='snow2')
                    self.button2no.config(bg='snow2')
                    self.check_user_input()
                else:
                    print(f'Invalid input {event.char}. '
                          f'{UserSettings.user2["name"]} already locked in '
                          f"with '{self.name_item['user2_response']}'.")

        else:
            print('INVALID user input: ' + event.char)

    def check_user_input(self):
        """validates the user input for different choices"""
        if (self.name_item['user1_response']
                and (self.name_item['user2_response']
                     or not UserSettings.two_users)):
            if self.name_item['user1_response'] == 'yes':
                self.button1yes.config(bg='pale green')
            elif self.name_item['user1_response'] == 'no':
                self.button1no.config(bg='OrangeRed1')
            if UserSettings.two_users:
                if self.name_item['user2_response'] == 'yes':
                    self.button2yes.config(bg='pale green')
                elif self.name_item['user2_response'] == 'no':
                    self.button2no.config(bg='OrangeRed1')

            self.button1no.after(1500, self.next_name)

    def next_name(self):
        """continues with the next name after a selection happened"""
        self.write_to_db()
        self.reset_buttons()
        # next name
        self.index += 1
        self.name_item = self.set_new_name(self.name_list, self.index)
        self.update_name_label()
        self.update_counter_label()

    def write_to_db(self) -> None:
        """saves the selection result in the results file"""
        try:
            add_result_to_db(self.name_item)
        except PermissionError as err:
            error_message(
                title='PermissionError',
                msg=('Could not save to the results file.\n'
                     '\n\nMaybe the file is open in another program?\n'
                     f'{err.args[1]} to access \n{UserSettings.results_file}'))

    def update_window(self) -> None:
        """resets the window elements to the start appearance"""
        self.update_counter_label()
        self.update_name_label()
        self.reset_buttons()

    def update_counter_label(self) -> None:
        """updates the counter of remaining names"""
        self.counter_label.config(
            text=f'{len(self.name_list) - self.index}')

    def update_name_label(self) -> None:
        """updates the name label of the name selection"""
        self.name_label.config(text=self.name_item['name'])
        self.sex_label.config(text=f'({self.name_item["sex"]})')

    def reset_buttons(self) -> None:
        """resets button to the default state"""
        self.name_item['user1_response'] = ''
        self.user1label.config(bg='SystemButtonFace')
        self.button1yes.config(bg='SystemButtonFace')
        self.button1no.config(bg='SystemButtonFace')
        if UserSettings.two_users:
            self.name_item['user2_response'] = ''
            self.user2label.config(bg='SystemButtonFace')
            self.button2yes.config(bg='SystemButtonFace')
            self.button2no.config(bg='SystemButtonFace')
