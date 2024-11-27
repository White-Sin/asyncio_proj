from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Определяем базовый класс
Base = declarative_base()

# Описание модели персонажа
class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, autoincrement=False)
    birth_year = Column(String(50))
    eye_color = Column(String(50))
    films = Column(Text)
    gender = Column(String(50))
    hair_color = Column(String(50))
    height = Column(Float)
    homeworld = Column(String(255))
    mass = Column(Float)
    name = Column(String(255))
    skin_color = Column(String(50))
    species = Column(Text)
    starships = Column(Text)
    vehicles = Column(Text)

# Соединение с базой данных
DATABASE_URL = "sqlite:///starwars.db"  # Здесь можно использовать другой URL для подключения к базе
engine = create_engine(DATABASE_URL, echo=True)

# Создание всех таблиц
def create_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()
