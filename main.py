import sys, os
from ensta import Guest
from utils import get_media_type
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import time
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('app.log'),  # Logs to a file
                              logging.StreamHandler()])        # Logs to the console
logger = logging.getLogger(__name__)

# region load .env data
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
# endregion load .env data

# Configurazione database

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Definizione delle tabelle
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)


class AccountHistory(Base):
    __tablename__ = 'account_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    follower_count = Column(Integer)
    following_count = Column(Integer)
    total_post_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    post_id = Column(String(50), unique=True, nullable=False)


class PostHistory(Base):
    __tablename__ = 'post_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    media_type = Column(String(50))
    posted_at = Column(DateTime)
    comment_count = Column(Integer)
    like_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Creazione delle tabelle
Base.metadata.create_all(engine)


# Funzione principale per aggiornare i dati
def update_data(username):
    guest = Guest()
    profile = guest.profile(username)
    #logger.debug(profile)

    session = Session()

    # Creazione dei dati dell'account se non esiste
    db_account = session.query(Account).filter_by(username=username).first()
    if not db_account:
        db_account = Account(username=username)
        session.add(db_account)
        session.commit()  # Necessario per generare l'id

    # Inserimento dei dati storici dell'account
    account_history = AccountHistory(
        account_id=db_account.id,
        follower_count=profile.follower_count,
        following_count=profile.following_count,
        total_post_count=profile.total_post_count,
        timestamp=datetime.utcnow()
    )
    session.add(account_history)
    session.commit()

    # Creazione o aggiornamento dei dati dei post
    posts = guest.posts(username)
    # logger.debug(posts)
    for post in posts:
        logger.debug(post)
        post_id = post.post_id
        db_post = session.query(Post).filter_by(post_id=post_id).first()
        if not db_post:
            db_post = Post(account_id=db_account.id, post_id=post_id)
            session.add(db_post)
            session.commit()  # Necessario per generare l'id

        # Inserimento dei dati storici del post
        post_history = PostHistory(
            post_id=db_post.id,
            media_type=get_media_type(post.media_type),
            posted_at=datetime.fromtimestamp(post.taken_at),
            comment_count=post.comment_count,
            like_count=post.like_count,
            timestamp=datetime.utcnow()
        )
        session.add(post_history)

    session.commit()
    session.close()

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        print("Usage: python main.py <account1> <account2> ...")
        sys.exit(1)

    for arg in args[1:]:
        logger.info(f'Downloading {arg} data')
        update_data(arg)

    # update_data("ig_username_example")
