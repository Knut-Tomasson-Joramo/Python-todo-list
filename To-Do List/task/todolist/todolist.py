# Write your code here
import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# Create database file and engine
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# ------------------Create table in database------------------
Base = declarative_base()  # Model class need to inherit from this


# Create the model class. Attributes equals table columns
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create our database
Base.metadata.create_all(engine)


# Functions
def today_task(the_session):
    today = datetime.today()
    all_rows = the_session.query(Task).filter(Task.deadline == today.date()).all()
    print("Today:", today.day, today.strftime('%b'))
    if len(all_rows) == 0:
        print("Nothing to do!")
    else:
        for num, row in enumerate(all_rows):
            print(f'{num + 1}) {row.task}, deadline: {row.deadline}')


def add_task(the_session):
    the_task = input("Enter task")
    the_deadline = datetime.strptime(input("Enter deadline"), '%Y-%m-%d')
    new_task = Task(task=the_task, deadline=the_deadline)
    the_session.add(new_task)
    the_session.commit()
    print("The task has been added")


def weeks_tasks(the_session):
    day_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.today()
    for i in range(7):
        this_day = today + timedelta(days=i)
        this_day_tasks = the_session.query(Task).\
            filter(Task.deadline == this_day.date()).all()
        print(day_array[this_day.weekday()], this_day.day, this_day.strftime('%b'))
        if len(this_day_tasks) == 0:
            print("Nothing to do!")
        else:
            for num, row in enumerate(this_day_tasks):
                print(f'{num + 1}) {row.task}')
        print()


def all_tasks(the_session):
    print("All tasks:")
    all_the_tasks = the_session.query(Task).order_by(Task.deadline).all()
    if len(all_the_tasks) == 0:
        print("You do not have any tasks! Add some!")
    else:
        for num, row in enumerate(all_the_tasks):
            print(f'{num + 1}) {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')


def missed_tasks(the_session):
    miss_task = the_session.query(Task).filter(Task.deadline < datetime.today().date()).all()
    if len(miss_task) == 0:
        print("Nothing is missed!")
    else:
        print("Missed tasks:")
        for num, row in enumerate(miss_task):
            print(f'{num + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')


def delete_task(the_session):
    # Print all tasks first
    all_task = the_session.query(Task).order_by(Task.deadline).all()
    if all_task == 0:
        print("No tasks!")
    else:
        print("Choose the number of the task you want to delete:")
        for num, row in enumerate(all_task):
            print(f'{num + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')

        to_delete = int(input())
        the_session.delete(all_task[to_delete - 1])
        the_session.commit()


# Program runs here
# Use session to access data and store data in it
Session = sessionmaker(bind=engine)
session = Session()

menu_titles = ["Today's tasks", "Week's tasks", "All tasks",
               "Missed tasks", "Add task", "Delete task", "Exit"]
while True:
    for number, value in enumerate(menu_titles):
        print(f"{number + 1 if number + 1 != len(menu_titles) else 0}) {value}")

    print()

    choice = int(input().strip())

    if choice == 0:
        sys.exit()
    elif choice == 1:
        today_task(session)
    elif choice == 2:
        weeks_tasks(session)
    elif choice == 3:
        all_tasks(session)
    elif choice == 4:
        missed_tasks(session)
    elif choice == 5:
        add_task(session)
    elif choice == 6:
        delete_task(session)

    print()
