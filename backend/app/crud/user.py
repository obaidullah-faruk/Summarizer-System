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