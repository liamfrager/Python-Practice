from quiz_brain import QuizBrain
import tkinter as tk
THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.score = 0
        # Tk window
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR, padx=20, pady=20)
        # Score display
        self.score_display = tk.Label(
            text="Score: 0", bg=THEME_COLOR, fg="white")
        self.score_display.grid(row=0, column=1)
        # Question display
        self.q_display = tk.Canvas(width=300, height=250, bg='white')
        self.q_text = self.q_display.create_text(
            150,
            125,
            width=280,
            fill=THEME_COLOR,
            font=('Arial', 20, 'italic')
        )
        self.q_display.grid(row=1, column=0, columnspan=2, pady=50)
        # True button
        self.true_img = tk.PhotoImage(file='./images/true.png')
        self.true_button = tk.Button(
            image=self.true_img,
            highlightcolor=THEME_COLOR,
            command=self.check_true
        )
        self.true_button.grid(row=2, column=0)
        # False button
        self.false_img = tk.PhotoImage(file='./images/false.png')
        self.false_button = tk.Button(
            image=self.false_img,
            highlightcolor=THEME_COLOR,
            command=self.check_false
        )
        self.false_button.grid(row=2, column=1)
        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        # Reset design
        self.q_display.config(bg='white')
        if self.quiz.still_has_questions():
            self.score_display.config(text=f"Score: {self.score}")
            q_text = self.quiz.next_question()
            self.q_display.itemconfig(
                self.q_text, text=q_text, fill=THEME_COLOR)
        else:
            self.q_display.itemconfig(
                self.q_text, text="Quiz complete!", fill=THEME_COLOR)
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def check_answer(self, user_answer: str):
        is_correct = self.quiz.check_answer(user_answer)
        if is_correct:
            self.score += 1
            self.q_display.config(bg='green')
        else:
            self.q_display.config(bg='red')
        self.q_display.itemconfig(self.q_text, fill='white')
        self.window.after(1000, self.get_next_question)

    def check_true(self):
        self.check_answer("True")

    def check_false(self):
        self.check_answer("False")
