
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
import sys
import os
from functions import add_result_to_db

# user names
USERNAME1 = "Anissa"
USERNAME2 = "Christoph"

# user buttons
USER1YES = "y"
USER1NO = "c"
USER2YES = "1"
USER2NO = "3"


class NameSelector:

    def __init__(self, name_list: list[str], db_file: str) -> None:

        self.root = tk.Tk()

        # database filepath
        self.db_file = db_file

        # name list
        self.name_list = name_list
        self.index = 0
        self.name_item: dict = self.set_new_name(self.name_list, self.index)

        self.set_window()
        self.set_frames()
        self.set_counterlabel()
        self.set_namelabel()
        self.set_sexlabel()
        self.set_usernames()
        self.set_buttons()
        self.root.bind("<KeyPress>", self.keydown)

        if getattr(sys, 'frozen', False):
            iconpath = os.path.join(sys._MEIPASS, "peanut.ico")  # type: ignore
        else:
            iconpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "peanut.ico")
        self.root.iconbitmap(iconpath)

        self.root.mainloop()

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
        self.root.title("Peanut Name Selector")

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

    def set_frames(self):
        self.counterframe = ttk.Frame(self.root)
        self.counterframe.pack(side=tk.TOP, anchor="ne")
        self.nameframe = ttk.Frame(self.root)
        self.nameframe.pack(side=tk.TOP, expand=True)
        self.userframe = ttk.Frame(self.root)
        self.userframe.pack(side=tk.TOP)
        self.buttonframe = ttk.Frame(self.root)
        self.buttonframe.pack(side=tk.TOP)

    def set_counterlabel(self):
        self.counter_label = tk.Label(
            self.counterframe,
            text=f"{len(self.name_list) - self.index}",
            font=("Helvetica", 10),
            fg="snow4")
        self.counter_label.pack(
            ipadx=15,
            ipady=10)

    def set_namelabel(self):
        self.name_label = tk.Label(
            self.nameframe,
            text=self.name_item["name"],
            font=("Helvetica", 40))
        self.name_label.pack(
            ipadx=10,
            ipady=10,
            anchor="center",)

    def set_sexlabel(self):
        self.sex_label = tk.Label(self.nameframe,
                                  text=f"({self.name_item['sex']})",
                                  font=("Helvetica", 10))
        self.sex_label.pack(
            ipadx=10,
            anchor="center",)

    def set_usernames(self):
        self.user1label = tk.Label(self.userframe,
                                   text=f"{USERNAME1}\n(User 1)")
        self.user1label.pack(
            ipadx=10,
            padx=100,
            anchor="center",
            side=tk.LEFT,
            expand=True
        )
        self.user2label = tk.Label(self.userframe,
                                   text=f"{USERNAME2}\n(User 2)")
        self.user2label.pack(
            ipadx=10,
            padx=100,
            anchor="center",
            side=tk.RIGHT,
            expand=True
        )

    def set_buttons(self):
        xsize = 40
        ysize = 15
        self.button1yes = tk.Button(self.buttonframe,
                                    text=f"Yes\n({USER1YES})",
                                    state=tk.DISABLED)
        self.button1yes.pack(
            ipadx=xsize,
            ipady=ysize,
            padx=(20, 5),
            pady=20,
            anchor="sw",
            side=tk.LEFT,
            expand=True
        )
        self.button1no = tk.Button(self.buttonframe,
                                   text=f"No\n({USER1NO})",
                                   state=tk.DISABLED)
        self.button1no.pack(
            ipadx=xsize,
            ipady=ysize,
            padx=(5, 50),
            pady=20,
            anchor="sw",
            side=tk.LEFT,
            expand=True
        )
        self.button2yes = tk.Button(self.buttonframe,
                                    text=f"Yes\n({USER2YES})",
                                    state=tk.DISABLED)
        self.button2yes.pack(
            ipadx=xsize,
            ipady=ysize,
            padx=(50, 5),
            pady=20,
            anchor="se",
            side=tk.LEFT,
            expand=True
        )
        self.button2no = tk.Button(self.buttonframe,
                                   text=f"No\n({USER2NO})",
                                   state=tk.DISABLED)
        self.button2no.pack(
            ipadx=xsize,
            ipady=ysize,
            padx=(5, 20),
            pady=20,
            anchor="se",
            side=tk.LEFT,
            expand=True
        )


    def keydown(self, event):
        if event.char == USER1YES or event.char == USER1NO:
            if not self.name_item["user1_response"]:
                if event.char == USER1YES:
                    print("valid user input: " + event.char)
                    self.name_item["user1_response"] = "yes"
                    self.check_user_input()
                elif event.char == USER1NO:
                    print("valid user input: " + event.char)
                    self.name_item["user1_response"] = "no"
                    self.check_user_input()
                self.user1label.config(bg="snow1")
            else:
                print(f"Invalid input {event.char}. "
                      f"User1 already locked in with "
                      f"'{self.name_item['user1_response']}'.")
        elif event.char == USER2YES or event.char == USER2NO:
            if not self.name_item["user2_response"]:
                if event.char == USER2YES:
                    print("valid user input: " + event.char)
                    self.name_item["user2_response"] = "yes"
                    self.check_user_input()
                elif event.char == USER2NO:
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
        self.update_name_label(self.name_item)
        self.update_counter_label()

    def write_to_db(self) -> None:
        try:
            add_result_to_db(self.db_file, self.name_item)
        except PermissionError as err:
            msgbox.showinfo(
                title='ERROR',
                message=('Could not save to database.\n'
                         + err.args[1]
                         + "\n\nMaybe the 'db.csv' file is open in Excel?")
                )
            self.root.destroy()
            sys.exit()

    def update_counter_label(self) -> None:
        self.counter_label.config(
            text=f"{len(self.name_list) - self.index}")

    def update_name_label(self, name: dict) -> None:
        self.name_label.config(text=name["name"])
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
