from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.brand import Brand as BrandModel
from app.schemas.brand import Brand, BrandPost, BrandPut
from app.security.schemas.profile_response import ProfileResponse
from app.security.token import get_current_active_user

brand_pr = APIRouter()

@brand_pr.post('/crearMarca', status_code=status.HTTP_201_CREATED)
async def crear_marca(brand: BrandPost, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        new_brand = BrandModel(name=brand.name, description=brand.description)
        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return new_brand

@brand_pr.put('/actualizarMarca/{id}', status_code=status.HTTP_202_ACCEPTED)
async def actualizar_marca(id: int, brand: BrandPut, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        brand_db = db.query(BrandModel).filter(BrandModel.id == id).first()
        if not brand_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la marca')
        brand_db.name = brand.name
        brand_db.description = brand.description
        db.commit()
        db.refresh(brand_db)
        return brand_db

@brand_pr.delete('/eliminarMarca/{id}', status_code=status.HTTP_200_OK)
async def eliminar_marca(id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_active_user)):
    user_type = list(user.keys())[0]
    if user_type != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No tiene permisos para realizar esta acción')
    else:
        brand_db = db.query(BrandModel).filter(BrandModel.id == id).first()
        if not brand_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No existe la marca')
        db.delete(brand_db)
        db.commit()
        return {'message': 'Se eliminó la marca'}