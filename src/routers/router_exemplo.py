""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from src.infra.sqlalchemy.repositorios.exemplo import (
    RepositorioExemplo
)
#-----------------------
# CONSTANTES
#-----------------------
router   = APIRouter(prefix="/exemplo",tags=["Exemplo"]);
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
async def create_favorite(  exemplo:schemas.Exemplo,
                            session:Session=Depends(get_db)):
    try:
        retorno = await RepositorioExemplo(session).createReturn(
            exemplo=exemplo
        );
        return retorno;
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
#-----------------------
# Main()
#-----------------------
#-----------------------