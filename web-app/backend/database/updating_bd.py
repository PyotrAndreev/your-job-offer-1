from sqlalchemy.orm import sessionmaker
from .models import Updates, engine

Session = sessionmaker(bind=engine)
session = Session()

def add_agregator(agregator_name):
    session.add(Updates(agregator=agregator_name))
    session.commit()

add_agregator("head hunter") ## айдишник hh - 1
add_agregator("habr career") ## айдишник hc - 2
add_agregator("superjob") ## айдишник sj - 3
add_agregator("zarplate") ## айдишник zp - 4

def update_time(agregator_id, time):
    update_info = session.query(Updates).filter_by(update_id=agregator_id).first()
    if update_info:
        update_info.updated_at = time
        session.commit()

def get_last_update(agregator_id):
    update_info = session.query(Updates).filter_by(update_id=agregator_id).first()
    if update_info:
        return update_info.updated_at
