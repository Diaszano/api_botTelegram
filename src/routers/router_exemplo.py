""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import List

import sqlalchemy
from src.schemas import schemas
from fastapi import APIRouter, status, HTTPException
from src.infra.sqlalchemy.repositorios.exemplo import (
    RepositorioExemplo
)
#-----------------------
# CONSTANTES
#-----------------------
router = APIRouter(prefix="/exemplo",tags=["Exemplo"]);
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
@router.post(   "/create",
                status_code=status.HTTP_201_CREATED,
                response_model=schemas.Exemplo,
                tags=["Create"])
async def create_exemplo(exemplo:schemas.Exemplo):
    try:
        retorno = await RepositorioExemplo.createReturn(
            exemplo=exemplo
        );
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.get(   "/list",
                status_code=status.HTTP_200_OK,
                response_model=List[schemas.Exemplo],
                tags=["List"])
async def list_exemplo():
    try:
        retorno = await RepositorioExemplo.read();
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.get(   "/get/{id}",
                status_code=status.HTTP_200_OK,
                response_model=schemas.Exemplo,
                tags=["Get"])
async def get_exemplo(id:int):
    try:
        retorno = await RepositorioExemplo.readId(id);
        return retorno;
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exemplo com id '{id}' não existe!"
        );
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );

@router.put(   "/update/{id}",
                status_code=status.HTTP_201_CREATED,
                response_model=schemas.RetornoPadrao,
                tags=["Update"])
async def update_exemplo(id:int,exemplo:schemas.Exemplo):
    try:
        await RepositorioExemplo.readId(id);
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exemplo com id '{id}' não existe!"
        );
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    
    try:
        await RepositorioExemplo.update(
            idExemplo=id,
            exemplo=exemplo
        );
        return schemas.RetornoPadrao;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
        
@router.delete( "/delete/{id}",
                status_code=status.HTTP_201_CREATED,
                response_model=schemas.RetornoPadrao,
                tags=["Delete"])
async def delete_exemplo(id:int):
    try:
        await RepositorioExemplo.readId(id);
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exemplo com id '{id}' não existe!"
        );
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    
    try:
        await RepositorioExemplo.delete(id)
        return schemas.RetornoPadrao;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );        
#-----------------------
# Main()
#-----------------------
#-----------------------