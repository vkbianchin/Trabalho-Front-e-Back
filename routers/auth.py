from fastapi import APIRouter, Depends, HTTPException

from database import consultar, get_conexao
from schemas import Login
from seguranca import conferir_senha, criar_token

router = APIRouter(prefix="/api")


@router.post("/login")
def login(dados: Login, db=Depends(get_conexao)):
    usuarios = consultar(db, "SELECT login, senha FROM usuarios WHERE login = %s", (dados.login.strip(),))
    if not usuarios or not conferir_senha(dados.senha, usuarios[0]["senha"]):
        raise HTTPException(401, "Login ou senha incorretos.")
    return {"token": criar_token(usuarios[0]["login"]), "usuario": usuarios[0]["login"]}
