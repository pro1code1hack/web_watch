from db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.future import select
from sqlalchemy.orm import Session, relationship


class Website(Base):
    """
    Represents a website being analyzed.

    :id: An unique identifier for the website.
    :domain: The domain name of the website.
    :urls: List of URLs associated with the website.
    :input_fields: List of input fields found on the website.

    Example:
    website = Website(id=1, domain='example.com')
    """

    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    domain = Column(String, unique=True)

    urls = relationship("URL", backref="website")
    input_fields = relationship("InputField", backref="website")

    # Note: These methods will require an instance of the class

    @classmethod
    async def get_by_domain(cls, db: Session, domain: str):
        result = await db.execute(select(cls).where(cls.domain == domain))
        return result.scalars().first()

    @classmethod
    async def create(cls, db: Session, domain: str):
        website = cls(domain=domain)
        db.add(website)
        await db.flush()
        await db.refresh(website)
        return website


class URL(Base):
    """
    Represents a specific URL on a website.

    :id: An unique identifier for the URL.
    :website_id: Reference to the website this URL belongs to.
    :url: The full URL.

    Example:
    url = URL(id=1, website_id=1, url='https://example.com/page1')
    """

    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    url = Column(String)

    @classmethod
    async def create(cls, db: Session, website_id: int, url: str):
        URL = cls(website_id=website_id, url=url)
        db.add(URL)
        await db.flush()
        await db.refresh(URL)
        return URL


class InputField(Base):
    """
    Represents an input field on a webpage that might be vulnerable to attacks.

    :id: An unique identifier for the input field.
    :website_id: Reference to the website this input field is found on.
    :page_url: The URL where this input field was found. This url can be a subdomain like [https://example.com/page1]
    :input_name: 'name' attribute of the input field.
    :input_type: 'type' attribute of the input field (e.g., 'text', 'password').
    :placeholder: 'placeholder' attribute of the input field.

    Example:
    input_field = InputField(id=1, website_id=1, page_url='https://example.com/page1', input_name='username', input_type='text', placeholder='Enter your username')
    """

    __tablename__ = "input_fields"
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"))
    page_url = Column(String)
    input_name = Column(String)
    input_type = Column(String)
    placeholder = Column(String)
