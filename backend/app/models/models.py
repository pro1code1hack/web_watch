from pydantic import BaseModel, HttpUrl
"""This module represents ``Pydantic`` classes which are going to be used as structures for ``API`` requests """

class Attack(BaseModel):
    id: int
    name: str
    description: str

class URLPayload(BaseModel):
    url: HttpUrl

class AttackPayload(BaseModel):
    selected_attacks: list[int]
    details: str