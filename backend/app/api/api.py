from fastapi import FastAPI, HTTPException, Body, Depends
from contextlib import asynccontextmanager

from pydantic import BaseModel, HttpUrl
from database_config import DatabaseConnection, db_session  

from db.website import Website, URL
from models.models import URLPayload, AttackPayload, Attack
from utils.utils import extract_domain_from_url


from logging_config import loggers

app = FastAPI()
logger = loggers["api"]

from fastapi import HTTPException
from sqlalchemy.orm import Session



@app.post("/url")
async def post_url(payload: URLPayload):
    """
    Endpoint to add a new URL to the database.
    
    Args:
    - payload (URLPayload): The payload containing the URL data.

    Returns:
    - dict: A dictionary containing the saved URL.

    Raises:
    - HTTPException: If there's an error while saving the URL to the database.
    """
    
    url_str = str(payload.url)
    logger.info(f"Received URL {url_str}")
    
    try:
        website_domain = extract_domain_from_url(url_str)
        
        async with db_session() as db:
            # Create or get existing website
            website = await Website.get_by_domain(db, website_domain)
            if not website:
                website = await Website.create(db, domain=website_domain)
            
            # create the ``URL`` object
            url = await URL.create(db=db, website_id=website.id, url=url_str)

    except Exception as e:
        logger.error(f"Failed to save URL {url} to database. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save URL to database.")

    return {
            "websiteDomain": website_domain,
            "url": url.url,
            "websiteId": url.website_id
            }


@app.get("/attacks")
async def get_attacks():
    return [
        {"id": 1, "name": "XSS", "description": "Cross Site Scripting"},
        {"id": 2, "name": "SQL Injection", "description": "Database Injection Attack"}
    ]

@app.post("/attacks")
async def post_attack(payload: AttackPayload):
    return {"selected_attacks": payload.selected_attacks, "details": payload.details}

@app.get("/data")
async def get_data():
    # TODO: Integrate with the database to fetch all necessary data.
    return {
        "urls": ["https://example.com"],
        "attacks": [
            {"id": 1, "name": "XSS", "description": "Cross Site Scripting"},
            {"id": 2, "name": "SQL Injection", "description": "Database Injection Attack"}
        ],
        "attack_details": [
            {"attack_id": 1, "details": "Details about attack 1"},
            {"attack_id": 2, "details": "Details about attack 2"}
        ]
    }
