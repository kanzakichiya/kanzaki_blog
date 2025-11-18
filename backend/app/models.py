# backend/app/models.py
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

# === 1. BASE MODELS ===
# 先定义所有基础模型
class TagBase(SQLModel):
    name: str = Field(unique=True, index=True)

class PostBase(SQLModel):
    title: str
    content: str
    summary: Optional[str] = None

class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: Optional[str] = None


# === 2. LINK TABLE (The "Bridge") ===
# 链接表必须在 Post 和 Tag 之前定义
class PostTagLink(SQLModel, table=True):
    post_id: int = Field(foreign_key="post.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


# === 3. MAIN TABLE MODELS ===
# 现在 Post 和 Tag 可以安全地引用 PostTagLink

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 我们移除了 'posts' 关系以打破循环

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # 这行现在可以正常工作了
    tags: List[Tag] = Relationship(link_model=PostTagLink)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


# === 4. API MODELS (保持不变) ===
# 这些用于 API 验证和响应
class TagCreate(TagBase):
    pass

class TagRead(TagBase):
    id: int

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class PostCreate(PostBase):
    tags: List[int] = [] 

class PostRead(PostBase):
    id: int
    created_at: datetime
    tags: List[TagRead] = []

class PostReadWithTags(PostRead):
    pass