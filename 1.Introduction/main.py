from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

posts = [{
"id":1,
"title":"Un dia soleado",
"content":"Hoy fue un dia hermoso",
"publish":True,
"rating":10},
{
"id":2,
"title":"Un dia nublado",
"content":"Hoy fue un dia hermoso",
"publish":True,
"rating":5}
]

@app.get("/posts")
def get_posts():
    return posts

@app.get("/posts/lastest")
def get_last_post():
    return posts[-1]

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    for post in posts:
        if post["id"] == id:
            response.status_code = status.HTTP_200_OK
            return {"post_detail":post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = random.randint(3,9999)
    posts.append(post_dict)

    return post.model_dump()

@app.delete("/posts/{id}")
def delete_post(id:int):
    for post in posts.copy():
        if post["id"] == id:
            posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

@app.put("/posts/{id}", status_code= status.HTTP_200_OK)
def modify_post(id:int, new_post: Post):
    new_post_dict = new_post.model_dump()
    new_post_dict["id"] = id

    for index, post in enumerate(posts.copy()):
        if post["id"] == id:
            posts[index] = new_post_dict
            return {"message": "updated post"}

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
