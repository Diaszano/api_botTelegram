"""Schema"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import Optional
from pydantic import BaseModel
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
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------