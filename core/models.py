from typing import Optional, Set
from datetime import date, datetime
from sqlalchemy import Integer, Date, DateTime, String, CHAR, UniqueConstraint, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .database import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    username : Mapped[str] = mapped_column(String(20))
    date_birth : Mapped[date] = mapped_column(Date)
    datetime_register : Mapped[date] = mapped_column(DateTime)
    pass_salt : Mapped[str] = mapped_column(CHAR(16))
    pass_hash : Mapped[str] = mapped_column(CHAR(64))
    role : Mapped[str] = mapped_column(String(10))
    contact_email : Mapped[Optional[str]] = mapped_column(String(50))
    contact_phone : Mapped[str] = mapped_column(CHAR(11))

    __table_args__ = (
        UniqueConstraint("username"),
    )

    color_preferences : Mapped[Optional[Set["ColorPreference"]]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    personality_preferences : Mapped[Optional[Set["PersonalityPreference"]]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    adoptions : Mapped[Optional[Set["Adoption"]]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    rescues : Mapped[Optional[Set["Rescue"]]] = relationship(back_populates="user")

    sent_messages : Mapped[Optional[Set["Message"]]] = relationship(back_populates="sender")
    received_messages : Mapped[Optional[Set["Message"]]] = relationship(back_populates="receiver")

    def __repr__(self):
        return f"""
        User (
            id={self.id!r},
            name={self.name!r},
            username={self.username!r},
            date_birth={self.date_birth},
            pass_salt={self.pass_salt!r},
            pass_hash={self.pass_hash!r},
            role={self.role!r},
            contact_email={self.contact_email!r},
            contact_phone={self.contact_phone!r}
        )
        """


class Cat(Base):
    __tablename__ = "cats"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    age : Mapped[int] = mapped_column(SmallInteger)
    sex : Mapped[str] = mapped_column(CHAR(1))

    adoption : Mapped[Optional["Adoption"]] = relationship(
        back_populates="cat", cascade="all, delete-orphan",
    )

    vaccinations : Mapped[Optional[Set["Vaccination"]]] = relationship(
        back_populates="cat", cascade="all, delete-orphan",
    )

    cat_diseases : Mapped[Optional[Set["CatDisease"]]] = relationship(
        back_populates="cat", cascade="all, delete-orphan",
    )

    cat_colors : Mapped[Set["CatColor"]] = relationship(
        back_populates="cat", cascade="all, delete-orphan",
    )

    cat_personalities : Mapped[Set["CatPersonality"]] = relationship(
        back_populates="cat", cascade="all, delete-orphan",
    )

    physical_description : Mapped["PhysicalDescription"] = relationship(
        back_populates="cat", cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"""
        Cat (
            id={self.id!r},
            name={self.name!r},
            age={self.age!r},
            sex={self.sex!r}
        )
        """


class Disease(Base):
    __tablename__ = "diseases"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    description : Mapped[Optional[str]] = mapped_column(String(1024))

    vaccine : Mapped[Optional["Vaccine"]] = relationship(back_populates="diseases")
    cat_diseases : Mapped[Optional[Set["CatDisease"]]] = relationship(
        back_populates="disease",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"""
        Disease (
            id={self.id!r},
            name={self.name!r},
            description={self.description!r}
        )
        """


class Personality(Base):
    __tablename__ = "personalities"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(30))
    description : Mapped[str] = mapped_column(String(1024))

    personality_preferences : Mapped[Optional[Set["PersonalityPreference"]]] = relationship(
        back_populates="personality", cascade="all, delete-orphan",
    )

    cat_personalities : Mapped[Optional[Set["CatPersonality"]]] = relationship(
        back_populates="personality", cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"""
        Personality (
            id={self.id!r},
            name={self.name!r},
            description={self.description!r}
        )
        """


class Color(Base):
    __tablename__ = "colors"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(10))

    color_preferences : Mapped[Optional[Set["ColorPreference"]]] = relationship(
        back_populates="color",
        cascade="all, delete-orphan",    
    )

    cat_colors : Mapped[Optional[Set["CatColor"]]] = relationship(
        back_populates="color", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"""
        Color (
            id={self.id!r},
            name={self.name!r}
        )
        """


class CatDisease(Base):
    __tablename__ = "cat_diseases"

    cat_id : Mapped[int] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    disease_id : Mapped[int] = mapped_column(ForeignKey("diseases.id"), primary_key=True)

    cat : Mapped["Cat"] = relationship(back_populates="cat_diseases")
    disease : Mapped["Disease"] = relationship(back_populates="cat_diseases")

    def __repr__(self):
        return f"""
        CatDisease (
            cat_id={self.cat_id!r},
            disease_id={self.disease_id!r}
        )
        """


class CatColor(Base):
    __tablename__ = "cat_colors"

    cat_id : Mapped[int] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    color_id : Mapped[int] = mapped_column(ForeignKey("colors.id"), primary_key=True)

    cat : Mapped["Cat"] = relationship(back_populates="cat_colors")
    color : Mapped["Color"] = relationship(back_populates="cat_colors")

    def __repr__(self):
        return f"""
        CatColor (
            cat_id={self.cat_id!r},
            color_id={self.color_id!r}
        )
        """


class CatPersonality(Base):
    __tablename__ = "cat_personalities"

    cat_id : Mapped[int] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    personality_id : Mapped[int] = mapped_column(ForeignKey("personalities.id"), primary_key=True)

    cat : Mapped["Cat"] = relationship(
        back_populates="cat_personalities",
    )

    personality : Mapped["Personality"] = relationship(
        back_populates="cat_personalities",
    )

    def __repr__(self):
        return f"""
        CatPersonality (
            cat_id={self.cat_id!r},
            personality_id={self.personality_id!r}
        )
        """


class Vaccine(Base):
    __tablename__ = "vaccines"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(50))
    description : Mapped[Optional[str]] = mapped_column(String(1024))
    disease_id : Mapped[int] = mapped_column(ForeignKey("diseases.id"))

    diseases : Mapped[Set["Disease"]] = relationship(back_populates="vaccine")
    vaccinations : Mapped[Optional[Set["Vaccination"]]] = relationship(back_populates="vaccine")

    def __repr__(self):
        return f"""
        Vaccine (
            id={self.id!r},
            name={self.name!r},
            description={self.description!r},
            disease_id={self.disease_id!r}
        )
        """


class Preference(Base):
    __abstract__ = True # Abstract Class

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class ColorPreference(Preference):
    __tablename__ = "color_preferences"

    color_id : Mapped[int] = mapped_column(ForeignKey("colors.id"), primary_key=True)

    user : Mapped["User"] = relationship(back_populates="color_preferences")
    color : Mapped["Color"] = relationship(back_populates="color_preferences")

    def __repr__(self):
        return f"""
        ColorPreference (
            id={self.id!r}
            user_id={self.user_id!r},
            choice_datetime={self.choice_datetime!r},
            type={self.type!r}
            color_id={self.color_id!r}
        )
        """
    

class PersonalityPreference(Preference):
    __tablename__ = "personality_preferences"

    personality_id : Mapped[int] = mapped_column(ForeignKey("personalities.id"), primary_key=True)

    user : Mapped["User"] = relationship(back_populates="personality_preferences")
    personality : Mapped["Personality"] = relationship(back_populates="personality_preferences")

    def __repr__(self):
        return f"""
        PersonalityPreference (
            id={self.id!r}
            user_id={self.user_id!r},
            choice_datetime={self.choice_datetime!r},
            type={self.type!r}
            personality_id={self.personality_id!r},
        )
        """


class Rescue(Base):
    __tablename__ = "rescues"

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    request_datetime : Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    status : Mapped[str] = mapped_column(String(50))
    closure_datetime : Mapped[Optional[int]] = mapped_column(SmallInteger)
    description : Mapped[str] = mapped_column(String(1024))
    addr_city : Mapped[str] = mapped_column(String(50))
    addr_state : Mapped[str] = mapped_column(String(100))
    addr_street : Mapped[str] = mapped_column(String(100))
    addr_number : Mapped[int] = mapped_column(Integer)
    addr_zipcode : Mapped[str] = mapped_column(CHAR(8)) # CEP

    user : Mapped["User"] = relationship(back_populates="rescues")

    def __repr__(self):
        return f"""
        Rescue (
            user_id={self.user_id!r},
            request_datetime={self.request_datetime!r},
            status={self.status!r},
            description={self.description!r},
            addr_city={self.addr_city!r},
            addr_state={self.addr_state!r},
            addr_number={self.addr_number!r},
            addr_zipcode={self.addr_zipcode!r}
        )
        """


class Adoption(Base):
    __tablename__ = "adoptions"

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    cat_id : Mapped[int] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    request_datetime : Mapped[datetime] = mapped_column(DateTime)
    hand_over_datetime : Mapped[Optional[datetime]] = mapped_column(DateTime)
    status : Mapped[str] = mapped_column(String(20))

    user : Mapped["User"] = relationship(back_populates="adoptions")
    cat : Mapped["Cat"] = relationship(back_populates="adoption")

    def __repr__(self):
        return f"""
        Adoption (
            user_id={self.user_id!r},
            cat_id={self.cat_id!r},
            request_datetime={self.request_datetime!r},
            hand_over_datetime={self.hand_over_datetime!r},
            status={self.status!r}
        )
        """


class PhysicalDescription(Base):
    __tablename__ = "physical_description"

    cat_id : Mapped[int] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    description : Mapped[str] = mapped_column(String(1024))

    cat : Mapped["Cat"] = relationship(back_populates="physical_description")

    def __repr__(self):
        return f"""
        PhysicalDescription (
            cat_id={self.cat_id!r},
            description={self.description!r}
        )
        """
    

class Message(Base):
    __tablename__ = "messages"

    sender_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    receiver_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    sent_datetime : Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    content : Mapped[str] = mapped_column(String(2000))
    status : Mapped[str] = mapped_column(String(20))

    sender : Mapped["User"] = relationship(back_populates="sent_messages")
    receiver : Mapped["User"] = relationship(back_populates="received_messages")

    def __repr__(self):
        return f"""
        Message (
            sender_id={self.sender_id!r},
            receiver_id={self.receiver_id!r},
            content={self.content!r},
            sent_datetime={self.sent_datetime!r}
        )
        """


class Vaccination(Base):
    __tablename__ = "vaccinations"

    cat_id : Mapped[int] = mapped_column(ForeignKey("cats.id"), primary_key=True)
    vaccine_id : Mapped[int] = mapped_column(ForeignKey("vaccines.id"), primary_key=True)
    dose : Mapped[str] = mapped_column(CHAR(3))
    appl_date : Mapped[date] = mapped_column(Date)
    next_date : Mapped[Optional[date]] = mapped_column(Date)
    
    cat : Mapped["Cat"] = relationship(back_populates="vaccinations")
    vaccine : Mapped["Vaccine"] = relationship(back_populates="vaccinations")

    def __repr__(self):
        return f"""
        Vaccination (
            cat_id={self.cat_id!r},
            vaccine_id={self.vaccine_id!r},
            dose={self.dose!r},
            appl_datetime={self.appl_datetime!r},
            next_datetime={self.next_datetime!r}
        )
        """
