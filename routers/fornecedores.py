from fastapi import APIRouter, Depends

from database import consultar, executar, get_conexao
from schemas import Fornecedor
from app.seguranca import usuario_logado

router = APIRouter(prefix="/api/fornecedores", dependencies=[Depends(usuario_logado)])


@router.get("")
def listar(db=Depends(get_conexao)):
    return consultar(db, "SELECT id, nome, contato FROM fornecedores ORDER BY id DESC")


@router.post("", status_code=201)
def criar(dados: Fornecedor, db=Depends(get_conexao)):
    novo_id = executar(db, "INSERT INTO fornecedores (nome, contato) VALUES (%s, %s)",
                       (dados.nome, dados.contato or None))
    return {"id": novo_id}


@router.delete("/{registro_id}", status_code=204)
def apagar(registro_id: int, db=Depends(get_conexao)):
    executar(db, "DELETE FROM fornecedores WHERE id = %s", (registro_id,))
