""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import List
from pydantic import constr
import sqlalchemy
from src.tools import rasteador
from src.schemas import schemas
from fastapi import (
    APIRouter, status, HTTPException, BackgroundTasks
)
from src.infra.sqlalchemy.repositorios.rastreio import ( 
    RepositorioRastreio
)
#-----------------------
# CONSTANTES
#-----------------------
router = APIRouter(prefix="/encomendas",tags=["Encomendas"]);
#-----------------------
# CLASSES
#-----------------------
rastreador = rasteador.Rastreio();
#-----------------------
# FUNÇÕES()
#-----------------------
@router.get(   "/rastrear/{codigo}",
                status_code=status.HTTP_200_OK,
                response_model=schemas.RastreioReturn,
                tags=["rastrear"])
async def create_exemplo(codigo:constr( max_length=13,min_length=13,
                                        regex=( r'[a-zA-Z]{2}[0-9]{9}'
                                                r'[a-zA-Z]{2}'))):
    try:
        retorno =  await RepositorioRastreio. \
                            readCodigo(codigo);
        retorno.mensagem = list(retorno.mensagem)
        return retorno;
    except sqlalchemy.exc.NoResultFound:
        mensagem:str  = await rastreador.rastrear(codigo);
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        ); 
    status_rastreio:bool = True;
    
    if(not mensagem):
        status_rastreio = False;
    
    retorno = schemas.RastreioInsert(
        codigo   = codigo,
        mensagem = mensagem,
        status   = status_rastreio
    );
    await RepositorioRastreio.create(retorno);
    retorno.mensagem = eval(retorno.mensagem)
    return retorno;  

@router.post(   "/rastrear",
                status_code=status.HTTP_201_CREATED,
                response_model=schemas.RastreioInsert,
                tags=["rastrear"])
async def create_exemplo(rastreio:schemas.RastreioBot):
    try:
        retorno_rastreio =  await RepositorioRastreio. \
                            readCodigo(rastreio.codigo);
    except sqlalchemy.exc.NoResultFound:
        rastreio.mensagem = await rastreador.rastrear(
            codigo=rastreio.codigo
        );
        rastreio.status:bool = True;
    
        if(not rastreio.mensagem):
            rastreio.status = False;
        
        retorno_rastreio = await RepositorioRastreio. \
                            createReturn(rastreio);
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    return retorno_rastreio; 
#-----------------------
# Main()
#-----------------------
#-----------------------