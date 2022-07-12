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
class RepositorioEncomenda:
    """Repositório Encomenda
    
    Nesta classe nós faremos o tratamento das informações 
    recebidas e armazenando no banco de dados.
    """
    @staticmethod
    async def createReturn(encomenda:schemas.Encomenda) -> models.Encomenda:
        """Create Return
        
        Neste método nós faremos a inserção dos encomenda
        no banco de dados.

        Args:
            encomenda (schemas.Encomenda): Ele é uma classe que usamos
            como método de inserção de dados.

        Returns:
            models.Encomenda: É o retorno do encomenda, mas de forma
            atualizada com o seu id.
        """
        session_user = models.Encomenda(
            nome         = encomenda.nome,
            usuario_id   = encomenda.usuario_id,
            rastreio_id  = encomenda.rastreio_id,
            data_criacao = encomenda.data_criacao
        );
        async with async_session() as session:
            session:Session
            
            session.add(session_user);
            await session.commit();
            await session.refresh(session_user);
        return session_user;

    @staticmethod
    async def create(encomenda:schemas.Encomenda) -> None:
        """Create
        
        Neste método nós faremos a inserção dos encomenda
        no banco de dados.

        Args:
            encomenda (schemas.Encomenda): Ele é uma classe que usamos
            como método de inserção de dados.
        """
        stmt = insert(models.Encomenda).values(
            nome         = encomenda.nome,
            usuario_id   = encomenda.usuario_id,
            rastreio_id  = encomenda.rastreio_id,
            data_criacao = encomenda.data_criacao
        )
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def read() -> List[models.Encomenda]:
        """Read
        
        Neste método nós faremos a leitura dos usuários
        no banco de dados.

        Returns:
            List[models.Encomenda]:
        """
        retorno = None;
        stmt    = select(models.Encomenda);
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().fetchall();
        return retorno;

    @staticmethod
    async def readId(idUser:int,idRastreio) -> models.Encomenda:
        """Read Id
        
        Neste método nós faremos a leitura do encomenda
        com o Id passado.

        Args:
            idEncomenda (int): necessitamos do id do 
            encomenda para ser buscado no banco.

        Returns:
            models.Encomenda
        """
        retorno = None;
        stmt    = select(models.Encomenda).where(
            (models.Encomenda.usuario_id==idUser) &
            (models.Encomenda.rastreio_id == idRastreio)
        );
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().one();
        return retorno;
    
    @staticmethod
    async def update(idEncomenda:int,encomenda:schemas.Encomenda) -> None:
        """Update
        
        Neste método nós faremos a atualização do encomenda
        com o Id passado.

        Args:
            idEncomenda (int): necessitamos do id do 
            encomenda para ser buscado no banco.
            encomenda (schemas.Encomenda): Ele é uma classe que usamos
            como método de atualização dos dados.
        """
        stmt = update(models.Encomenda).where(
            models.Encomenda.id==idEncomenda
        ).values(
            nome         = encomenda.nome,
        );
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def delete(idEncomenda:int) -> None:
        """Delete
        
        Neste método nós faremos a remoção de um encomenda
        com o Id passado.

        Args:
            idEncomenda (int): necessitamos do id do 
            encomenda para ser buscado no banco.
        """
        stmt = delete(models.Encomenda).where(
            models.Encomenda.id==idEncomenda
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