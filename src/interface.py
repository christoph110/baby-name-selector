
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
import sys
from functions import add_result_to_db
import settings
from settings import UserSettings


class NameSelector:

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
        try:
            name, sex = name_list[index].split(";")
            name_item = {
                "name": name,
                "sex": sex,
                "user1_response": "",
                "user2_response": "",
            }
            return name_item
        except IndexError:
            msgbox.showinfo(title='Ende', message='No names left! :)')
            self.root.destroy()
            sys.exit()

    def set_window(self):
        self.root.title("Name Selector")
        window_width = 600
        window_height = 400
        # get the screen dimension
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.root.geometry(f"{window_width}x{window_height}"
                           f"+{center_x}+{center_y}")
        self.root.bind("<KeyPress>", self.keydown)
        self.root.iconbitmap(settings.ICON_PATH)

    def set_frames(self):
        counterframe = ttk.Frame(self.root)
        self.set_counterlabel(counterframe)
        counterframe.pack(side=tk.TOP, anchor="ne")

        nameframe = ttk.Frame(self.root)
        self.set_namelabel(nameframe)
        self.set_sexlabel(nameframe)
        nameframe.pack(side=tk.TOP, expand=True)

        userframe = ttk.Frame(self.root)
        self.set_usernames(userframe)
        userframe.pack(side=tk.TOP)

        buttonframe = ttk.Frame(self.root)
        self.set_buttons(buttonframe)
        buttonframe.pack(side=tk.TOP)

    def set_counterlabel(self, counterframe: ttk.Frame) -> None:
        self.counter_label = tk.Label(counterframe,
                                      font=("Helvetica", 10),
                                      fg="snow4")
        self.counter_label.pack(ipadx=15, ipady=10)

    def set_namelabel(self, nameframe: ttk.Frame) -> None:
        self.name_label = tk.Label(nameframe, font=("Helvetica", 40))
        self.name_label.pack(ipadx=10, ipady=10, anchor="center",)

    def set_sexlabel(self, nameframe: ttk.Frame):
        self.sex_label = tk.Label(nameframe, font=("Helvetica", 10))
        self.sex_label.pack(ipadx=10, anchor="center",)

    def set_usernames(self, userframe: ttk.Frame):
        self.user1label = tk.Label(
            userframe, text=f"{UserSettings.user1['name']}")
        self.user1label.pack(ipadx=10,
                             padx=(5, 120),
                             anchor="center",
                             side=tk.LEFT,
                             expand=True)
        self.user2label = tk.Label(
            userframe, text=f"{UserSettings.user2['name']}")
        self.user2label.pack(ipadx=10,
                             padx=(120, 5),
                             anchor="center",
                             side=tk.RIGHT,
                             expand=True)

    def set_buttons(self, buttonframe: ttk.Frame):
        xsize = 40
        ysize = 15
        self.button1yes = tk.Button(
            buttonframe,
            text=f"Yes\n({UserSettings.user1['yes_button']})",
            state=tk.DISABLED)
        self.button1yes.pack(ipadx=xsize,
                             ipady=ysize,
                             padx=(20, 5),
                             pady=20,
                             anchor="sw",
                             side=tk.LEFT,
                             expand=True)
        self.button1no = tk.Button(
            buttonframe,
            text=f"No\n({UserSettings.user1['no_button']})",
            state=tk.DISABLED)
        self.button1no.pack(ipadx=xsize,
                            ipady=ysize,
                            padx=(5, 50),
                            pady=20,
                            anchor="sw",
                            side=tk.LEFT,
                            expand=True)
        self.button2yes = tk.Button(
            buttonframe,
            text=f"Yes\n({UserSettings.user2['yes_button']})",
            state=tk.DISABLED)
        self.button2yes.pack(ipadx=xsize,
                             ipady=ysize,
                             padx=(50, 5),
                             pady=20,
                             anchor="se",
                             side=tk.LEFT,
                             expand=True)
        self.button2no = tk.Button(
            buttonframe,
            text=f"No\n({UserSettings.user2['no_button']})",
            state=tk.DISABLED)
        self.button2no.pack(ipadx=xsize,
                            ipady=ysize,
                            padx=(5, 20),
                            pady=20,
                            anchor="se",
                            side=tk.LEFT,
                            expand=True)

    def run(self, name_list: list[str]) -> None:
        # name list
        self.name_list = name_list
        self.index = 0
        self.name_item = self.set_new_name(self.name_list, self.index)
        self.update_window()
        self.root.mainloop()

    def keydown(self, event):
        if event.char in (UserSettings.user1['yes_button'],
                          UserSettings.user1['no_button']):
            if not self.name_item["user1_response"]:
                if event.char == UserSettings.user1['yes_button']:
                    print("valid user input: " + event.char)
                    self.name_item["user1_response"] = "yes"
                    self.check_user_input()
                elif event.char == UserSettings.user1['no_button']:
                    print("valid user input: " + event.char)
                    self.name_item["user1_response"] = "no"
                    self.check_user_input()
                self.user1label.config(bg="snow1")
            else:
                print(f"Invalid input {event.char}. "
                      f"User1 already locked in with "
                      f"'{self.name_item['user1_response']}'.")

        elif (event.char in (UserSettings.user2['yes_button'],
                             UserSettings.user2['no_button'])):
            if not self.name_item["user2_response"]:
                if event.char == UserSettings.user2['yes_button']:
                    print("valid user input: " + event.char)
                    self.name_item["user2_response"] = "yes"
                    self.check_user_input()
                elif event.char == UserSettings.user2['no_button']:
                    print("valid user input: " + event.char)
                    self.name_item["user2_response"] = "no"
                    self.check_user_input()
                self.user2label.config(bg="snow1")
            else:
                print(f"Invalid input {event.char}. "
                      f"User2 already locked in with "
                      f"'{self.name_item['user2_response']}'.")

        else:
            print("INVALID user input: " + event.char)

    def check_user_input(self):
        if (self.name_item['user1_response']
                and self.name_item['user2_response']):
            if self.name_item['user1_response'] == "yes":
                self.button1yes.config(background='pale green')
            elif self.name_item['user1_response'] == "no":
                self.button1no.config(background='OrangeRed1')
            if self.name_item['user2_response'] == "yes":
                self.button2yes.config(background='pale green')
            elif self.name_item['user2_response'] == "no":
                self.button2no.config(background='OrangeRed1')

            self.button2no.after(1500, self.next_name)

    def next_name(self):
        self.write_to_db()
        self.reset_buttons()
        # next name
        self.index += 1
        self.name_item = self.set_new_name(self.name_list, self.index)
        self.update_name_label()
        self.update_counter_label()

    def write_to_db(self) -> None:
        try:
            add_result_to_db(self.name_item)
        except PermissionError as err:
            msgbox.showerror(
                title='ERROR',
                message=('Could not save to database.\n'
                         + err.args[1]
                         + "\n\nMaybe the 'db.csv' file is open in Excel?")
                )
            self.root.destroy()
            sys.exit()

    def update_window(self) -> None:
        self.update_counter_label()
        self.update_name_label()
        self.reset_buttons()

    def update_counter_label(self) -> None:
        self.counter_label.config(
            text=f"{len(self.name_list) - self.index}")

    def update_name_label(self) -> None:
        self.name_label.config(text=self.name_item["name"])
        self.sex_label.config(text=f"({self.name_item['sex']})")

    def reset_buttons(self) -> None:
        self.name_item['user1_response'] = ""
        self.name_item['user2_response'] = ""
        self.user1label.config(bg="SystemButtonFace")
        self.user2label.config(bg="SystemButtonFace")
        self.button1yes.config(bg='SystemButtonFace')
        self.button1no.config(bg='SystemButtonFace')
        self.button2yes.config(bg='SystemButtonFace')
        self.button2no.config(bg='SystemButtonFace')
