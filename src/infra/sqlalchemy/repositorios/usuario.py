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
class RepositorioUsuario:
    """Repositório Usuario
    
    Nesta classe nós faremos o tratamento das informações 
    recebidas e armazenando no banco de dados.
    """
    @staticmethod
    async def createReturn(usuario:schemas.Usuario)->models.Usuario:
        """Create Return
        
        Neste método nós faremos a inserção dos usuario
        no banco de dados.

        Args:
            usuario (schemas.Usuario): Ele é uma classe que usamos
            como método de inserção de dados.

        Returns:
            models.Usuario: É o retorno do usuario, mas de forma
            atualizada com o seu id.
        """
        session_user = models.Usuario(
            id_telegram  = usuario.id_telegram,
            data_criacao = usuario.data_criacao
        );
        async with async_session() as session:
            session:Session
            
            session.add(session_user);
            await session.commit();
            await session.refresh(session_user);
        return session_user;

    @staticmethod
    async def create(usuario:schemas.Usuario) -> None:
        """Create
        
        Neste método nós faremos a inserção dos usuario
        no banco de dados.

        Args:
            usuario (schemas.Usuario): Ele é uma classe que usamos
            como método de inserção de dados.
        """
        stmt = insert(models.Usuario).values(
            id_telegram  = usuario.id_telegram,
            data_criacao = usuario.data_criacao
        )
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def read() -> List[models.Usuario]:
        """Read
        
        Neste método nós faremos a leitura dos usuários
        no banco de dados.

        Returns:
            List[models.Usuario]:
        """
        retorno = None;
        stmt    = select(models.Usuario);
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().fetchall();
        return retorno;

    @staticmethod
    async def readId(idUsuario:int) -> models.Usuario:
        """Read Id
        
        Neste método nós faremos a leitura do usuario
        com o Id passado.

        Args:
            idUsuario (int): necessitamos do id do 
            usuario para ser buscado no banco.

        Returns:
            models.Usuario
        """
        retorno = None;
        stmt    = select(models.Usuario).where(
            models.Usuario.id==idUsuario
        );
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().one();
        return retorno;
    
    @staticmethod
    async def readIdTelegram(idTelegram:str) -> models.Usuario:
        """Read Id
        
        Neste método nós faremos a leitura do usuario
        com o Id passado.

        Args:
            Codigo (str): necessitamos do id do 
            usuario para ser buscado no banco.

        Returns:
            models.Usuario
        """
        retorno = None;
        stmt    = select(models.Usuario).where(
            models.Usuario.id_telegram==idTelegram
        );
        async with async_session() as session:
            session:Session
            
            retorno = await session.execute(stmt);
            retorno = retorno.scalars().one();
        return retorno;

    @staticmethod
    async def update(idUsuario:int,usuario:schemas.Usuario) -> None:
        """Update
        
        Neste método nós faremos a atualização do usuario
        com o Id passado.

        Args:
            idUsuario (int): necessitamos do id do 
            usuario para ser buscado no banco.
            usuario (schemas.Usuario): Ele é uma classe que usamos
            como método de atualização dos dados.
        """
        stmt = update(models.Usuario).where(
            models.Usuario.id==idUsuario
        ).values(
            id_telegram  = usuario.id_telegram
        );
        async with async_session() as session:
            session:Session
            
            await session.execute(stmt);
            await session.commit();
    
    @staticmethod
    async def delete(idUsuario:int) -> None:
        """Delete
        
        Neste método nós faremos a remoção de um usuario
        com o Id passado.

        Args:
            idUsuario (int): necessitamos do id do 
            usuario para ser buscado no banco.
        """
        stmt = delete(models.Usuario).where(
            models.Usuario.id==idUsuario
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