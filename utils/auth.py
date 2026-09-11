# @Author: Sheep Wang
# @File: auth.py
# @Created: 2026-09-01 22:37
# @Description: auth.py



from utils.jwt import jwt_util
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials




# FastAPI support tool to get Header certificate
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    # Auth dependency: extract and validate the token, return username on success, raise 401 on failure
    token = credentials.credentials
    payload = jwt_util.verify_token(token)


    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            datails="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return payload["username"]

# def login_required(func):
#     @wraps(func)
#     def wrapper(*args, **kargs):
#         # Get "Authorization" from request header
#         auth_header = request.headers.get("Authorization")

#         # Request header not contains "Authorization"
#         if not auth_header:
#             return jsonify({
#                 "message": "Missing Authorizaton of header"
#             }), 401

#         # Not start as "Bearer" in "Authorization" of header
#         if not auth_header.startswith("Bearer "):
#             return jsonify({
#                 "message": "Invalid Authorization of header"
#             })

#         # If Authorization is correct
#         # Get token value
#         token = auth_header[7:]

#         # Decode token
#         payload = jwt_util.verify_token(token)

#         # Decoding token is incorrect
#         if payload is None:
#             return jsonify({
#                 "message": "Invalid or expired token"
#             }), 401

#         # username
#         kargs["username"] = payload["username"]

#         return func(*args, **kargs)
    
#     return wrapper