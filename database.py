"""Conexão com o MySQL (pool) e funções auxiliares de consulta."""
import mysql.connector
from fastapi import HTTPException
from mysql.connector import pooling

from sshtunnel import SSHTunnelForwarder

from config import DB, SSH

config_db = dict(DB)
if SSH["host"]:
    # Abre o túnel: o MySQL do servidor passa a aparecer numa porta local deste computador.
    tunel = SSHTunnelForwarder(
        (SSH["host"], SSH["port"]),
        ssh_username=SSH["user"],
        ssh_password=SSH["password"],
        remote_bind_address=(DB["host"], DB["port"]),
    )
    tunel.start()
    config_db.update(host="127.0.0.1", port=tunel.local_bind_port)

pool = pooling.MySQLConnectionPool(pool_name="equipamentos", pool_size=5, **config_db)

# código de erro do MySQL -> mensagem para o usuário
MENSAGENS = {
    1062: "Já existe um registro com esse nome ou patrimônio.",
    1451: "Este registro está em uso por algum equipamento.",
    1452: "Categoria ou fornecedor inválido.",
}


def get_conexao():
    """Dependência do FastAPI: pega uma conexão do pool e a devolve no final do pedido."""
    conexao = pool.get_connection()
    try:
        yield conexao
    finally:
        conexao.close()


def consultar(conexao, sql, params=()):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(sql, params)
    linhas = cursor.fetchall()
    cursor.close()
    return linhas


def executar(conexao, sql, params=()):
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, params)
        return cursor.lastrowid
    except mysql.connector.IntegrityError as erro:
        raise HTTPException(409, MENSAGENS.get(erro.errno, "Não foi possível salvar."))
    finally:
        cursor.close()
