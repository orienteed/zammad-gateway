from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def getCustomer():
    return "hola get"


@router.post('/')
def createCustomer():
    return "hola post"
