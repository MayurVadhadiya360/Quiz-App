import pyrebase
from tkinter import *
# from PIL import ImageTk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
# from matplotlib import pyplot as plt
from matplotlib.pyplot import subplot, title, xlabel, ylabel, plot, bar, pie, tight_layout, show
# import numpy as np
from numpy import array, zeros, arange
from scipy.stats import norm
from statistics import mean, stdev
from os.path import basename
from csv import reader


# pyinstaller -F -w --onefile QuizApp_admin.py

class firebase_server:
    def __init__(self):
        self.firebaseConfig = {
            'apiKey': "AIzaSyAE7WYgMHCiuNECxX8Bx6xmhoMr4BOaaI4",
            'authDomain': "logindemo-9c06d.firebaseapp.com",
            'projectId': "logindemo-9c06d",
            'storageBucket': "logindemo-9c06d.appspot.com",
            'messagingSenderId': "1042977831527",
            'appId': "1:1042977831527:web:97e799d486dd3b48fa32c2",
            'measurementId': "G-LK8RPMX8QP",
            'databaseURL': "https://logindemo-9c06d-default-rtdb.firebaseio.com/"
        }
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.db = self.firebase.database()


def plot_Result(lst):
    marks = []
    count_of_marks = zeros(11)
    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(lst)):
        marks.append(int(lst[i][1]))

        if int(lst[i][1]) == 0:
            count_of_marks[0] += 1

        elif int(lst[i][1]) == 1:
            count_of_marks[1] += 1

        elif int(lst[i][1]) == 2:
            count_of_marks[2] += 1

        elif int(lst[i][1]) == 3:
            count_of_marks[3] += 1

        elif int(lst[i][1]) == 4:
            count_of_marks[4] += 1

        elif int(lst[i][1]) == 5:
            count_of_marks[5] += 1

        elif int(lst[i][1]) == 6:
            count_of_marks[6] += 1

        elif int(lst[i][1]) == 7:
            count_of_marks[7] += 1

        elif int(lst[i][1]) == 8:
            count_of_marks[8] += 1

        elif int(lst[i][1]) == 9:
            count_of_marks[9] += 1

        elif int(lst[i][1]) == 10:
            count_of_marks[10] += 1

    marks = array(marks)

    subplot(2, 2, 1)
    title("Student Marks - Histogram")
    xlabel('Marks')
    ylabel('Number of student')
    BIN = range(11)
    bar(BIN, count_of_marks)

    subplot(2, 2, 2)
    marks.sort()
    # Probability Density Function
    nd = norm.pdf(marks, mean(marks), stdev(marks))
    title("Gaussian Distribution")
    xlabel('Marks')
    ylabel('PDF')
    plot(marks, nd, marker='o', markersize=2, color='blue', linewidth=1)

    subplot(2, 2, 3)
    y = arange(11)
    title('Pie Chart')
    pie(count_of_marks, labels=y, autopct='%.02f%%')

    tight_layout(pad=2, h_pad=1, w_pad=1)
    show()


def exit_win():
    exit()


class SelectQuiz_admin:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("admin - Quiz")
        self.root.geometry("700x600+100+50")
        self.root.config(background="#ffffff")
        self.root.maxsize(1600, 800)
        # self.root.wm_iconbitmap()
        self.list_box = None
        lst = self.db.child('Quiz').get().val()
        if lst is not None:
            self.QuizLST = list(lst.keys())
        else:
            self.QuizLST = []
            Label(self.root, text='No Quiz Available!', font=("Goudy old style", 15, "bold"), bg="#6fad93", fg='#6fff00').pack()
        self.j = 0

        for i in range(len(self.QuizLST)):
            if i % 3 == 0:
                self.j += 1
            self.b = Button(self.root, cursor="hand2", text=f"{self.QuizLST[i]}", fg="white", bg="#d77337", font=("times new roman", 20))
            self.b.grid(row=self.j, column=i % 3, padx=20, pady=20)
            self.b.bind('<Button-1>', self.click)

        self.MenuBar = Menu(self.root)
        self.FileMenu = Menu(self.MenuBar, tearoff=0)
        # To open new file
        self.FileMenu.add_command(label="Add New Quiz", command=self.add_quiz)
        self.FileMenu.add_command(label='Remove Quiz', command=self.remove_quiz)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label='Exit', command=exit_win)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)
        self.root.config(menu=self.MenuBar)
        self.rm_quiz = None
        self.rm_quiz_win = None

    def get_value(self):
        if self.rm_quiz.get() == '':
            messagebox.showerror("Error", "All fields are required", parent=self.rm_quiz_win)
        else:
            quiz = self.rm_quiz.get()
            if quiz not in self.QuizLST:
                messagebox.showwarning('Delete Warning', 'Entered quiz does not exist so cannot be deleted!', parent=self.rm_quiz_win)
                return
            self.db.child('Quiz').child(f"{quiz}").remove()
            self.rm_quiz_win.destroy()

    def remove_quiz(self):
        self.rm_quiz_win = Tk()
        self.rm_quiz_win.geometry("500x200")
        Label(self.rm_quiz_win, text='Enter name of the quiz you want to remove :').pack()
        self.rm_quiz = Entry(self.rm_quiz_win, width=20)
        self.rm_quiz.pack()
        Button(self.rm_quiz_win, text="Remove", command=self.get_value, font=("", 15, "bold"), bg='#689bde', fg='#ff0000', pady=2, padx=3).pack(pady=5, ipady=3, ipadx=3, side=TOP)
        self.rm_quiz_win.mainloop()

    def add_quiz(self):
        file = askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.csv")])
        if file is None:
            pass
        else:
            file_dict = {}
            file_ok = True
            try:
                if basename(file) in self.QuizLST:
                    file_ok = False
                if file_ok:
                    with open(file, 'r') as check:
                        csvreader = reader(check)
                        for row in csvreader:
                            if row[5] not in ('A', 'B', 'C', 'D'):
                                file_ok = False
                                break

                if file_ok:
                    with open(file, 'r') as check:
                        csvreader = reader(check)
                        rows = []
                        for row in csvreader:
                            rows.append(row)

                        for i in range(len(rows)):
                            file_dict.update({f"Que{i + 1}": f"{rows[i][0]}"})
                            file_dict.update({f"Opt{i + 1}": [rows[i][1], rows[i][2], rows[i][3], rows[i][4]]})
                            file_dict.update({f"Ans{i + 1}": f"{rows[i][5]}"})

            except Exception as e:
                file_ok = False
                messagebox.showwarning('Warning', f'Select valid file\n\nError:\n{e}', parent=self.root)

            if file_ok:
                try:
                    quizName = basename(file).replace('.csv', '')
                    # ------------------------------------------------------------------------------
                    # self.storage.child(f"QuizFiles/{LocalFile}").put(LocalPath + '/' + LocalFile)
                    if messagebox.askquestion('Upload Quiz', f"Do you want to upload '{quizName}'?"):
                        self.db.child('Quiz').child(quizName).update(file_dict)
                        messagebox.showinfo('Uploaded', f'{quizName} is uploaded!\nRestart app to see changes!', parent=self.root)
                except Exception as e:
                    messagebox.showerror('ERROR!', f'{e}', parent=self.root)
            else:
                return

    def ShowResult(self, quizName):
        temp = (self.db.child('Result').get().val())
        if temp is not None:
            temp = dict(temp)
            all_user_LST = list(temp.keys())
            all_result_LST = list(temp.values())
            user_result_LST = []
            for i in range(len(all_result_LST)):
                if all_result_LST[i].get(f'{quizName}') is not None:
                    t = [all_user_LST[i], all_result_LST[i].get(f'{quizName}')]
                    user_result_LST.append(t)

        f1 = Frame(self.root, width=500)
        f1.grid(row=1, column=3, rowspan=4, columnspan=3, padx=10, pady=10, ipadx=10, ipady=10)
        scrollbar_lbx = Scrollbar(f1)
        # scrollbar_lbx.grid(row=1, rowspan=4, column=6)

        self.list_box = Listbox(f1, width=400, yscrollcommand=scrollbar_lbx.set)
        # self.lbx.grid(row=1, column=3, rowspan=4, columnspan=3, padx=10, pady=10)
        self.list_box.pack(side=LEFT, in_=f1)
        scrollbar_lbx.pack(side=RIGHT, fill=Y)
        for i in range(len(user_result_LST)):
            self.list_box.insert(END, f"{i + 1}. {user_result_LST[i][0]:<30}- {user_result_LST[i][1]}/{10}")
        scrollbar_lbx.config(command=self.list_box.yview)
        plot_Result(user_result_LST)

    def click(self, event):
        pass
        text = event.widget.cget("text")
        try:
            self.ShowResult(text)
            self.root.title(f"admin - {text}")
        except Exception as e:
            messagebox.showerror("ERROR!", f"{e}", parent=self.root)


server = firebase_server()
root = Tk()
SQa = SelectQuiz_admin(root=root, db=server.db)


def on_closing_SelectQuiz():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        exit()


root.protocol("WM_DELETE_WINDOW", on_closing_SelectQuiz)

root.mainloop()
