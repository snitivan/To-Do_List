# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
rows = session.query(Table).all()
#print(rows)
today = datetime.today()
while True:
    print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    select = int(input('> '))
    if select == 1:
        rows_day = session.query(Table).filter(Table.deadline == today.date()).all()
        if len(rows_day) == 0:
            print(f'Today {today.day} {today.strftime("%b")}:')
            print(f'\nNothing to do!')
        else:
            print(f'Today {today.day} {today.strftime("%b")}:')
            for i in range(0, len(rows_day)):
                print(f'{i + 1}. {rows_day[i]}')
        print()
    elif select == 2:
        n = 0
        week_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                     3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                     6: 'Sunday'}
        while n != 7:
            day = today + timedelta(days=n)
            rows_day = session.query(Table).filter(Table.deadline == day.date()).all()
            if len(rows_day) == 0:
                print(f'\n{week_days[day.weekday()]} {day.day} {day.strftime("%b")}\nNothing to do!')
            else:
                print(f'\n{week_days[day.weekday()]} {day.day} {day.strftime("%b")}')
                for i in range(0, len(rows_day)):
                    print(f'{i+1}. {rows_day[i]}')
            n += 1
        print('')
    elif select == 3:
        print('All tasks:')
        z = 0
        count = 1
        while z != len(rows) + 1:
            day = today + timedelta(days=z)
            rows_day = session.query(Table).filter(Table.deadline == day.date()).all()
            if len(rows_day) > 0:
                for i in range(0, len(rows_day)):
                    print(f'{count}. {rows_day[i]}. {day.day} {day.strftime("%b")}')
                    count += 1
            z += 1
        print()
    elif select == 4:
        print('Missed tasks:')
        rows_miss = session.query(Table).filter(Table.deadline < datetime.today()).all()
        rows_miss_t = session.query(Table.deadline).filter(Table.deadline < datetime.today()).all()
        ss = rows_miss_t[0]
        if len(rows_miss) > 0:
            for i in range(0, len(rows_miss)):
                print(f'{i + 1}. {rows_miss[i]}. {rows_miss_t[i][0].day} {rows_miss_t[i][0].strftime("%b")}')
        else:
            print('Missed tasks:\nNothing is missed!')
        print()
    elif select == 5:
        task1 = input('Enter task\n> ')
        deadline1 = input('Enter deadline\n> ')
        new_row = Table(task=task1, deadline=datetime.strptime(deadline1, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print('The task has been added!')
    elif select == 6:
        print('Chose the number of the task you want to delete:')
        z = 0
        count = 1
        rows_day = session.query(Table).order_by(Table.deadline).all()
        day = today + timedelta(days=z)
        if len(rows_day) > 0:
            for i in rows_day:
                print(f'{count}. {i}. {day.day} {day.strftime("%b")}')
                count += 1
        del_task = int(input('> '))
        specific_row = rows_day[del_task - 1]
        session.delete(specific_row)
        session.commit()
        print('The task has been deleted!')
    elif select == 0:
        print('\nBye!')
        break
