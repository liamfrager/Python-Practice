from question_model import Question
from data import question_data
from quiz_brain import QuizBrain


questions = []
for question in question_data:
    new_q = Question(question['question'], question['correct_answer'])
    questions.append(new_q)


quiz_brain = QuizBrain(questions)
while quiz_brain.still_has_questions():
    quiz_brain.next_question()

print("You completed the quiz!")
print(f"Your final score was: {quiz_brain.score}/{len(quiz_brain.q_bank)}")
