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
class RepositorioExemplo:
    """Repositório Exemplo
    
    Nesta classe nós faremos o tratamento das informações 
    recebidas e armazenando no banco de dados.
    """
    @staticmethod
    async def createReturn(exemplo:schemas.Exemplo)->models.Exemplo:
        """Create Return
        
        Neste método nós faremos a inserção dos exemplo
        no banco de dados.

        Args:
            exemplo (schemas.Exemplo): Ele é uma classe que usamos
            como método de inserção de dados.

        Returns:
            models.Exemplo: É o retorno do exemplo, mas de forma
            atualizada com o seu id.
        """
        session_user = models.Exemplo(
            nome=exemplo.nome
        );
        async with async_session() as session:
            session:Session
            
            session.add(session_user);
            await session.commit();
            await session.refresh(session_user);
        return session_user;

    @staticmethod
    async def create(exemplo:schemas.Exemplo) -> None:
        """Create
        
        Neste método nós faremos a inserção dos exemplo
        no banco de dados.

        Args:
            exemplo (schemas.Exemplo): Ele é uma classe que usamos
            como método de inserção de dados.
        """
        stmt = insert(models.Exemplo).values(
            nome=exemplo.nome
        )
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def read() -> List[models.Exemplo]:
        """Read
        
        Neste método nós faremos a leitura dos exemplos
        no banco de dados.

        Returns:
            List[models.Exemplo]:
        """
        retorno = None;
        stmt    = select(models.Exemplo);
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().fetchall();
        return retorno;

    @staticmethod
    async def readId(idExemplo:int) -> models.Exemplo:
        """Read Id
        
        Neste método nós faremos a leitura do exemplo
        com o Id passado.

        Args:
            idExemplo (int): necessitamos do id do 
            exemplo para ser buscado no banco.

        Returns:
            models.Exemplo
        """
        retorno = None;
        stmt    = select(models.Exemplo).where(
            models.Exemplo.id==idExemplo
        );
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().one();
        return retorno;

    @staticmethod
    async def update(idExemplo:int,exemplo:schemas.Exemplo) -> None:
        """Update
        
        Neste método nós faremos a atualização do exemplo
        com o Id passado.

        Args:
            idExemplo (int): necessitamos do id do 
            exemplo para ser buscado no banco.
            exemplo (schemas.Exemplo): Ele é uma classe que usamos
            como método de atualização dos dados.
        """
        stmt = update(models.Exemplo).where(
            models.Exemplo.id==idExemplo
        ).values(
            nome=exemplo.nome
        );
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def delete(idExemplo:int) -> None:
        """Delete
        
        Neste método nós faremos a remoção de um exemplo
        com o Id passado.

        Args:
            idExemplo (int): necessitamos do id do 
            exemplo para ser buscado no banco.
        """
        stmt = delete(models.Exemplo).where(
            models.Exemplo.id==idExemplo
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