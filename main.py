import uvicorn
from fastapi import FastAPI
from fstsite.api import users, category, product, review
app = FastAPI(title='fstsite')

app.include_router(users.users_router)
app.include_router(category.categories_router)
app.include_router(review.reviews_router)
app.include_router(product.products_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)