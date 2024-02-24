from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    __tablename__ = "input"

    age: Mapped[int]
    name: Mapped[str]
    job: Mapped[str]
    marital: Mapped[str]
    education: Mapped[int]
    default: Mapped[str]
    balance: Mapped[str]
    housing: Mapped[str]
    loan: Mapped[str]
    day: Mapped[int]
    month: Mapped[str]
    duration: Mapped[int]
    campaign: Mapped[int]
    pdays: Mapped[int]
    previous: Mapped[int]
    poutcome: Mapped[str]
