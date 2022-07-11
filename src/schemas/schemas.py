"""Schema"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from random import randint
from typing import List, Optional
from pydantic import BaseModel, constr, PositiveInt, Field
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class Exemplo(BaseModel):
    """Exemplo
    
    Essa classe serve como modelo 
    de dados que nós operamos nesta 
    API.
    """
    id  : Optional[int] = None;
    nome: str;
    
    class Config:
        orm_mode = True;

class RetornoPadrao(BaseModel):
    """Exemplo
    
    Essa classe serve como modelo 
    de dados que nós operamos nesta 
    API.
    """
    status :Optional[bool] = True;
    message:Optional[str]  = "Execução com sucesso";
    detail :Optional[str]  = "Tudo ocorreu como o esperado";
    
    
    class Config:
        orm_mode = True;

class Rastreio(BaseModel):
    """Rastreio
    
    Essa classe serve como modelo 
    de dados que nós operamos nesta 
    API.
    """
    codigo:constr(
        max_length=13,
        min_length=13,
        regex=r'[a-zA-Z]{2}[0-9]{9}[a-zA-Z]{2}'
    ) = Field(
        "LD280110210RC", 
        title="Código", 
        description= (
            "Aqui deve ser colocado o "
            "código de rastreio da "
            "encomenda."
        )
    );
    
    class Config:
        orm_mode = True;

class RastreioReturn(Rastreio):
    """Encomenda
    
    Essa classe serve como modelo 
    de dados que nós operamos nesta 
    API.
    """
    mensagem:list = Field(
        "mensagem...", 
        title="Mensagem", 
        description= (
            "Aqui retornará o mensagem "
            "do rastreio com todas as "
            "informações da "
            "encomenda rastreada."
        )
    );
    status:bool = Field(
        True, 
        title="status", 
        description= (
            "Aqui retornará o status "
            "em forma booliana da "
            "encomenda rastreada."
        )
    );

class RastreioReturnId(Rastreio):
    """Encomenda
    
    Essa classe serve como modelo 
    de dados que nós operamos nesta 
    API.
    """
    mensagem:list = Field(
        "mensagem...", 
        title="Mensagem", 
        description= (
            "Aqui retornará o mensagem "
            "do rastreio com todas as "
            "informações da "
            "encomenda rastreada."
        )
    );
    status:bool = Field(
        True, 
        title="status", 
        description= (
            "Aqui retornará o status "
            "em forma booliana da "
            "encomenda rastreada."
        )
    );

class RastreioInsert(Rastreio):
    id:Optional[int] = None;
    mensagem:str = Field(
        "mensagem...", 
        title="Mensagem", 
        description= (
            "Aqui retornará o mensagem "
            "do rastreio com todas as "
            "informações da "
            "encomenda rastreada."
        )
    );
    status:bool = Field(
        True, 
        title="status", 
        description= (
            "Aqui retornará o status "
            "em forma booliana da "
            "encomenda rastreada."
        )
    );


class RastreioBot(RastreioInsert):
    id_telegram:PositiveInt = Field(
        randint(1,99999), 
        title="ID do Telegram", 
        description= (
            "Aqui é o id único "
            "que cada usuário "
            "tem no telegram."
        )
    );
    nome_encomenda:str = Field(
        "Celular", 
        title="Nome da encomenda", 
        description= (
            "Aqui deve se colocar o nome "
            "da encomenda solicitada."
        )
    );
    
# encomendas:List[Encomenda] = Field(
#         None,
#         title="Encomendas", 
#         description=(
#             "Aqui teremos a lista com "
#             "todas encomendas "
#             "rastreadas pelo usuário"
#         )
#     )
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------