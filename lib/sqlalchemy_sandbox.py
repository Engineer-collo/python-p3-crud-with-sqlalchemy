#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ =(
        PrimaryKeyConstraint("id", name="unique_id"),
        UniqueConstraint("email", name="unique_email"),
        CheckConstraint("grade BETWEEN 1 AND 12", name="grade_between_1_and_12")
    )
    
    Index("index_name", "name")
    
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime)
    enrolled_date = Column(DateTime(),default=datetime.now)

    def __repr__(self):
        return f"Student {self.id}, {self.name}, Grade {self.grade} "

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)
session = session()

albert_einstein = Student(
    name="albert_einstein",
    email="albert.einstein@zurich.edu",
    grade=6,
    birthday=datetime(
        year=1879,
        month=3,
        day=14
    )
)

alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        )
    )

session.bulk_save_objects([albert_einstein,alan_turing])
session.commit()

# students = session.query(Student).all()
# print(students)

    # create session, student objects

query = session.query(
    Student).filter(
        Student.name == "Albert Einstein")        

    # retrieve first matching record as object
albert_einstein = query.first()

    # delete record
session.delete(albert_einstein)
session.commit()

    # try to retrieve deleted record
albert_einstein = query.first()

print(albert_einstein)
    

