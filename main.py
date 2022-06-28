"""Api do Bot do Telegram"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import io
import pyqrcode
from db import *
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, validator, constr
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class Qrcode(BaseModel):
    """Qrcode
    
    Aqui nós iremos colocar os dados para a criação de um QRCode.
    
    Para isso nós precisaremos do link que virará um QRCode.
    """ 
    link:str = None;

    @validator('link')
    def verificar_link(cls, link):
        if((link == None) or (link == '')):
            raise ValueError('Valor do link errado');
        return link;

class User(BaseModel):
    """User
    
    Aqui nós iremos colocar os dados do usuário.
    
    Para isso nós precisaremos:
    \n\tUsername do novo usuário.
    \n\tSenha do novo usuário.
    """
    username:constr(max_length=30,min_length=5);
    senha   :constr(max_length=30,min_length=5);

    @validator('username')
    def verificar_username(cls, username):
        if((username == None) or (username.replace(" ", "") == '')):
            raise ValueError('Valor do username errado');
        return username;
    
    @validator('senha')
    def verificar_senha(cls, senha):
        if((senha == None) or (senha == '')):
            raise ValueError('Valor da senha errado');
        return senha;

class Insert_user(User):
    """Insert User
    
    Aqui nós iremos colocar os dados para inserção de um usuário.
    
    Para isso nós precisaremos:
    \n\tUsername do novo usuário.
    \n\tSenha do novo usuário.
    \n\tAPIKEY de um usuário administrador.
    \n\tTipo do usuário.
    """ 
    APIKEY:str       = None;
    tipo  :Tipo_user = None;

    @validator('APIKEY')
    def verificar_apikey(cls, apikey):
        if len(apikey) <= 10:
            raise ValueError('Valor de Apikey falsa');
        return apikey;
    
    @validator('tipo')
    def verificar_tipo(cls, tipo):
        return str(tipo);

class Menu(BaseModel):
    """Menu
    
    Aqui nós iremos colocar os dados do menu.
    
    Para isso nós precisaremos:
    \n\tID do usuário.
    \n\tAPIKEY de um usuário administrador.
    """
    id_user:int = None;
    APIKEY :str = None;

    @validator('id_user')
    def verificar_id(cls, id):
        if(id <= 0):
            raise ValueError('Valor do ID menor igual a zero');
        return id;
    
    @validator('APIKEY')
    def verificar_apikey(cls, apikey):
        if(len(apikey) <= 10):
            raise ValueError('Valor de Apikey falsa');
        return apikey;

class Update_menu(Menu):
    """Update Menu
    
    Aqui nós iremos atualizar os dados do menu.
    
    Para isso nós precisaremos:
    \n\tID do usuário.
    \n\tAPIKEY de um usuário administrador.
    \n\testado do usuário.
    """
    estado:int = None;

    @validator('estado')
    def verificar_estado(cls, estado):
        if(estado < 0):
            raise ValueError('Valor do estado menor a zero');
        return estado;
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