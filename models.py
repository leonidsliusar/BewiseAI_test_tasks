from sqlalchemy import Integer, Text, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class QuizQuestion(Base):
    __tablename__: str = 'quiz_question'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f'{self.id}, {self.question}'
