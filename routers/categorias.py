from fastapi import APIRouter, Depends

from database import consultar, executar, get_conexao
from schemas import Categoria
from app.seguranca import usuario_logado

# dependencies=...: todas as rotas daqui exigem token válido
router = APIRouter(prefix="/api/categorias", dependencies=[Depends(usuario_logado)])


@router.get("")
def listar(db=Depends(get_conexao)):
    return consultar(db, "SELECT id, nome FROM categorias ORDER BY id DESC")


@router.post("", status_code=201)
def criar(dados: Categoria, db=Depends(get_conexao)):
    return {"id": executar(db, "INSERT INTO categorias (nome) VALUES (%s)", (dados.nome,))}


@router.delete("/{registro_id}", status_code=204)
def apagar(registro_id: int, db=Depends(get_conexao)):
    executar(db, "DELETE FROM categorias WHERE id = %s", (registro_id,))
