#-----------------------
# BIBLIOTECAS
#-----------------------
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
#-----------------------
# CONSTANTES
#-----------------------
Base = declarative_base();
#-----------------------
# CLASSES
#-----------------------
class Exemplo(Base):
    """Exemplo

    Está classe é serve como modelo 
    de dados que nós operamos no 
    banco de dados.
    """
    __tablename__ = "exemplo";
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    );
    nome = Column(String);
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------