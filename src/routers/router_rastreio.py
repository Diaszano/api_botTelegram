""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
import sqlalchemy
from asyncio import gather
from src.tools import rasteador
from src.schemas import schemas
from pydantic import PositiveInt, constr
from fastapi import (
    APIRouter, status, HTTPException
)
from src.infra.sqlalchemy.repositorios.rastreio import ( 
    RepositorioRastreio
)
from src.infra.sqlalchemy.repositorios.usuario import (
    RepositorioUsuario
)
from src.infra.sqlalchemy.repositorios.encomenda import (
    RepositorioEncomenda
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
async def pegar_usuario(idTelegram:int) -> schemas.Usuario:
    try:
        usuario = await RepositorioUsuario.readIdTelegram(
            idTelegram=idTelegram
        );
    except sqlalchemy.exc.NoResultFound:
        usuario = await RepositorioUsuario.createReturn(
            schemas.Usuario(
                id_telegram=idTelegram
            )
        );
    except Exception as error:
        raise error;
    return usuario;

async def pegar_rastreio(codigo:int) -> schemas.Rastreio:
    try:
        rastreio = await RepositorioRastreio.readCodigo(
            codigo= codigo
        )
    except sqlalchemy.exc.NoResultFound:
        mensagem = rastreador.rastrear(codigo)
        rastreio = await RepositorioRastreio.createReturn(
            rastreio = schemas.Rastreio(
                codigo   = codigo,
                mensagem = await mensagem
            )
        )
    except Exception as error:
        raise error;
    return rastreio;

@router.post(   "/adicionar",
                status_code=status.HTTP_201_CREATED,
                response_model=schemas.RastreioRetorno,
                tags=["rastrear"])
async def adicionar_encomenda(nova_encomenda:schemas.EncomendaInsert):
    try:
        [usuario,rastreio] = await gather(
            pegar_usuario(nova_encomenda.id_telegram),
            pegar_rastreio(nova_encomenda.codigo)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    try:
        encomenda = await RepositorioEncomenda.readId(
            idUser     = usuario.id,
            idRastreio = rastreio.id
        );
    except sqlalchemy.exc.NoResultFound:
        encomenda = await RepositorioEncomenda.createReturn(
            encomenda = schemas.Encomenda(
                nome = nova_encomenda.nome,
                usuario_id     = usuario.id,
                rastreio_id    = rastreio.id
            ) 
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    
    return rastreio;

@router.get(   "/{idTelegram}/usuario",
                status_code=status.HTTP_200_OK,
                response_model=schemas.UsuarioRetorno,
                tags=["Listar"])
async def usuario_encomendas(idTelegram:PositiveInt):
    try:
        usuario = await RepositorioUsuario.readIdTelegram(
            idTelegram=idTelegram
        );
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Usuário inexistente."
        );
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    return usuario;

@router.get(   "/{codigo}/rastreio",
                status_code=status.HTTP_200_OK,
                response_model=schemas.RastreioRetornoCompleto,
                tags=["Listar"])
async def rastreio_encomendas(codigo:constr(max_length=13,
                                            min_length=13,
                                            regex=(
                                            r'[a-zA-Z]{2}'
                                            r'[0-9]{9}'
                                            r'[a-zA-Z]{2}'))):
    try:
        rastreio = await RepositorioRastreio.readCodigo(codigo);
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Usuário inexistente."
        );
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{error}"
        );
    return rastreio;
#-----------------------
# Main()
#-----------------------
#-----------------------