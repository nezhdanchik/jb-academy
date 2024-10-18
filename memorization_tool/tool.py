import enum

from menu import Menu, Option
from flashcard import Flashcard

class StateMenu(enum.Enum):
    MAIN_MENU = 1
    ADD_FLASHCARD_MENU = 2
    ADD_FLASHCARD = 3
    PRACTICE_FLASHCARD = 4
    QUESTION_MENU = 5
    EXIT = 0

class StateQuestion(enum.Enum):
    ANSWER = 1
    SKIP = 2
    UPDATE_MENU = 3
    EDIT = 4
    DELETE = 5

class Manage:
    def __init__(self):
        self.end_program = False
        self.current_state = StateMenu.MAIN_MENU

        self.main_menu = Menu()
        self.add_flash_menu = Menu()
        self.question_menu = Menu()
        self.update_menu = Menu()

        self.main_menu.options = [
            Option('1', '1. Add a new flashcard', StateMenu.ADD_FLASHCARD_MENU),
            Option('2', '2. Practice flashcards', StateMenu.PRACTICE_FLASHCARD),
            Option('3', '3. Exit', StateMenu.EXIT),
        ]

        self.add_flash_menu.options = [
            Option('1', '1. Add a new flashcard', StateMenu.ADD_FLASHCARD),
            Option('2', '2. Exit', StateMenu.MAIN_MENU),
        ]

        self.question_menu.options = [
            Option('y', 'press "y" to see the answer:', StateQuestion.ANSWER),
            Option('n', 'press "n" to skip:', StateQuestion.SKIP),
            Option('u', 'press "u" to update:', StateQuestion.UPDATE_MENU),
        ]

        self.update_menu.options = [
            Option('d', 'press "d" to delete the flashcard:', StateQuestion.DELETE),
            Option('e', 'press "e" to edit the flashcard:', StateQuestion.EDIT),
        ]

        self.run()


    def ask_input_question(self):
        while True:
            question = input('Question:\n')
            if question.replace(' ', ''):
                return question

    def ask_input_answer(self):
        while True:
            answer = input('Answer:\n')
            if answer.replace(' ', ''):
                return answer

    def listen(self, menu):
        menu.print()
        while True:
            choice = input()
            if choice in menu.options:
                return choice
            elif len(choice) == 0:
                continue
            else:
                print(f'{choice} is not an option')
                menu.print()


    def run(self):
        while not self.end_program:
            match self.current_state:
                case StateMenu.MAIN_MENU:
                    choice = self.listen(self.main_menu)
                    self.current_state = self.main_menu.options[choice].state
                case StateMenu.ADD_FLASHCARD_MENU:
                    choice = self.listen(self.add_flash_menu)
                    self.current_state = self.add_flash_menu.options[choice].state
                case StateMenu.ADD_FLASHCARD:
                    question = self.ask_input_question()
                    answer = self.ask_input_answer()
                    Flashcard.create_flashcard(question, answer)
                    self.current_state = StateMenu.ADD_FLASHCARD_MENU
                case StateMenu.PRACTICE_FLASHCARD:
                    flashcards = Flashcard.get_flashcards()
                    if len(flashcards) == 0:
                        print('There is no flashcard to practice!')
                        self.current_state = StateMenu.MAIN_MENU
                        continue
                    for flashcard in flashcards:
                        print(f'Question: {flashcard.question}')
                        choice = self.listen(self.question_menu)
                        match self.question_menu.options[choice].state:
                            case StateQuestion.ANSWER:
                                print(f'Answer: {flashcard.answer}')
                            case StateQuestion.SKIP:
                                continue
                            case StateQuestion.UPDATE_MENU:
                                choice = self.listen(self.update_menu)
                                match self.update_menu.options[choice].state:
                                    case StateQuestion.DELETE:
                                        flashcard.delete()
                                    case StateQuestion.EDIT:
                                        question = input('Question:\n')
                                        answer = input('Answer:\n')
                                        flashcard.update(question, answer)
                    self.current_state = StateMenu.MAIN_MENU
                case StateMenu.EXIT:
                    self.exit()


    def exit(self):
        print('Bye!')
        self.end_program = True


if __name__ == '__main__':
    Manage().run()
