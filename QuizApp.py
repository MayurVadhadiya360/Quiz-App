from ProjectPackage import *

# pyinstaller -F -w --onefile QuizApp.py --icon=images/quiz_icon.ico

server = firebase_server()
again = True    # Flag for when quiz window should be opened
###############################################################################
# ==== Login ====#
root = Tk()
acc = Login(root, server.auth)


def on_closing_Login():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        global again
        # Closing login window so windows after that should not be opened
        again = False
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing_Login)
root.mainloop()


while again:

    ###############################################################################
    # ==== Quiz Selection ====#

    root = Tk()
    SQ = SelectQuiz(root=root, acc=acc, db=server.db)


    def on_closing_SelectQuiz():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            global again
            # Closing SelectQuiz window so windows after that should not be opened
            again = False
            root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing_SelectQuiz)
    root.mainloop()

    if not again:
        break

    ###############################################################################
    # ==== Quiz code starts ====#

    root = Tk()
    QUIZ = quiz(root=root, quizName=SQ.QuizName, acc=acc, db=server.db)


    def on_closing_Quiz():
        messagebox.showwarning("Quit", "You cannot quit during quiz!")

    root.protocol("WM_DELETE_WINDOW", on_closing_Quiz)
    root.mainloop()

    if not again:
        break
