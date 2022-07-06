#-----------------------
# BIBLIOTECAS
#-----------------------
import os
from asyncio import run
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from src.infra.sqlalchemy.models.models import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
#-----------------------
# CONSTANTES
#-----------------------
DATABASE_URL:str = (
    f"{os.getenv('TIPO_DATABASE')}://"
    f"{os.getenv('USER_DATABASE')}:"
    f"{os.getenv('PASS_DATABASE')}@"
    f"{os.getenv('URL__DATABASE')}/"
    f"{os.getenv('NAME_DATABASE')}"
);

engine        = create_async_engine(DATABASE_URL);
async_session = sessionmaker(engine, class_=AsyncSession);
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
async def create_database():
    """Create DataBase
    
    Nesta função nós iremos fazer a criação
    das tabelas do nosso database.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all);

async def delete_database():
    """Delete DataBase
    
    Nesta função nós iremos fazer a remoção
    das tabelas do nosso database.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all);
        
async def reset_database():
    """Reset DataBase
    
    Nesta função nós iremos fazer a remoção e 
    criação das tabelas do nosso database.
    """
    await delete_database();
    await create_database();

async def get_db() -> Session:
    """Get db
    
    Nesta função nós iremos fazer a 
    conexão com o banco de dados e 
    retornar uma seção.
    """
    async with async_session() as session:
        session:Session
        yield session;
#-----------------------
# Main()
#-----------------------
if(__name__ == "__main__"):
    # run(reset_database());
    run(create_database());
    # run(delete_database());
#-----------------------