from sqlmodel import select
from app.models.user import User

def check_user_exists(email, session):
    user_exits = session.exec(select(User).where(User.email == email)).first()
    return user_exits


def create_user(email:str, password: str, session):
    user = User(
        email = email,
        password_hash = password
    )
    session.add(user)
    session.commit()
    return user

def get_password(email: str, session):
    statement = select(User.password_hash, User.id).where(User.email==email)
    results = session.exec(statement)
    user_pass = results.first()
    return user_pass