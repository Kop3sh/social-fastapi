from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import user, post, auth, vote


# to make sa setup first db
# models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World!!!!!!!!!!!!!"}


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])        
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
app.include_router(vote.router, prefix="/vote", tags=["Votes"])