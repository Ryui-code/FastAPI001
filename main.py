from fastapi import FastAPI
from fstsite.api import users, category, product, review
app = FastAPI()

app.include_router(users.users_router)
app.include_router(category.categories_router)
app.include_router(review.reviews_router)
app.include_router(product.products_router)