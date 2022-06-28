"""Banco de Dados SqLite"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import os
import typing
import sqlite3
from .database import DataBase
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DataBaseSqlite(DataBase):
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_isAlive'):
            cls._isAlive = super().__new__(cls);
        return cls._isAlive;

    def __init__(self) -> None:
        """Banco de Dados SqLite

        Aqui utilizaremos o banco de dados SqLite.
        """
        caminho:str = os.path.dirname(
            os.path.realpath('~/')
        );
        pasta  :str = os.path.join(caminho,"data");
        arquivo:str = "database.db";

        if(not(os.path.exists(pasta))):
            os.mkdir(pasta);
        
        self.nome:str = os.path.join(pasta,arquivo);
        self.__create_table();
        self._create_admin();
        mensagem:str = (
            f"\n\n\n\n"
            f"APIKEY do ADM = "
            f"{self.apiKey_Adm}"
            f"\n\n\n\n"
        );
        print(mensagem);
    # -----------------------
    # Funções estáticas
    # -----------------------
    @staticmethod
    def __corrigir_comando(comando:str) -> str:
        """Corrigir Comando
        Aqui fazemos a mudança do sql do MariaDB para o SqLite.
        """
        now     = "(SELECT DATETIME('now','localtime'))";
        comando = comando.replace('%s','?');
        comando = comando.replace('now()',now);
        return comando;
    # -----------------------
    # Conexão e Criação
    # -----------------------
    def _connection(self) -> sqlite3.Connection:
        connection:sqlite3.Connection = sqlite3.connect(self.nome,timeout=1);
        return connection;
    
    def __create_table(self) -> None:
        """Create table

        :return - None

        Aqui nós fazemos a criação das tabelas.
        """
        comandos:list[str] = [
            (   
                " CREATE TABLE IF NOT EXISTS menu( "
                " id_user	INTEGER NOT NULL UNIQUE, "
                " estado	INTEGER NOT NULL) "
            ),
            (
                " CREATE TABLE IF NOT EXISTS api_key( "
                " id 	  INTEGER PRIMARY KEY "
                " AUTOINCREMENT NOT NULL UNIQUE, "
                " apikey  TEXT  NOT NULL UNIQUE, "
                " tipo	  TEXT	NOT NULL) "
            ),
            (
                " CREATE TABLE IF NOT EXISTS cliente( "
                " username  TEXT NOT NULL UNIQUE, "
                " senha  TEXT NOT NULL, "
                " id_key INTEGER NOT NULL UNIQUE, "
                " FOREIGN KEY(id_key) REFERENCES "
                " api_key (id) ON DELETE NO ACTION "
                " ON UPDATE NO ACTION) "
            )
        ];

        for comando in comandos:
            self.__execute_create(comando=comando);
    
    def __execute_create(self,comando:str) -> None:
        """Execute create

        :param  - comando:str
        :return - None

        Aqui nós executamos os comandos de criação passados
        pelo argumento 'comando'.
        """
        try:
            Connection = self._connection();
            cursor = Connection.cursor();
            cursor.execute(comando);
            Connection.commit();
            cursor.close();
        except sqlite3.OperationalError:
            if cursor:
                cursor.close();
            self.__execute_create(comando=comando);
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    def _insert(self,comando:str,tupla:tuple) -> None:
        comando = self.__corrigir_comando(comando=comando);
        try:
            cnxn   = self._connection();
            cursor = cnxn.cursor();
            cursor.execute(comando, tupla);
            cnxn.commit();
        except sqlite3.OperationalError:
            self._insert(comando=comando,tupla=tupla);
        except sqlite3.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            
    # Read
    def _select(self,comando:str) -> typing.List[typing.Tuple[str]]:
        comando = self.__corrigir_comando(comando=comando);
        retorno:list[str] = [];
        try:
            cnxn   = self._connection();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            retorno = cursor.fetchall();
        except sqlite3.OperationalError:
            self._select(comando=comando);
        except sqlite3.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            
            return retorno;
    # Update
    def _update(self,comando:str) -> None:
        comando = self.__corrigir_comando(comando=comando);
        try:
            cnxn   = self._connection();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            cnxn.commit();
        except sqlite3.OperationalError:
            self._update(comando=comando);
        except sqlite3.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            
    # Delete
    def _delete(self,comando:str) -> None:
        comando = self.__corrigir_comando(comando=comando);
        try:
            cnxn   = self._connection();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            cnxn.commit();
        except sqlite3.OperationalError:
            self._delete(comando=comando);
        except sqlite3.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
if(__name__ == "__main__"):
    pass; 
#-----------------------