import asyncio
import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, Text

# Определяем базовый класс для SQLAlchemy
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

# Соединение с базой данных (асинхронное)
DATABASE_URL = "sqlite+aiosqlite:///starwars.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Функция для получения данных о персонаже
async def fetch_character(session, character_id):
    url = f"https://swapi.dev/api/people/{character_id}/"
    async with session.get(url) as response:
        return await response.json()

# Функция для загрузки данных в базу
async def save_character(session, character_data):
    character = Character(
        id=character_data['id'],
        birth_year=character_data['birth_year'],
        eye_color=character_data['eye_color'],
        films=','.join([film.split('/')[-2] for film in character_data['films']]),
        gender=character_data['gender'],
        hair_color=character_data['hair_color'],
        height=float(character_data['height']) if character_data['height'] else None,
        homeworld=character_data['homeworld'],
        mass=float(character_data['mass']) if character_data['mass'] else None,
        name=character_data['name'],
        skin_color=character_data['skin_color'],
        species=','.join([species.split('/')[-2] for species in character_data['species']]),
        starships=','.join([starship.split('/')[-2] for starship in character_data['starships']]),
        vehicles=','.join([vehicle.split('/')[-2] for vehicle in character_data['vehicles']])
    )

    async with session.begin():
        session.add(character)

# Функция для загрузки всех персонажей
async def load_all_characters():
    async with aiohttp.ClientSession() as session:
        async with SessionLocal() as db_session:
            character_id = 1
            while True:
                character_data = await fetch_character(session, character_id)
                if 'detail' in character_data and character_data['detail'] == 'Not found':
                    break  # Выход, если персонаж не найден

                # Добавление ID персонажа
                character_data['id'] = character_id
                await save_character(db_session, character_data)
                
                print(f"Character {character_data['name']} saved to DB.")
                character_id += 1

# Запуск загрузки данных
if __name__ == "__main__":
    asyncio.run(load_all_characters())
