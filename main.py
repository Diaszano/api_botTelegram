"""Api do Bot do Telegram"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from banco import *
from fastapi import FastAPI
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
app = FastAPI()
db = DataBaseSqlite();

@app.get("/v1/auth")
def auth(authenticationDto:User):
    username:str  = authenticationDto.username;
    senha   :str  = authenticationDto.senha;
    retorno :dict = {};
    retorno["APIKEY"] = db.get_apiKey_user(
            username=username,
            senha=senha
        )
    return retorno;

@app.post("/v1/auth")
def auth(authenticationDto:Insert_user):
    username:str = authenticationDto.username;
    senha   :str = authenticationDto.senha;
    apikey  :str = authenticationDto.APIKEY;
    tipo    :str = authenticationDto.tipo;
    
    retorno = db.create_user(
        username=username,
        senha=senha,
        tipo=tipo,
        apikey=apikey
    );
    return retorno;
#-----------------------