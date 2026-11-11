from fastapi import APIRouter, Depends

from database import consultar, executar, get_conexao
from schemas import Equipamento
from seguranca import usuario_logado

router = APIRouter(prefix="/api/equipamentos", dependencies=[Depends(usuario_logado)])


@router.get("")
def listar(db=Depends(get_conexao)):
    # JOIN: troca os ids pelos nomes da categoria e do fornecedor
    return consultar(db, """
        SELECT e.id, e.nome, e.patrimonio, c.nome AS categoria, f.nome AS fornecedor
        FROM equipamentos e
        JOIN categorias c ON c.id = e.categoria_id
        JOIN fornecedores f ON f.id = e.fornecedor_id
        ORDER BY e.id DESC""")


@router.post("", status_code=201)
def criar(dados: Equipamento, db=Depends(get_conexao)):
    novo_id = executar(
        db,
        "INSERT INTO equipamentos (nome, patrimonio, categoria_id, fornecedor_id) VALUES (%s, %s, %s, %s)",
        (dados.nome, dados.patrimonio or None, dados.categoria_id, dados.fornecedor_id))
    return {"id": novo_id}


@router.delete("/{registro_id}", status_code=204)
def apagar(registro_id: int, db=Depends(get_conexao)):
    executar(db, "DELETE FROM equipamentos WHERE id = %s", (registro_id,))
