# @Author: Sheep Wang
# @File: jwt.py
# @Created: 2026-08-31 21:51
# @Description: jwt.py


from flask import Flask, jsonify, request
from functools import wraps
import jwt, datetime
from config.jwt_config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_HOURS




class JWTUtil:

    # def __init__(self):
        
    #     # Secrect key
    #     self.SECRET_KEY = "gweufhweuhdsuhhweiugcucweucubwcuw"
    #     self.ALGORITHM = "HS256"

    #     # Token validity period
    #     self.TOKEN_EXPIRE_HOURS = 2

        # Connect redis to store backlist
        # r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)



    # the function is generate token 
    def generate_token(self, username: str) -> str:

        # current datetime
        now = datetime.datetime.now(datetime.timezone.utc)

        # payload join expire datet
        payload = {
            "username": username,
            "exp": now + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS),     # Expire time
            "iat": now      # Issue at
        }

        # generate token with payload and secret key
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return token


    # Token validation function
    def verify_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWKError:
            return None


# Initiate a util object, support external part to import
jwt_util = JWTUtil()
