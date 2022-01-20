import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    JSON,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship, validates

from database import Base


class Eval(Base):
    __tablename__ = 'eval'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    evaluator_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    evaluatee_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    date = Column(Date, nullable=False)
    review = Column(JSON, nullable=True)
    feedback = Column(JSON, nullable=True)

    evaluator = relationship('User', foreign_keys=[evaluator_id])
    evaluatee = relationship('User', foreign_keys=[evaluatee_id])
    cohort = relationship('Cohort')

    @validates('evaluator_id', 'evaluatee_id')
    def validate_evaluator_id(self, key, value):
        if type(value) is not int:
            raise TypeError

        if len(str(value)) != 18:
            raise ValueError

        if key == 'evaluatee_id' and value == self.evaluator_id:
            raise ValueError

        return value

    @validates('cohort_id')
    def validate_cohort_id(self, key, cohort_id):
        if type(cohort_id) is not int:
            raise TypeError

        return cohort_id

    @validates('date')
    def validate_date(self, key, date):
        if type(date) is not datetime.date:
            raise TypeError

        return date


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    nickname = Column(String(16), nullable=False)
