""""""
#-----------------------
# BIBLIOTECAS
#-----------------------
import sqlalchemy
from asyncio import gather
from src.tools import rasteador
from src.schemas import schemas
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
                nome_encomenda = nova_encomenda.nome_encomenda,
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
#-----------------------
# Main()
#-----------------------
#-----------------------