from fastapi import APIRouter

router = APIRouter(prefix='/admin', tags=['Administration'])

@router.get('/users')
def get_users():
    ...