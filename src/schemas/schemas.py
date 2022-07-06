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
    
    Está classe é serve como modelo 
    de dados que nós operamos nesta 
    API.
    """
    id  : Optional[int] = None;
    nome: str;
    
    class Config:
        orm_mode = True;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
#-----------------------