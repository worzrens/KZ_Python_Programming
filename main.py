from tkinter import *
from populate import *

window = Tk()
window.title("Welcome to Repl.it")
window.geometry('800x600')


#########################
subjects = query_subjects()
answers = query_answers()

subjects_list = Listbox(window, height=len(subjects), width=15, selectmode=MULTIPLE)
subjects_list.pack()
for sub in subjects:
    subjects_list.insert(END, str(sub.name))
    
    for question in query_questions(sub):
        questions_list = Label(window, text=question.text, font=('Helvetica', 16, 'bold'))
        questions_list.pack()
    linebreak = Label(window, text=END)
    linebreak.pack()


answers_list = Label(window, text=answers)
answers_list.pack()
######################


window.mainloop()
