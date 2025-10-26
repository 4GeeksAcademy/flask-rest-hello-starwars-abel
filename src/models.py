from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorite_characters: Mapped[list['FavoriteCharacter']] = relationship(
        back_populates='user')
    favorite_planets: Mapped[list['FavoritePlanet']
                             ] = relationship(back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mass: Mapped[int | None] = mapped_column(Integer, nullable=True)
    favorites: Mapped[list['FavoriteCharacter']
                      ] = relationship(back_populates='character')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str | None] = mapped_column(String(80), nullable=True)
    population: Mapped[int | None] = mapped_column(Integer, nullable=True)
    favorites: Mapped[list['FavoritePlanet']
                      ] = relationship(back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
        }


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey('character.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='favorite_characters')
    character: Mapped['Character'] = relationship(back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planet.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='favorite_planets')
    planet: Mapped['Planet'] = relationship(back_populates='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }


if __name__ == '__main__':
    render_er(db.Model, 'diagram.png')
