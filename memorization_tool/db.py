from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, create_engine


class Database:
    engine = create_engine('sqlite:///flashcard.db')

    @staticmethod
    def create_db_and_tables() -> None:
        Base.metadata.create_all(Database.engine)


class Base(DeclarativeBase):
    pass


class FlashcardBase(Base):
    __tablename__ = "flashcard"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(500))
    answer: Mapped[str] = mapped_column(String(500))

    def __repr__(self):
        return f'Flashcard({self.id=} {self.question=}, {self.answer=})'

    @staticmethod
    def create_flashcard(question, answer):
        flashcard = FlashcardBase(question=question, answer=answer)
        with Session(Database.engine) as session:
            session.add(flashcard)
            session.commit()
            session.refresh(flashcard)
        return flashcard

    @staticmethod
    def get_flashcards():
        with Session(Database.engine) as session:
            return session.query(FlashcardBase).all()

    @staticmethod
    def update_flashcard(flashcard_id, question=None, answer=None):
        if question and question.replace(' ', '') == '':
            question = None
        if answer and answer.replace(' ', '') == '':
            answer = None
        with Session(Database.engine) as session:
            flashcard = session.query(FlashcardBase).get(flashcard_id)
            flashcard.question = question if question else flashcard.question
            flashcard.answer = answer if answer else flashcard.answer
            session.commit()

    @staticmethod
    def delete(flashcard_id):
        with Session(Database.engine) as session:
            flashcard = session.query(FlashcardBase).get(flashcard_id)
            session.delete(flashcard)
            session.commit()


Database.create_db_and_tables()
