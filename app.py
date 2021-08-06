import os
from fastapi import FastAPI

from auth import router as auth_router
from tag import router as tag_router
from article import router as article_router

from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://vue3-blog.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=['Auth'])
app.include_router(article_router, tags=['Article'])
app.include_router(tag_router, tags=['Tags'])

register_tortoise(
    app,
    db_url=os.getenv('DB_URL') or 'mysql://root:root@127.0.0.1/v3blog',
    modules={'models': ['auth', 'article', 'tag']},
    generate_schemas=True,
    add_exception_handlers=True
)
