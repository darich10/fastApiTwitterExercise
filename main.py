# Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# fastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()


# Models
class UserBase(BaseModel):
    userID: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)


class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8
    )


class Tweet(BaseModel):
    tweetID: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operations

# # Users
# # # Register user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
async def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
        - Request body parameter
            - user: UserRegister

    Return a json with the basic user information
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - birth_day: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["userID"] = str(user_dict["userID"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

# # # Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
async def login():
    pass


# # # Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all User",
    tags=["Users"]
)
async def show_all_users():
    """
    Show all users

    This path operation show all users registered in the app

    Parameters:
        -

    Returns a json list with all users in the app, with the following keys:

    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - birth_day: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

# # # Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
async def show_user():
    pass


# # # Delete a user
@app.delete(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
async def delete_user():
    pass


# # # Update a user
@app.put(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
async def update_user():
    pass


# # Tweet
# # # Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
async def home():
    """
    Show all tweets

    This path operation show all users registered in the app

    Parameters:
        -

    Returns a json list with all tweets in the app, with the following keys:

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


# # # Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweets",
    tags=["Tweets"]
)
async def post_tweet(tweet: Tweet = Body(...)):
    """
    Post Tweet

    This operation path posrt a tweet in the app

    Parameters:
        - Request body parameter
            - tweet: Tweet

    Returns a json with the tweet information posted.
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweetID"] = str(tweet_dict["tweetID"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["by"]["userID"] = str(tweet_dict["by"]["userID"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        if tweet_dict["updated_at"]:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


# # # Show a tweet
@app.get(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
async def show_tweet():
    pass


# # # Delete a tweet
@app.delete(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
async def delete_tweet():
    pass


# # # Delete a tweet
@app.put(
    path="/tweet/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
async def update_tweet():
    pass
