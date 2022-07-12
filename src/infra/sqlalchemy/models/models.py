#-----------------------
# BIBLIOTECAS
#-----------------------
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import (    
    Column, Integer, String, ForeignKey, 
    Boolean, DateTime
)
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
        autoincrement=True,
        index=True
    );
    nome = Column(String);

class Rastreio(Base):
    
    __tablename__ = 'rastreio';
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    );
    codigo       = Column(String,index=True);
    mensagem     = Column(String);
    atualizacao  = Column(DateTime);
    mudanca      = Column(DateTime);
    lido         = Column(Boolean);
    solicitacoes = relationship(
        "Encomenda",
        back_populates='rastreio',
        lazy='subquery'
    );
    

class Usuario(Base):
    
    __tablename__ = 'usuario';
    
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    );
    id_telegram = Column(Integer,index=True);
    encomendas  = relationship(
        "Encomenda",
        back_populates="usuario",
        lazy='subquery'
    );
    data_criacao = Column(DateTime);

class Encomenda(Base):
    
    __tablename__ = 'encomenda';
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    );
    nome       = Column(String);
    
    usuario_id = Column(
        Integer,
        ForeignKey(
            'usuario.id',
            name="fk_encomenda_usuario"
        )
    );
    
    usuario = relationship(
        "Usuario",
        back_populates="encomendas",
        lazy='subquery'
    );
    
    rastreio_id = Column(
        Integer,
        ForeignKey(
            'rastreio.id',
            name="fk_encomenda_rastreio"
        )
    );
    rastreio = relationship(
        "Rastreio",
        back_populates="solicitacoes",
        lazy='subquery'
    );
    
    data_criacao = Column(DateTime);
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------