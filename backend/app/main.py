from fastapi import (
    FastAPI, Depends, HTTPException, status, 
    File, UploadFile
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, SQLModel # 1. 确保 SQLModel 被导入
from sqlalchemy.orm import selectinload
from typing import List
import os # 2. 确保 os 被导入
import uuid

from .database import create_db_and_tables, get_session, engine # 3. 确保 engine 被导入
from .models import (
    Post, PostCreate, PostRead, PostBase,
    User, UserCreate, UserRead,
    Tag, TagCreate, TagRead, PostReadWithTags,
    PostTagLink
)
from .security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    decode_token,
    oauth2_scheme
)

app = FastAPI()

# --- CORS ---
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 静态文件目录 ---
os.makedirs("static/images", exist_ok=True) 
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- 启动事件 (自动创建管理员) ---
@app.on_event("startup")
def on_startup():
    # a. 创建数据库表
    create_db_and_tables()

    # b. 从环境变量读取管理员配置
    ADMIN_USER = os.environ.get("ADMIN_USER")
    ADMIN_PASS = os.environ.get("ADMIN_PASSWORD")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")

    if ADMIN_USER and ADMIN_PASS:
        # c. 使用一个临时的数据库会话
        with Session(engine) as session: # 确保 engine 已导入
            # d. 检查管理员是否已存在
            user = session.exec(select(User).where(User.username == ADMIN_USER)).first()
            if not user:
                print(f"创建默认管理员: {ADMIN_USER}")
                hashed_password = get_password_hash(ADMIN_PASS)
                db_user = User(
                    username=ADMIN_USER, 
                    email=ADMIN_EMAIL, 
                    hashed_password=hashed_password
                )
                session.add(db_user)
                session.commit()
            else:
                print(f"管理员 {ADMIN_USER} 已存在")
    else:
        print("未配置 ADMIN_USER 或 ADMIN_PASSWORD，跳过创建管理员")


# === 认证和用户 ===
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的 Token")
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在")
    return user

@app.post("/users", response_model=UserRead, tags=["Auth"])
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已被注册")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.post("/token", tags=["Auth"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserRead, tags=["Auth"])
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# === 图片上传 ===
@app.post("/upload-image", tags=["Posts"])
async def upload_image(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join("static/images", unique_filename)
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {e}")
    
    # 修复：返回相对路径，由 Nginx 处理
    url = f"/static/images/{unique_filename}"
    return {"url": url}

# === 标签接口 ===
@app.post("/tags", response_model=TagRead, tags=["Tags"])
def create_tag(tag: TagCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    existing_tag = session.exec(select(Tag).where(Tag.name == tag.name)).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="标签已存在")
    db_tag = Tag.from_orm(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@app.get("/tags", response_model=List[TagRead], tags=["Tags"])
def read_tags(session: Session = Depends(get_session)):
    tags = session.exec(select(Tag)).all()
    return tags

@app.get("/tags/{tag_id}", response_model=TagRead, tags=["Tags"])
def read_tag(tag_id: int, session: Session = Depends(get_session)):
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    return db_tag

@app.delete("/tags/{tag_id}", status_code=204, tags=["Tags"])
def delete_tag(tag_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="标签未找到")
    links = session.exec(select(PostTagLink).where(PostTagLink.tag_id == tag_id)).all()
    if len(links) > 0:
        raise HTTPException(status_code=400, detail=f"无法删除：该标签仍被 {len(links)} 篇文章使用。")
    session.delete(db_tag)
    session.commit()
    return None

# === 文章接口 (受保护) ===
@app.post("/posts", response_model=PostRead, tags=["Posts"])
def create_post(post: PostCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    post_base = PostBase(title=post.title, content=post.content, summary=post.summary)
    db_post = Post.from_orm(post_base)
    if post.tags:
        tags = session.exec(select(Tag).where(Tag.id.in_(post.tags))).all()
        db_post.tags = tags
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    _ = db_post.tags 
    return db_post

@app.put("/posts/{post_id}", response_model=PostRead, tags=["Posts"])
def update_post(post_id: int, post_data: PostCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="文章不存在")
    db_post.title = post_data.title
    db_post.content = post_data.content
    db_post.summary = post_data.summary
    if post_data.tags:
        tags = session.exec(select(Tag).where(Tag.id.in_(post_data.tags))).all()
        db_post.tags = tags
    else:
        db_post.tags = []
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    _ = db_post.tags
    return db_post

@app.delete("/posts/{post_id}", status_code=204, tags=["Posts"])
def delete_post(post_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    session.delete(post)
    session.commit()
    return None

# === 新增：站点配置模型 ===
class SiteConfig(SQLModel):
    blog_title: str

# === 新增：站点配置接口 (公开) ===
@app.get("/config", response_model=SiteConfig, tags=["Public"])
def get_site_config():
    # 从 .env 读取我们刚设置的变量，如果没设置，就用 'My Blog' 作为备用
    title = os.environ.get("BLOG_OWNER_NAME", "My Blog")
    return SiteConfig(blog_title=title)


# === 文章接口 (公开) ===
@app.get("/posts", response_model=List[PostRead], tags=["Public"])
def read_posts(session: Session = Depends(get_session)):
    statement = select(Post).options(selectinload(Post.tags))
    posts = session.exec(statement).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostReadWithTags, tags=["Public"])
def read_post(post_id: int, session: Session = Depends(get_session)):
    statement = select(Post).where(Post.id == post_id).options(selectinload(Post.tags))
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章未找到")
    return post

@app.get("/posts/by_tag/{tag_id}", response_model=List[PostRead], tags=["Public"])
def read_posts_by_tag(tag_id: int, session: Session = Depends(get_session)):
    statement = select(Post).where(Post.tags.any(Tag.id == tag_id)).options(selectinload(Post.tags))
    posts = session.exec(statement).all()
    return posts
