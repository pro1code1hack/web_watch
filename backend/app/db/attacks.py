from app.db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Attack(Base):
    """A class to represent an attack type.

    Attributes:
        id (int): The primary key.
        name (str): Name of the attack (e.g., XSS, SQL Injection).
        description (str): A brief description of the attack.
        results (list): A list of results for this attack type.

    Example:
        xss_attack = Attack(name="XSS", description="Cross Site Scripting attack")
    """
    __tablename__ = 'attacks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    results = relationship("AttackResult", backref="attack")
