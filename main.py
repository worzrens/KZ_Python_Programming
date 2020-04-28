from tkinter import *
from populate import *

window = Tk()
window.title("Пiдготовчi курси")
window.geometry('1360x768')


subjects = query_subjects()
answers = query_answers()

subjects_list = Listbox(window, height=len(subjects), width=15, selectmode=MULTIPLE)
subjects_list.pack()
for sub in subjects:
    subjects_list.insert(END, str(sub.name))

    questions_count = Label(window, text=f'For {sub.name} are {len(query_questions(sub))} questions\n',
                            font=('Helvetica', 14, 'bold'))
    questions_count.pack()
    for question in query_questions(sub):
        questions_list = Label(window, text=f"{question.text}", font=('Helvetica', 16, 'bold'))
        questions_list.pack()
    linebreak = Label(window, text="\n")
    linebreak.pack()


answers_list = Label(window, text=answers)
answers_list.pack()


window.mainloop()
