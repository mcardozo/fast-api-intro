"""Main module."""

from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def home():
    """Home page."""
    return {'hello': 'world'}
