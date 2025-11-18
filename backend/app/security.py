# backend/app/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional

# --- 1. 密码加密设置 ---

# --- 2. JWT 令牌设置 ---
# a. 一个私密的密钥 (这个值应该保密，不要泄露)
SECRET_KEY = "YOUR_SUPER_SECRET_KEY_CHANGE_ME"
# b. 加密算法
ALGORITHM = "HS256"
# c. 令牌有效期 (例如 30 天)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30 

# --- 3. OAuth2 方案 ---
# 告诉 FastAPI 从哪个 URL 获取 token (等下我们会创建这个 /token 接口)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- 4. 辅助函数 ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码和哈希密码是否匹配"""
    # bcrypt限制密码长度为72字节，需要截断
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def get_password_hash(password: str) -> str:
    """生成密码的哈希值"""
    # bcrypt限制密码长度为72字节，需要截断
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建 JWT 令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[str]:
    """
    解码令牌，返回用户名 (subject)
    如果解码失败 (过期或无效)，抛出异常
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None