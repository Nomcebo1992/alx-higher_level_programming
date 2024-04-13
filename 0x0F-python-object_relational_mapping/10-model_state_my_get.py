#!/usr/bin/python3

"""
Module to list all State objects from the database hbtn_0e_6_usa
with the name passed as argument
"""

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from model_state import Base, State
    from sys import argv as arg

    engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'.
                           format(arg[1], arg[2],
                                  arg[3]), pool_pre_ping=True)

    Session = sessionmaker(bind=engine)

    session = Session()

    state = session.query(State).filter(State.name == arg[4]).first()

    if state is None:
        print("Not found")
    else:
        print("{}".format(state.id))

    session.close()
