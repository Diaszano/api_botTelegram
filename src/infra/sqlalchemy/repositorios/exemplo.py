#-----------------------
# BIBLIOTECAS
#-----------------------
# from typing import List
from src.schemas import schemas
from sqlalchemy.orm import Session
# from sqlalchemy.future import select
# from sqlalchemy import update, delete, insert
from src.infra.sqlalchemy.models import models
# from src.infra.sqlalchemy.config.database import async_session
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class RepositorioExemplo():
    """Repositório Exemplo
    
    Nesta classe nós faremos o tratamento das informações 
    recebidas e armazenando no banco de dados.
    """
    def __init__(self, session:Session) -> None:
        """Repositório Exemplo

        Neste Repositório nós faremos todas as operações
        com o banco de dados.
        
        
        Args:
            session (Session): É a conexão com o banco de dados.
        """
        self.session = session;
    
    async def createReturn(self,exemplo:schemas.Exemplo)->models.Exemplo:
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
        
        self.session.add(session_user);
        await self.session.commit();
        await self.session.refresh(session_user);
        return session_user;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------