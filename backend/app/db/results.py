import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from .base import Base


class AttackResult(Base):
    """
    Represents the result of an attack on a specific ``URL`` or ``InputField``.

    :id: The primary key identifier for the attack result.
    :website_id: The identifier of the website being attacked.
    :url_id: The identifier of the URL being attacked.
    :input_field_id: The identifier of the input field being attacked (if applicable).
    :attack_id: The identifier of the type of attack performed.
    :was_successful: Indicates whether the attack was successful.
    :timestamp: The date and time the attack was executed.
    :details: Details about the attack, such as payloads used, server response, etc.

    Example:
    --------
    attack_result = AttackResult(website_id=1, url_id=1, input_field_id=1,
                                 attack_id=1, was_successful=True, details="Script executed successfully.")
    """

    __tablename__ = "attack_results"
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    url_id = Column(Integer, ForeignKey("urls.id"))
    input_field_id = Column(Integer, ForeignKey("input_fields.id"))
    attack_id = Column(Integer, ForeignKey("attacks.id"))
    was_successful = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(String)
