from typing import Optional, Set
from datetime import date, datetime
from sqlalchemy import Integer, Date, DateTime, String, CHAR, UniqueConstraint, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .database import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    username : Mapped[str] = mapped_column(String)
    date_birth : Mapped[date] = mapped_column(Date)
    pass_hash : Mapped[str] = mapped_column(CHAR(64))
    role : Mapped[str] = mapped_column(String(10))
    contact_email : Mapped[Optional[str]] = mapped_column(String(50))
    contact_phone : Mapped[str] = mapped_column(CHAR(11))

    __table_args__ = (
        UniqueConstraint("username"),
    )

    user_preferences : Mapped[Set["UserPreference"]] = relationship(
        back_populates="user", cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"""
        User (
            id={self.id!r},
            name={self.name!r},
            username={self.username!r},
            date_birth={self.date_birth},
            pass_hash={self.pass_hash!r},
            role={self.role!r},
            contact_email={self.contact_email!r},
            contact_phone={self.contact_phone!r}
        )
        """

class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    color_id : Mapped[int] = mapped_column(ForeignKey("cat_colors.id"))
    personality_id : Mapped[int] = mapped_column(ForeignKey("personalities.id"))
    age : Mapped[Optional[int]] = mapped_column(SmallInteger)

    user : Mapped["User"] = relationship(
        back_populates="user_preferences",
    )

    def __repr__(self):
        return f"""
        UserPreference (
            user_id={self.user_id!r},
            color_id={self.color_id!r},
            personality_id={self.personality_id},
            age={self.age!r}
        )
        """

