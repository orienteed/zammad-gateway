from fastapi import APIRouter, Header, Body
from dotenv import load_dotenv
import requests
import os

load_dotenv()

router = APIRouter()

@router.get('/by_ticket/{ticketId}')
def getTicketThread(ticketId):
    return "hola"

@router.post('/')
def sendComment():
    return "hola"