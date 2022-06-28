"""Api do Bot do Telegram"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import io
import pyqrcode
from db import *
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
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
app   = FastAPI();
banco = DataBaseSqlite();

@app.get("/auth")
async def auth(authenticationDto:User):
    """Pegar usuário

    Aqui pegaremos um usuário da api
    """
    username:str  = authenticationDto.username;
    senha   :str  = authenticationDto.senha;
    retorno :dict = {};
    retorno["APIKEY"] = banco.get_apiKey_user(
            username=username,
            senha=senha
        )
    return retorno;

@app.post("/auth")
async def auth(authenticationDto:Insert_user):
    """Criação de usuários

    Aqui criaremos os usuários da api
    """
    username:str = authenticationDto.username;
    senha   :str = authenticationDto.senha;
    apikey  :str = authenticationDto.APIKEY;
    tipo    :str = authenticationDto.tipo;
    
    retorno = banco.create_user(
        username=username,
        senha=senha,
        tipo=tipo,
        apikey=apikey
    );
    return retorno;

@app.get("/api/bot_telegram/menu")
async def menu(info:Menu):
    """Pegamos o estado do menu

    Aqui pegaremos o estado do user solicitado.
    """
    apikey :str = info.APIKEY;
    id_user:int = info.id_user;
    retorno:dict = {};
    if(not banco.login_api_key(apikey)):
        retorno["Erro"] = "User sem autorização";
    else:
        var_menu = banco.pega_estado_menu(
            id_user=id_user
        );
        if(var_menu < 0):
            retorno["Erro"] = "Cliente não existente";
        else:
            retorno["menu"] = var_menu;
    return retorno;

@app.post("/api/bot_telegram/menu")
async def menu(info:Menu):
    """Insere o estado do menu

    Aqui inserimos o estado do user solicitado.
    """
    apikey :str = str(info.APIKEY);
    id_user:int = int(info.id_user);
    retorno:dict = {};
    if(not banco.login_api_key(apikey)):
        retorno["Erro"] = "User sem autorização";
    else:
        estado = banco.cria_estado_menu(
            id_user=id_user
        );
        if(estado):
            retorno["Sucesso"] = "Cadastrado o estado";
        else:
            retorno["Erro"] = "User já existente";
    return retorno;

@app.put("/api/bot_telegram/menu")
async def menu(info:Update_menu):
    """Atualiza o estado do menu

    Aqui atualizaremos o estado do user solicitado.
    """
    apikey :str = str(info.APIKEY);
    id_user:int = int(info.id_user);
    estado :int = int(info.estado);
    retorno:dict = {};
    if(not banco.login_api_key(apikey)):
        retorno["Erro"] = "User sem autorização";
    elif(estado < 0):
        retorno["Erro"] = "Valor de estado do menu menor que zero";
    else:
        atualizado = banco.atualiza_estado_menu(
            id_user=id_user,
            estado=estado
        );
        if(atualizado):
            retorno["Sucesso"] = "Estado do menu modificado";
        else:
            retorno["Erro"] = "Estado do menu não modificado";
    return retorno;

@app.get("/api/qrcode")
async def gerador_qrcode(qrcode:Qrcode):
    """Gerador de QRCode

    Aqui nós geraremos um QRCode com o link enviado.
    """
    link = qrcode.link;
    img  = io.BytesIO();
    url  = pyqrcode.create(link);

    url.png(img,scale=8);
    img.seek(0);
    
    retorno = StreamingResponse(
        content = img, 
        media_type = "image/jpeg",
        headers = {
            'Content-Disposition': 'inline; filename="QRCode.jpg"'
        }
    );
    return retorno;
#-----------------------