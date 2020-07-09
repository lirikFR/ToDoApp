from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Date, Integer, DateTime
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
base = declarative_base()


class Task(base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return str(self.id) + ". " + self.task



base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_new_row():
    user_input_name = input("Enter task\n")
    user_input_date = input("Enter deadline\n")
    try:
        new_row = Task(task=user_input_name, deadline=datetime.strptime(user_input_date, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    except Exception as e:
        print(e)


def print_all_rows():
    rows = session.query(Task).all()
    print("All tasks: ")
    if rows:
        for row in rows:
            print(row, "/"+row.deadline.strftime("%d %B"))
        print()
    else:
        print("Nothing to do!")


def print_todays_tasks():
    today = datetime.today().date()
    rows = session.query(Task).filter(Task.deadline == today).all()
    print("Today " + str(datetime.today().date().strftime("%d %B")) + ":")
    if rows:
        for row in rows:
            print(row)
        print()
    else:
        print("Nothing to do!")


def print_weeks_tasks():
    weekday = datetime.today().date()
    for day in range(7):
        rows = session.query(Task).filter(Task.deadline == weekday).all()
        print(str(weekday.strftime("%A %d %B")) + ":")
        weekday += timedelta(days=1)
        if rows:
            for row in rows:
                print(row)
            print()
        else:
            print("Nothing to do!\n")


def delete_task():
    print("Chose the number of the task you want to delete:")
    print_all_rows()
    try:
        number = int(input())
        row = session.query(Task).filter(Task.id == number).all()
        specific_row = row[0]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")
    except Exception as e:
        print(e)


def missed_tasks():
    print("Missed tasks:")
    rows = session.query(Task).filter(Task.deadline < datetime.today().date())
    if rows:
        for row in rows:
            print(row, "/"+row.deadline.strftime("%d %B"))
    else:
        print("Nothing is missed!")
    print()

def option(i):
    switcher = {
        1: "print_todays_tasks()",
        2: "print_weeks_tasks()",
        3: "print_all_rows()",
        4: "missed_tasks()",
        5: "create_new_row()",
        6: "delete_task()",
        0: "print('Bye!')"

    }
    return eval(switcher.get(i, "Invalid Input"))


def interact():
    while True:
        print("""1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit""")
        try:
            user_input = int(input())
            option(user_input)
            if user_input == 0:
                break
        except Exception as e:
            print(e)


interact()
