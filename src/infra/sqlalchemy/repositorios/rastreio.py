#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import List
from src.schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update, delete, insert
from src.infra.sqlalchemy.models import models
from src.infra.sqlalchemy.config.database import async_session
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class RepositorioRastreio:
    """Repositório Rastreio
    
    Nesta classe nós faremos o tratamento das informações 
    recebidas e armazenando no banco de dados.
    """
    @staticmethod
    async def createReturn(rastreio:schemas.Rastreio) -> models.Rastreio:
        """Create Return
        
        Neste método nós faremos a inserção dos rastreio
        no banco de dados.

        Args:
            rastreio (schemas.Rastreio): Ele é uma classe que usamos
            como método de inserção de dados.

        Returns:
            models.Rastreio: É o retorno do rastreio, mas de forma
            atualizada com o seu id.
        """
        session_user = models.Rastreio(
            codigo      = rastreio.codigo,
            mensagem    = rastreio.mensagem,
            atualizacao = rastreio.atualizacao,
            mudanca     = rastreio.mudanca,
            lido        = rastreio.lido
        );
        async with async_session() as session:
            session:Session
            
            session.add(session_user);
            await session.commit();
            await session.refresh(session_user);
        return session_user;

    @staticmethod
    async def create(rastreio:schemas.Rastreio) -> None:
        """Create
        
        Neste método nós faremos a inserção dos rastreio
        no banco de dados.

        Args:
            rastreio (schemas.Rastreio): Ele é uma classe que usamos
            como método de inserção de dados.
        """
        stmt = insert(models.Rastreio).values(
            codigo      = rastreio.codigo,
            mensagem    = rastreio.mensagem,
            atualizacao = rastreio.atualizacao,
            mudanca     = rastreio.mudanca,
            lido        = rastreio.lido
        )
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def read() -> List[models.Rastreio]:
        """Read
        
        Neste método nós faremos a leitura dos rastreios
        no banco de dados.

        Returns:
            List[models.Rastreio]:
        """
        retorno = None;
        stmt    = select(models.Rastreio);
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().fetchall();
        return retorno;

    @staticmethod
    async def readId(idRastreio:int) -> models.Rastreio:
        """Read Id
        
        Neste método nós faremos a leitura do rastreio
        com o Id passado.

        Args:
            idRastreio (int): necessitamos do id do 
            rastreio para ser buscado no banco.

        Returns:
            models.Rastreio
        """
        retorno = None;
        stmt    = select(models.Rastreio).where(
            models.Rastreio.id==idRastreio
        );
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().one();
        return retorno;
    
    @staticmethod
    async def readCodigo(codigo:str) -> models.Rastreio:
        """Read Id
        
        Neste método nós faremos a leitura do rastreio
        com o Id passado.

        Args:
            Codigo (str): necessitamos do id do 
            rastreio para ser buscado no banco.

        Returns:
            models.Rastreio
        """
        retorno = None;
        stmt    = select(models.Rastreio).where(
            models.Rastreio.codigo==codigo
        );
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().one();
        return retorno;

    @staticmethod
    async def update(idRastreio:int,rastreio:schemas.Rastreio) -> None:
        """Update
        
        Neste método nós faremos a atualização do rastreio
        com o Id passado.

        Args:
            idRastreio (int): necessitamos do id do 
            rastreio para ser buscado no banco.
            rastreio (schemas.Rastreio): Ele é uma classe que usamos
            como método de atualização dos dados.
        """
        stmt = update(models.Rastreio).where(
            models.Rastreio.id==idRastreio
        ).values(
            mensagem    = rastreio.mensagem,
            atualizacao = rastreio.atualizacao,
            mudanca     = rastreio.mudanca,
            lido        = rastreio.lido
        );
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def delete(idRastreio:int) -> None:
        """Delete
        
        Neste método nós faremos a remoção de um rastreio
        com o Id passado.

        Args:
            idRastreio (int): necessitamos do id do 
            rastreio para ser buscado no banco.
        """
        stmt = delete(models.Rastreio).where(
            models.Rastreio.id==idRastreio
        );
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------