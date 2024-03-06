class QuizBrain:

    def __init__(self, questions):
        self.q_num = 0
        self.q_bank = questions
        self.score = 0

    def still_has_questions(self):
        return self.q_num < len(self.q_bank)

    def next_question(self):
        question = self.q_bank[self.q_num]
        self.q_num += 1
        user_answer = input(f"Q.{self.q_num}: {question.text} (T/F)?: ")
        correct_answer = question.answer
        self.check_answer(user_answer, correct_answer)

    def check_answer(self, user_answer, correct_answer):
        if user_answer[0].lower() == correct_answer[0].lower():
            self.score += 1
            print("Correct!")
        else:
            print("You got it wrong.")
        print(f"The correct answer was: {correct_answer}")
        print(f"Your score is {self.score}/{self.q_num}")
        print()
