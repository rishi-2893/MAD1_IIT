import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import select

from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# should be same as in sqlite
class User(Base):
    __tablename__ = 'user' 
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)



class Article(Base):
    __tablename__ = 'article'
    article_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    authors = relationship("User", secondary="article_authors")



class ArticleAuthors(Base):
    __tablename__ = 'article_authors'
    user_id = Column(Integer,   ForeignKey("user.user_id"), primary_key=True, nullable=False)
    article_id = Column(Integer,  ForeignKey("article.article_id"), primary_key=True, nullable=False) 


# pass relative path to the database
engine = create_engine("sqlite:///./testdb.sqlite3")



if __name__ == '__main__':
    with Session(engine, autoflush=False) as session:
        session.begin()
        try:
            author1 = session.query(User).filter(User.username == "rishi").one()
            author2 = session.query(User).filter(User.username == "raj").one()

            article = Article(title="2nd Using relationship", content="2nd Use relationships to insert. It's easy")

            article.authors.append(author1)
            article.authors.append(author2)
            session.add(article)

        except:
            print("Exception, rolling back")
            session.rollback()
            raise
        
        else:
            print("No exceptions, hence commit")
            session.commit()   
