"""Hash de senha (bcrypt) e token JWT."""
import time

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import SECRET_KEY, TOKEN_HORAS

esquema = HTTPBearer(auto_error=False)   # lê o cabeçalho "Authorization: Bearer <token>"


def gerar_hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def conferir_senha(senha: str, hash_salvo: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_salvo.encode())


def criar_token(usuario: str) -> str:
    dados = {"sub": usuario, "exp": int(time.time()) + TOKEN_HORAS * 3600}
    return jwt.encode(dados, SECRET_KEY, algorithm="HS256")


def usuario_logado(credenciais: HTTPAuthorizationCredentials | None = Depends(esquema)) -> str:
    """Dependência: libera a rota só com token válido. Devolve o login do usuário."""
    try:
        return jwt.decode(credenciais.credentials, SECRET_KEY, algorithms=["HS256"])["sub"]
    except Exception:   # sem token, token falso ou expirado
        raise HTTPException(401, "Sessão inválida ou expirada. Entre novamente.")
