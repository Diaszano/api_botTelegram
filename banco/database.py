"""Banco de Dados abstrato"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import typing
import secrets
from enum import Enum
from typing import Union
from pydantic import BaseModel
from abc import ABC, abstractmethod
#-----------------------
# CONSTANTES
#-----------------------
SENHA_ADM:str = "h4fc3cpBAn2YLlO3BKw4XA";
#-----------------------
# CLASSES
#-----------------------
class Tipo_user(Enum):
    def __str__(self):
        return self.name.upper();
    
    def __repr__(self):
        return f"{self}".upper();
    
    Padrao = 1;
    Administrador = 2;

class User(BaseModel): 
    username: str
    senha   : str

class Insert_user(User):
    APIKEY  : str
    tipo    : Tipo_user

class DataBase(ABC):
    # -----------------------
    # Criação e conexão
    # -----------------------
    @abstractmethod
    def _connection(self):
        """Conexão

        :return - Connection

        Aqui nós fazemos a conexão com o banco de dados e 
        retornamos a mesma.
        """
        pass;
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    @abstractmethod
    def _insert(self,comando:str,tupla:tuple) -> None:
        """Insert

        :param  - comando:str
        :param  - tupla:tuple
        :return - None

        Aqui nós executamos o insert no banco com os argumentos 
        'comando' e 'tupla'.
        """
        pass;
            
    # Read
    @abstractmethod
    def _select(self,comando:str) -> typing.List[typing.Tuple[str]]:
        """Select

        :param  - comando:str
        :return - None

        Aqui nós executamos o select no banco com o argumento 
        'comando'.
        """ 
        pass;

    # Update
    @abstractmethod
    def _update(self,comando:str) -> None:
        """Update

        :param  - comando:str
        :return - None

        Aqui nós executamos o select no banco com o argumento 
        'comando'.
        """
        pass;
            
    # Delete
    @abstractmethod
    def _delete(self,comando:str) -> None:
        """Delete

        :param  - comando:str
        :return - None

        Aqui nós executamos o delete no banco com o argumento 
        'comando'.
        """
        pass;
    # -----------------------
    # Menu
    # -----------------------     
    def pega_estado_menu(self,id_user:int=-1) -> int:
        """Pega o estado do menu principal

        :param  - id_user:str
        :return - estado:int

        Aqui procuraremos o estado do user no programa
        """
        retorno:int = -1;
        if(not isinstance(id_user,int)):
            return retorno;
        elif(id_user <= 0):
            return retorno;
        comando_select:str = (
            f" SELECT estado "
            f" FROM menu "
            f" WHERE id_user = {id_user}"
        );

        retorno_select:list[str] = self._select(
            comando=comando_select
        );

        if(retorno_select == []):
            comando_insert:str = (
                " INSERT INTO menu "
                " (id_user, estado) "
                " VALUES(%s, 0) "
            );
            tupla_insert:tuple = (id_user,);
            self._insert(
                comando=comando_insert,
                tupla=tupla_insert
            )
            retorno = self.pega_estado_menu(
                id_user=id_user
            );
        else:
            retorno = int(retorno[0][0]);
        return retorno;

    def atualiza_estado_menu(self,id_user:int=-1,estado:int = 0) -> None:
        """Atualiza o estado do menu principal

        :param  - id_user:str
        :param  - estado:int
        :return - None

        Aqui atualizaremos o estado do user
        """
        if(not isinstance(id_user,int)):
            return;
        elif(id_user <= 0):
            return;
        comando_update:str = ( 
            f" UPDATE menu "
            f" SET estado={estado} "
            f" WHERE id_user={id_user} "
        );
        self._update(
            comando=comando_update
        );
    # -----------------------
    # Auth
    # ----------------------- 
    def _user_existe(self,username:str) -> bool:
        """Checar user

        :param  - username:str
        :return - None
        
        Retorna True se existe o user.

        Aqui checaremos se o user está utilizando a api.
        """
        retorno:bool = False;

        if(not(isinstance(username,str))):
            return retorno;
        elif(username == ''):
            return retorno;
        
        comando_select:str = (
            f" SELECT * "
            f" FROM cliente "
            f" WHERE username = '{username}' "
        );
        retorno_select:list[str] = self._select(
            comando=comando_select
        );
        
        if(retorno_select != []):
            retorno = True;
        return retorno;
    
    def _login_api(self,username:str,senha:str) -> bool:
        """Login api

        :param  - username:str
        :param  - senha:str
        :return - None

        Retorna True se efetuou o login.

        Aqui checaremos se o user que está utilizando a api existe.
        """
        retorno:bool = False;

        if(not(isinstance(username,str) and isinstance(senha, str))):
            return retorno;
        elif((username == '') or (senha == '')):
            return retorno;
        
        if(not self._user_existe(username)):
            return retorno;

        comando_select:str = (
            f" SELECT * "
            f" FROM cliente "
            f" WHERE username = '{username}' "
            f" AND senha = '{senha}' "
        );
        retorno_select:list[str] = self._select(
            comando=comando_select
        );
        if(retorno_select != []):
            retorno = True;
        return retorno;
    
    def get_apiKey_user(self,username:str,senha:str)-> Union[str,None]:
        """Pegar ApiKey do user

        :param  - username:str
        :param  - senha:str
        :return - str|None

        Aqui nós pegaremos a apiKey do user.
        """
        retorno:Union[str,None] = None;
        if(not self._login_api(username,senha)):
            return retorno;
        
        comando_select:str = (
            f" SELECT apikey "
            f" FROM cliente "
            f" INNER JOIN api_key "
            f" WHERE username = '{username}' "
            f" AND senha = '{senha}' "
            f" AND id_key = api_key.id "
        );
        retorno_select:list[str] = self._select(
            comando=comando_select
        );

        if(retorno_select != []):
            retorno = retorno_select[0][0];
        
        return retorno;
    
    def _checar_apiKey(self,apikey:str) -> bool:
        """Checar apiKey

        :param  - apikey:str
        :return - bool

        Retorna verdadeira se não existe 
        nenhum user com essa key.

        Checar se já existe essa apiKey.
        """
        retorno:bool = False;
        if(not isinstance(apikey,str)):
            return retorno;
        elif(apikey == ''):
            return retorno;
        
        comando_select:str = (
            f" SELECT * "
            f" FROM api_key "
            f" WHERE apikey = '{apikey}' "
        );
        retorno_select:list[str] = self._select(
            comando=comando_select
        );
        
        if(retorno_select == []):
            retorno = True;
        return retorno;
    
    def _checar_privilegios(self,apikey:str) -> bool:
        """Checar privilégios

        :param  - apikey:str
        :return - bool

        Retorna verdadeira se user for ADM
        e false se o user for padrão.

        Checar se já existe essa apiKey.
        """
        retorno:bool = False;

        if(not isinstance(apikey,str)):
            return retorno;
        elif(apikey == ''):
            return retorno;
        
        if(self._checar_apiKey(apikey)):
            return retorno;
        
        comando_select:str = (
            f" SELECT tipo "
            f" FROM api_key "
            f" WHERE apikey = '{apikey}' "
        );
        retorno_select:list[str] = self._select(
            comando=comando_select
        );

        tipo:str = '';
        
        if(retorno_select != []):
            tipo = retorno_select[0][0].upper();

        if(tipo == str(Tipo_user(2))):
            retorno = True;
        
        return retorno;
    
    def _create_apiKey(self,tipo:Tipo_user) -> str:
        """Criação de apiKey

        :return - str

        Aqui nós criaremos a apiKey do user.
        """
        apikey:str = "";
        tipo  :str = str(tipo);

        while True:
            apikey:str = secrets.token_urlsafe(16);
            if(self._checar_apiKey(apikey=apikey)):
                break
        
        tupla_insert:tuple = (apikey,tipo,);

        comando_insert:str = (
            f" INSERT INTO api_key "
            f" (apikey, tipo) "
            f" VALUES(%s,%s) "
        );

        self._insert(
            comando=comando_insert,
            tupla=tupla_insert
        );

        
        comando_select:str = (
            f" SELECT id "
            f" FROM api_key "
            f" WHERE apikey = '{apikey}' "
        );
        retorno_select = self._select(
            comando=comando_select
        );
        
        if(retorno_select == []):
            return self._create_apiKey(tipo);

        return retorno_select[0][0];

    def create_user(self,username:str,senha:str,tipo:str,apikey:str) -> dict:
        """Criação de novos users

        :param  - username:str
        :param  - senha:str
        :param  - tipo:str
        :param  - apikey:str
        :return - str|None

        Aqui nós pegaremos a apiKey do user.
        """
        retorno:dict = {};

        if(not self._checar_privilegios(apikey)):
            retorno['Erro'] = "User sem autorização";
            return retorno;
        if(self._user_existe(username)):
            retorno['Erro'] = "User já existente";
            return retorno;
        
        id_apikey:str = self._create_apiKey(
            tipo=tipo
        );
        
        tupla_insert:tuple = (username,senha,id_apikey,);
        comando_insert:str = (
            f" INSERT INTO cliente "
            f" (username, senha, id_key) "
            f" VALUES(%s,%s,%s) "
        );
        
        self._insert(
            comando=comando_insert,
            tupla=tupla_insert
        );

        retorno["APIKEY"] = self.get_apiKey_user(
            username=username,
            senha=senha
        );

        return retorno;
    # -----------------------
    # Create Admin
    # -----------------------
    def _create_admin(self) -> dict:
        """Criação do ADM

        :return - None

        Aqui nós criaremos o adm.
        """

        username:str       = "admin";
        senha   :str       = SENHA_ADM;
        tipo    :Tipo_user = Tipo_user(2);

        if(self._user_existe(username)):
            self.__get_apikey_adm(
                username=username,
                senha=senha
            )
            return;
        
        id_apikey:str = self._create_apiKey(
            tipo=tipo
        );
        
        tupla_insert:tuple = (username,senha,id_apikey,);
        comando_insert:str = (
            f" INSERT INTO cliente "
            f" (username, senha, id_key) "
            f" VALUES(%s,%s,%s) "
        );
        
        self._insert(
            comando=comando_insert,
            tupla=tupla_insert
        );

        self.__get_apikey_adm(
            username=username,
            senha=senha
        );

    def __get_apikey_adm(self,username,senha):
        
        retorno:str = self.get_apiKey_user(
            username=username,
            senha=senha
        );

        self.apiKey_Adm = retorno;
    # -----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
if(__name__ == "_main_"):
    pass; 
#-----------------------