import uuid
from typing import List

from sqlalchemy import Integer, String, LargeBinary, ForeignKey, Text, Identity
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class User(Base):
    __tablename__: str = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4(), unique=True)
    records: Mapped[List["Record"]] = relationship(back_populates='user')

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.UUID}'


class Record(Base):
    __tablename__: str = 'record'

    record_id: Mapped[int] = mapped_column(Integer, Identity(start=1), primary_key=True)
    user_id: Mapped[id] = mapped_column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    UUID: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4())
    content: Mapped[bytes] = mapped_column(LargeBinary)
    user: Mapped["User"] = relationship(back_populates='records')
    record_name: Mapped[str] = mapped_column(Text)  # append attribute name for record for save original file name

    def __repr__(self):
        return f'record {self.UUID}'
