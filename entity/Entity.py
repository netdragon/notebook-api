from datetime import datetime
from typing import Optional

from passlib.apps import custom_app_context as pwd_context
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BaseModule = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModule):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    dname = Column(String(30), nullable=True)
    avatar = Column(String(50), nullable=True)
    password = Column(String(200), nullable=True)
    is_admin = Column(Integer, nullable=True, default=0)
    ctime = Column(DateTime(50), nullable=True, default=datetime.now)
    utime = Column(DateTime(50), nullable=True, default=datetime.now)
    role = Column(String(40), nullable=True)
    disabled = Column(Integer, nullable=True, default=0)
    deleted = Column(Integer, nullable=True, default=0)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


class UserV(BaseModel):
    id: Optional[int] = None
    name: str
    password: Optional[str] = None
    dname: Optional[str] = None
    avatar: Optional[str] = None
    ctime: Optional[str] = None
    utime: Optional[str] = None
    is_admin: Optional[int] = None
    role: Optional[str] = None
    disabled: Optional[bool] = None
    deleted: Optional[bool] = None


class Memo(BaseModule):
    __tablename__ = 'memo'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(160), nullable=True)
    content = Column(String(1024), nullable=True)
    label = Column(String(30), nullable=True)
    color = Column(String(10), nullable=True)
    ctime = Column(DateTime(50), nullable=True, default=datetime.now)
    utime = Column(DateTime(50), nullable=True, default=datetime.now)


class MemoV(BaseModel):
    id: Optional[int] = 0
    uid: Optional[int] = 0
    title: Optional[str] = None
    content: Optional[str] = None
    label: Optional[str] = None
    color: Optional[str] = None
    ctime: Optional[str] = None
    utime: Optional[str] = None
