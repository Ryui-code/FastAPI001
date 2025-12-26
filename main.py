import uvicorn
from fastapi import FastAPI
from fstsite.api import users
app = FastAPI(title='fstsite')

app.include_router(users.users_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)