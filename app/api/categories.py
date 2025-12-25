from typing import Annotated, List, Optional
from uuid import uuid1
import shutil
import os

from fastapi import Form, Depends, HTTPException, status, File, UploadFile
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..models.user import User
from ..models.task import Category
from ..schemas.categories import CategoryResponse
from .deps import get_admin, get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_categories(
    name: Annotated[str, Form()],
    color: Annotated[str, Form()],
    icon: Annotated[UploadFile, File()],
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin)],
):
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists."
        )

    if icon.content_type not in ["image/svg+xml", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="icon should be svg format"
        )

    if icon.content_type == "image/svg+xml":
        icon_extention = "svg"
    elif icon.content_type == "image/png":
        icon_extention = "png"

    icon_path = f"media/category-icons/{str(uuid1())}.{icon_extention}"
    with open(icon_path, "wb") as f:
        shutil.copyfileobj(icon.file, f)

    new_category = Category(name=name, color=color, icon=icon_path)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_category_list(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    categories = db.query(Category).all()
    return categories


@router.get("/{pk}")
def get_one_category(
    pk: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> CategoryResponse:
    category = db.query(Category).filter(Category.category_id == pk).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )
    return category


@router.put("/{pk}", status_code=status.HTTP_200_OK)
def update_category(
    pk: int,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
    name: Annotated[Optional[str], Form()] = None,
    color: Annotated[Optional[str], Form()] = None,
    icon: Annotated[Optional[UploadFile], File()] = None,
):
    category = db.query(Category).filter(Category.category_id == pk).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )
    if name is None and color is None and icon is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (name, color, icon) must be provided for update.",
        )

    if name:
        category.name = name
    if color:
        category.color = color
    if icon:
        if icon.content_type not in ["image/svg+xml", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="icon should be svg format",
            )

        os.remove(category.icon)

        if icon.content_type == "image/svg+xml":
            icon_extention = "svg"
        elif icon.content_type == "image/png":
            icon_extention = "png"

        icon_path = f"media/category-icons/{str(uuid1())}.{icon_extention}"
        with open(icon_path, "wb") as f:
            shutil.copyfileobj(icon.file, f)
        category.icon = icon_path

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    pk: int,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    category = db.query(Category).filter(Category.category_id == pk).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )

    os.remove(category.icon)

    db.delete(category)
    db.commit()
    return {"detail": "Category deleted successfully."}
