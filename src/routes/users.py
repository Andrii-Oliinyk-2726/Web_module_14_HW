from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET endpoint that returns the current user's information.

    :param current_user: User: Get the current user
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    # cloudinary.config(
    #     cloud_name=settings.cloudinary_name,
    #     api_key=settings.cloudinary_api_key,
    #     api_secret=settings.cloudinary_api_secret,
    #     secure=True
    # )
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The new avatar image to be uploaded.
            current_user (User): The user whose avatar is being updated.

    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user's email
    :param db: Session: Get the database session
    :return: A user object
    :doc-author: Trelent
    """
    public_id = f'HW13/{current_user.username}'
    r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    src_url = cloudinary.CloudinaryImage(public_id)\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
