"""
Dependencies
Các dependency có thể inject vào route handlers
"""
from fastapi import Depends, Header, HTTPException, status
from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.core.config import settings

security = HTTPBearer()


async def verify_api_key(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> str:
    """
    Dependency để verify API key
    
    Args:
        x_api_key: API Key từ header X-API-Key
        
    Returns:
        API Key string nếu hợp lệ
        
    Raises:
        HTTPException: Nếu API key không hợp lệ hoặc thiếu
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide X-API-Key header",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    
    return x_api_key


# async def verify_token(authorization: Optional[str] = Header(None)) -> str:
#     """
#     Dependency để verify token (placeholder cho tương lai)
    
#     Args:
#         authorization: Bearer token từ header
        
#     Returns:
#         Token string
        
#     Raises:
#         HTTPException: Nếu token không hợp lệ
#     """
#     # TODO: Implement actual token verification
#     # Hiện tại chỉ là placeholder
#     if authorization is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Missing authentication token"
#         )
#     return authorization


def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None


# async def get_current_user(token: str = Header(None)):
#     """
#     Dependency để lấy user hiện tại từ token (placeholder cho tương lai)
    
#     Args:
#         token: Authentication token
        
#     Returns:
#         User object
#     """
#     # TODO: Implement actual user retrieval from token
#     # Hiện tại chỉ là placeholder
#     return {"user_id": "1", "username": "demo_user"}

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token không hợp lệ"
        )

    return payload


def require_admin():
    """
    Dependency để kiểm tra quyền admin (placeholder cho tương lai)
    """
    # TODO: Implement actual admin check
    pass
