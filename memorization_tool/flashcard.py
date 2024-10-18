from db import FlashcardBase


class Flashcard:
    def __init__(self, id, question: str, answer: str):
        self._id = id
        self.question = question
        self.answer = answer

    def update(self, question: str, answer: str):
        FlashcardBase.update_flashcard(self._id, question, answer)

    def delete(self):
        FlashcardBase.delete(self._id)

    @staticmethod
    def get_flashcards():
        return [Flashcard(fc.id, fc.question, fc.answer) for fc in
                FlashcardBase.get_flashcards()]

    @staticmethod
    def create_flashcard(question, answer):
        return FlashcardBase.create_flashcard(question, answer)
