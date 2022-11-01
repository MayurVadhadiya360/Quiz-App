import pyrebase
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk
from random import randint
from time import sleep


class firebase_server:
    def __init__(self):
        self.firebaseConfig = {
            'apiKey': "",
            'authDomain': "",
            'projectId': "",
            'storageBucket': "",
            'messagingSenderId': "",
            'appId': "",
            'measurementId': "",
            'databaseURL': ""
        }
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()


class Login:
    def __init__(self, root, auth):
        self.root = root
        self.auth = auth
        self.root.title("Login System")
        self.root.geometry("1200x600+100+50")
        self.root.wm_iconbitmap('images/quiz_icon.ico')
        self.root.resizable(False, False)
        self.email = None
        self.password = None
        self.user = None
        self.text_user_signup = None
        self.text_pass_signup = None
        # =====BG Image=====
        self.bg = ImageTk.PhotoImage(file="images/backgroundIMG.png")
        Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        # =====Login Frame=====
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=50, y=150, height=340, width=500)

        Label(Frame_login, text="Login Here", font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=90, y=30)
        Label(Frame_login, text="Quiz Login Area", font=("Goudy old style", 15, "bold"), fg="#d25d17", bg="white").place(x=90, y=100)

        Label(Frame_login, text="Email", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=90, y=140)
        self.text_user = Entry(Frame_login, font=("times new roman", 15), bg="lightgrey")
        self.text_user.place(x=90, y=170, height=35, width=350)

        Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=90, y=210)
        self.text_pass = Entry(Frame_login, show='*', font=("courier new", 13), bg="lightgrey")
        self.text_pass.place(x=90, y=240, height=35, width=350)
        Button(Frame_login, command=self.forgot_password, cursor="hand2", text="Forgot Password ?", bg="white", fg="#d77337", border=0, font=("times new roman", 12)).place(x=90, y=280)
        Button(Frame_login, command=self.signup_frame, cursor="hand2", text="New user? Sign Up", bg="white", fg="#d77337", border=0, font=("times new roman", 12)).place(x=300, y=280)
        Button(self.root, command=self.login_function, cursor="hand2", text="Login", fg="white", bg="#d77337", font=("times new roman", 20)).place(x=210, y=470, width=180, height=40)

    def login_function(self):
        if self.text_pass.get() == '' or self.text_user.get() == '':
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            self.text_pass.delete(0, END)
        else:
            try:
                self.email = self.text_user.get()
                self.password = self.text_pass.get()
                self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
                messagebox.showinfo("Welcome", f"{self.user['email']} logged in successfully!", parent=self.root)
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Wrong password or\nAccount doesn't exist\n\nDetails:\n{e}", parent=self.root)
                self.text_pass.delete(0, END)

    def signup_function(self):
        if self.text_pass_signup.get() == '' or self.text_user_signup.get() == '':
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            self.text_pass_signup.delete(0, END)
        else:
            try:
                self.email = self.text_user_signup.get()
                self.password = self.text_pass_signup.get()
                self.user = self.auth.create_user_with_email_and_password(self.email, self.password)
                messagebox.showinfo("Welcome", f"successfully created account with {self.user['email']}!", parent=self.root)
                self.root.destroy()
            except Exception as e:
                messagebox.showwarning("Warning", f"Error occured!\n\nDetails:\n{e}", parent=self.root)
                self.text_pass_signup.delete(0, END)

    def forgot_password(self):
        if self.text_user.get() == '':
            messagebox.showerror("Error", "Email required", parent=self.root)
            self.text_pass.delete(0, END)
        else:
            try:
                self.email = self.text_user.get()
                self.user = self.auth.send_password_reset_email(self.email)
                messagebox.showinfo("Welcome", f"Password reset email sent to {self.user['email']}!\n\tPlease, check it out", parent=self.root)
            except Exception as e:
                messagebox.showwarning("Warning", f"Make sure to enter proper email!\n\nDetails:\n{e}", parent=self.root)
                self.text_pass.delete(0, END)

    def signup_frame(self):
        Frame_signup = Frame(self.root, bg="white")
        Frame_signup.place(x=650, y=150, height=340, width=500)

        Label(Frame_signup, text="Sign Up Here", font=("Impact", 35, "bold"), fg="#d77337", bg="white").place(x=90, y=30)
        Label(Frame_signup, text="Create new account here", font=("Goudy old style", 15, "bold"), fg="#d25d17", bg="white").place(x=90, y=100)

        Label(Frame_signup, text="Email", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=90, y=140)
        self.text_user_signup = Entry(Frame_signup, font=("times new roman", 15), bg="lightgrey")
        self.text_user_signup.place(x=90, y=170, height=35, width=350)

        Label(Frame_signup, text="Password", font=("Goudy old style", 15, "bold"), fg="grey", bg="white").place(x=90, y=210)
        self.text_pass_signup = Entry(Frame_signup, show='*', font=("courier new", 13), bg="lightgrey")
        self.text_pass_signup.place(x=90, y=240, height=35, width=350)

        Button(self.root, command=self.signup_function, cursor="hand2", text="Sign Up", fg="white", bg="#d77337", font=("times new roman", 20)).place(x=810, y=470, width=180, height=40)


class SelectQuiz:
    def __init__(self, root, acc, db):
        self.root = root
        self.acc = acc
        self.db = db
        self.root.title(f"{self.acc.user['email']} - Quiz")
        self.root.geometry("700x600+100+50")
        self.root.wm_iconbitmap('images/quiz_icon.ico')
        self.root.config(background="#ffffff")
        self.root.maxsize(1600, 800)
        # self.root.wm_iconbitmap()
        self.QuizName = None
        lst = self.db.child('Quiz').get().val()
        if lst is not None:
            self.QuizLST = list(lst.keys())
        else:
            self.QuizLST = []
            Label(self.root, text='No Quiz Available!', font=("Goudy old style", 15, "bold"), bg="#6fad93", fg='#6fff00').pack()
        self.total = 10
        self.ResultFound = False
        self.j = 0

        for i in range(len(self.QuizLST)):
            if i % 3 == 0:
                self.j += 1
            self.b = Button(self.root, cursor="hand2", text=f"{self.QuizLST[i]}", fg="white", bg="#d77337", font=("times new roman", 20))
            self.b.grid(row=self.j, column=i % 3, padx=20, pady=20)
            self.b.bind('<Button-1>', self.click)

    def click(self, event):
        self.QuizName = event.widget.cget("text")
        try:
            self.ResultFound, score = self.CheckIfQuizIsAlreadyGiven(self.QuizName)
            if self.ResultFound:
                messagebox.showinfo("Quiz Already Given", f'Your score is "{score}/{self.total}" ', parent=self.root)
            else:
                messagebox.showinfo("Quiz Selected", f'"{self.QuizName}" Quiz will start now !', parent=self.root)
                self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"{e}", parent=self.root)

    def CheckIfQuizIsAlreadyGiven(self, quizname):
        mail = f"{self.acc.user['email']}".replace('.', '')
        temp = self.db.child('Result').child(mail).get().val()
        if temp is not None:
            t1 = dict(temp)
            if t1.get(quizname) is not None:
                return True, int(t1.get(quizname))
            else:
                return False, 0
        else:
            return False, 0


class quiz:
    def __init__(self, root, quizName, acc, db):
        self.root = root
        self.quizName = quizName
        self.acc = acc
        self.db = db
        self.root.title(f"{acc.user['email']} - {self.quizName} - Quizstar")
        self.root.geometry("700x600+100+50")
        self.root.config(background="#ffffff")
        self.root.wm_iconbitmap('images/quiz_icon.ico')
        self.root.resizable(False, True)

        self.questions, self.answers_choice, self.answers = self.extractData(self.quizName)
        self.user_answer = []

        self.indexes = []
        self.ques = 1
        self.score = 0
        self.total = 0

        self.img1 = PhotoImage(file="images/transparentGradHat.png")
        self.label_image = Label(
            self.root,
            image=self.img1,
            background="#ffffff",
        )
        self.label_image.pack(pady=(40, 0))

        self.labeltext = Label(
            self.root,
            text="Quiz",
            font=("Comic sans MS", 24, "bold"),
            background="#ffffff",
        )
        self.labeltext.pack(pady=(0, 50))

        self.img2 = PhotoImage(file="images/Frame.png")
        self.btnStart = Button(
            self.root,
            image=self.img2,
            relief=FLAT,
            border=0,
            command=self.startIspressed,
        )
        self.btnStart.pack()

        self.lblInstruction = Label(
            self.root,
            text="Read The Rules And\nClick Start Once You Are ready",
            background="#ffffff",
            font=("Consolas", 14),
            justify="center",
        )
        self.lblInstruction.pack(pady=(10, 100))

        self.lblRules = Label(
            self.root,
            text="This quiz contains 10 questions\nYou won't be able leave quiz once stated until completed\nYou will get only one attempt for any quiz\nYour score will be displayed right after quiz!",
            width=100,
            font=("Times", 14),
            background="#000000",
            foreground="#FACA2F",
        )
        self.lblRules.pack()

        self.progress_bar = None
        self.label_result_text = None
        self.lblQuestion = None
        self.radio_var = None
        self.r1 = None
        self.r2 = None
        self.r3 = None
        self.r4 = None
        self.btn_next = None

    def extractData(self, quizname):
        questions = []
        answers_choice = []
        answers = []

        temp = dict(self.db.child('Quiz').child(quizname).get().val())
        # print(len(temp)) = 30
        for i in range(len(temp) // 3):
            questions.append(temp[f"Que{i + 1}"])
            answers_choice.append(temp[f"Opt{i + 1}"])

            if temp[f"Ans{i + 1}"] == 'A':
                answers.append(int(0))
            elif temp[f"Ans{i + 1}"] == 'B':
                answers.append(int(1))
            elif temp[f"Ans{i + 1}"] == 'C':
                answers.append(int(2))
            elif temp[f"Ans{i + 1}"] == 'D':
                answers.append(int(3))

        return questions, answers_choice, answers

    def gen(self):
        # global indexes
        while len(self.indexes) < 10:
            x = randint(0, 9)
            if x in self.indexes:
                continue
            else:
                self.indexes.append(x)

    def showresult(self, score, total):
        mail = f"{self.acc.user['email']}".replace('.', '')
        self.db.child('Result').child(mail).update({f"{self.quizName}": score})
        self.lblQuestion.destroy()
        self.r1.destroy()
        self.r2.destroy()
        self.r3.destroy()
        self.r4.destroy()
        self.btn_next.destroy()
        self.label_image = Label(
            self.root,
            background="#ffffff",
            border=0,
        )
        self.label_image.pack(pady=(50, 30))
        self.label_result_text = Label(
            self.root,
            font=("Consolas", 20),
            background="#ffffff",
        )
        self.label_result_text.pack()
        if score >= int(total * 0.8):
            img = PhotoImage(file="images/great.png")
            self.label_image.configure(image=img)
            self.label_image.image = img
            self.label_result_text.configure(text="You Are Excellent !!")
        elif int(total * 0.4) <= score < int(total * 0.8):
            img = PhotoImage(file="images/ok.png")
            self.label_image.configure(image=img)
            self.label_image.image = img
            self.label_result_text.configure(text="You Can Be Better !!")
        else:
            img = PhotoImage(file="images/bad.png")
            self.label_image.configure(image=img)
            self.label_image.image = img
            self.label_result_text.configure(text="You Should Work Hard !!")
        messagebox.showinfo('Result', f'Your score is {score}/{total}')
        sleep(2)
        self.root.destroy()

    def calc(self):
        x = 0
        score = 0
        total = 0
        for i in self.indexes:
            if self.user_answer[x] == self.answers[i]:
                score = score + 1
            total = total + 1
            x += 1
        # print(score)
        self.score = score
        self.total = total
        self.showresult(score, total)

    def selected(self):
        x = self.radio_var.get()
        self.user_answer.append(x)
        self.progress_bar['value'] += 10
        self.radio_var.set(-1)
        if self.ques < 10:
            self.lblQuestion.config(text=f"{self.ques + 1}.  {self.questions[self.indexes[self.ques]]}")
            self.r1['text'] = self.answers_choice[self.indexes[self.ques]][0]
            self.r2['text'] = self.answers_choice[self.indexes[self.ques]][1]
            self.r3['text'] = self.answers_choice[self.indexes[self.ques]][2]
            self.r4['text'] = self.answers_choice[self.indexes[self.ques]][3]
            self.ques += 1
        else:
            # print(indexes)
            # print(user_answer)
            # these two lines were just developement code
            # we don't need them
            self.calc()

    def startquiz(self):
        self.progress_bar = ttk.Progressbar(
            self.root,
            orient=HORIZONTAL,
            mode='determinate'
        )
        self.progress_bar.pack(pady=20, fill=X)
        self.lblQuestion = Label(
            self.root,
            text=f"{self.ques}.  {self.questions[self.indexes[0]]}",
            font=("Consolas", 16),
            width=600,
            justify="center",
            wraplength=500,
            background="#ffffff",
        )
        self.lblQuestion.pack(pady=(50, 30), anchor='w')

        # global radiovar
        self.radio_var = IntVar()
        self.radio_var.set(-1)

        self.r1 = Radiobutton(
            self.root,
            text=self.answers_choice[self.indexes[0]][0],
            font=("Times", 12),
            value=0,
            variable=self.radio_var,
            # command=selected,
            background="#ffffff",
        )
        self.r1.pack(pady=10, padx=150, anchor='w')

        self.r2 = Radiobutton(
            self.root,
            text=self.answers_choice[self.indexes[0]][1],
            font=("Times", 12),
            value=1,
            variable=self.radio_var,
            # command=selected,
            background="#ffffff",
        )
        self.r2.pack(pady=10, padx=150, anchor='w')

        self.r3 = Radiobutton(
            self.root,
            text=self.answers_choice[self.indexes[0]][2],
            font=("Times", 12),
            value=2,
            variable=self.radio_var,
            # command=selected,
            background="#ffffff",
        )
        self.r3.pack(pady=10, padx=150, anchor='w')

        self.r4 = Radiobutton(
            self.root,
            text=self.answers_choice[self.indexes[0]][3],
            font=("Times", 12),
            value=3,
            variable=self.radio_var,
            # command=selected,
            background="#ffffff",
        )
        self.r4.pack(pady=10, padx=150, anchor='w')
        # img_next = PhotoImage(file="images/Next.png")
        self.btn_next = Button(
            self.root,
            text='Next',
            cursor="hand2",
            relief=FLAT,
            bg='#00BFFF',
            fg='white',
            font=('cursive', 18, 'bold'),
            padx=10,
            pady=5,
            command=self.selected
        )
        # self.btn1.pack(padx=120, pady=50, anchor='w')
        self.btn_next.pack(pady=50)

    def startIspressed(self):
        self.label_image.destroy()
        self.labeltext.destroy()
        self.lblInstruction.destroy()
        self.lblRules.destroy()
        self.btnStart.destroy()
        self.gen()
        self.startquiz()
