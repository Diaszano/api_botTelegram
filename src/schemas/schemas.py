"""Schemas"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from random import randint
from typing import List, Optional
from datetime import datetime
from pydantic import (
    BaseModel, constr, PositiveInt, 
    Field, validator
)
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# Simples
#-----------------------
# Modelo simples do Usuário
class UsuarioSimples(BaseModel):
    id_telegram:PositiveInt = Field(
        randint(1,99999), 
        title="ID do Telegram", 
        description= (
            "Aqui é o id único "
            "que cada usuário "
            "tem no telegram."
        )
    );
    class Config:
        orm_mode = True;
# Modelo simples da Encomenda
class EncomendaSimples(BaseModel):
    nome:str = Field(
        "Celular", 
        title="Nome da encomenda", 
        description= (
            "Aqui deve se colocar o nome "
            "da encomenda solicitada."
        )
    );
    usuario:UsuarioSimples;
    class Config:
        orm_mode = True;
#-----------------------
# Inserções
#-----------------------
# Inserções das Encomendas
class EncomendaInsert(BaseModel):
    id_telegram:PositiveInt = Field(
        randint(1,99999), 
        title="ID do Telegram", 
        description= (
            "Aqui é o id único "
            "que cada usuário "
            "tem no telegram."
        )
    );
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
    nome:str = Field(
        "Celular", 
        title="Nome da encomenda", 
        description= (
            "Aqui deve se colocar o nome "
            "da encomenda solicitada."
        )
    );
    
    class Config:
        orm_mode = True;
#-----------------------
# Modelos do Banco
#-----------------------
# Modelo do Exemplo
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
# Modelo do Usuário
class Usuario(BaseModel):
    id:Optional[PositiveInt] = Field(
        randint(1,99999), 
        title="ID do Usuário", 
        description= (
            "Aqui é o id único "
            "que cada usuário "
            "tem na api."
        )
    );
    
    id_telegram:PositiveInt = Field(
        randint(1,99999), 
        title="ID do Telegram", 
        description= (
            "Aqui é o id único "
            "que cada usuário "
            "tem no telegram."
        )
    );
    
    data_criacao:Optional[datetime] = Field(
        datetime.now(), 
        title="Data da Criação", 
        description= (
            "Aqui guardaremos a data da "
            "criação do usuário na api. "
        )
    );
    
    class Config:
        orm_mode = True;
# Modelo do Rastreio
class Rastreio(BaseModel):
    id:Optional[PositiveInt] = Field(
        randint(1,99999), 
        title="ID do Rastreio", 
        description= (
            "Aqui é o id único "
            "que cada Rastreio "
            "tem na api."
        )
    );
    
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
    
    mensagem:Optional[str] = Field(
        "mensagem...", 
        title="Mensagem", 
        description= (
            "Aqui retornará o mensagem "
            "do rastreio com todas as "
            "informações da "
            "encomenda rastreada."
        )
    );
    
    atualizacao:datetime = Field(
        datetime.now(), 
        title="Data da Atualização", 
        description= (
            "Aqui guardaremos a data da "
            "atualização do rastreio na api. "
        )
    );
    
    mudanca:datetime = Field(
        datetime.now(), 
        title="Mudança", 
        description= (
            "Aqui veremos se teve mudança "
            "na última verificação do "
            "rastreio."
        )
    );
    lido:bool = Field(
        True, 
        title="Lido", 
        description= (
            "Aqui veremos se as informações "
            "foram lidas depois da atualização."
        )
    );
    class Config:
        orm_mode = True;
# Modelo da Encomenda
class Encomenda(BaseModel):
    id:Optional[PositiveInt] = Field(
        randint(1,99999), 
        title="ID da Encomenda", 
        description= (
            "Aqui é o id único "
            "que cada encomenda "
            "tem na api."
        )
    );
    
    nome:str = Field(
        "Celular", 
        title="Nome da encomenda", 
        description= (
            "Aqui deve se colocar o nome "
            "da encomenda solicitada."
        )
    );
    
    usuario_id:PositiveInt = Field(
        randint(1,99999), 
        title="ID do Usuário", 
        description= (
            "Aqui é o id único "
            "que cada usuário "
            "tem na api."
        )
    );
    
    rastreio_id:PositiveInt = Field(
        randint(1,99999), 
        title="ID do Rastreio", 
        description= (
            "Aqui é o id único "
            "que cada Rastreio "
            "tem na api."
        )
    );
    
    data_criacao:Optional[datetime] = Field(
        datetime.now(), 
        title="Data da Criação", 
        description= (
            "Aqui guardaremos a data da "
            "criação da encomenda na api. "
        )
    );
    
    class Config:
        orm_mode = True;
#-----------------------
# Retornos
#-----------------------
# Retornos Padrões
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
# Retornos Rastreios
class RastreioRetorno(BaseModel):
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
    
    mensagem:Optional[list] = Field(
        "mensagem...", 
        title="Mensagem", 
        description= (
            "Aqui retornará o mensagem "
            "do rastreio com todas as "
            "informações da "
            "encomenda rastreada."
        )
    );
    
    atualizacao:datetime = Field(
        datetime.now(), 
        title="Data da Atualização", 
        description= (
            "Aqui guardaremos a data da "
            "atualização do rastreio na api. "
        )
    );
    
    mudanca:datetime = Field(
        datetime.now(), 
        title="Mudança", 
        description= (
            "Aqui veremos se teve mudança "
            "na última verificação do "
            "rastreio."
        )
    );
    
    @validator("mensagem", pre=True, each_item=True)
    def transformar_mensagem(cls,mensagem):
        if(isinstance(mensagem,str)):
            return eval(mensagem);
    
    class Config:
        orm_mode = True;

class EncomendaRetorno(BaseModel):
    rastreio:Optional[RastreioRetorno]
    class Config:
        orm_mode = True;

class UsuarioRetorno(BaseModel):
    encomendas:Optional[List[EncomendaRetorno]] = Field(
        [], 
        title="Encomendas", 
        description= (
            "Aqui veremos todas as encomendas "
            "do usuário."
        )
    );
    class Config:
        orm_mode = True;
#-----------------------
# Completo
#-----------------------
# Modelo completo do Rastreio
class RastreioRetornoCompleto(RastreioRetorno):
    lido:bool = Field(
        True, 
        title="Lido", 
        description= (
            "Aqui veremos se as informações "
            "foram lidas depois da atualização."
        )
    );
    solicitacoes:List[EncomendaSimples];
    class Config:
        orm_mode = True;
#-----------------------