#-----------------------
# BIBLIOTECAS
#-----------------------
import os
from jose import jwt
from datetime import datetime, timedelta
#-----------------------
# CONSTANTES
#-----------------------
SECRET_KEY        :str = os.getenv('TOKEN_SECRET');
ALGORITHM         :str = "HS256";
EXPIRES_IN_MINUTES:int = (((60*24)*365)*5); # Teoricamente 5 anos
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES()
#-----------------------
def create_access_token(data:dict) -> str:
    dados         = data.copy();
    hora_agora    = datetime.utcnow();
    hora_relativa = timedelta(
        minutes=EXPIRES_IN_MINUTES
    );
    
    expiracao =  hora_agora + hora_relativa;
    
    dados.update({"exp":expiracao});

    token_jwt = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    );

    return token_jwt;

def verificar_access_token(token:str):
    payload:dict = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALGORITHM
    );
    return payload.get("sub");
#-----------------------
# Main()
#-----------------------
#-----------------------