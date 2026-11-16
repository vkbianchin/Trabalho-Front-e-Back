"""Ponto de entrada. Rode com:  uvicorn main:app --reload"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import consultar, executar, pool
from routers import auth, categorias, equipamentos, fornecedores
from seguranca import gerar_hash

PASTA = Path(__file__).parent


@asynccontextmanager
async def inicio(_app):
    """Ao ligar o servidor, cria o usuário admin se a tabela estiver vazia."""
    conexao = pool.get_connection()
    try:
        if not consultar(conexao, "SELECT id FROM usuarios LIMIT 1"):
            executar(conexao, "INSERT INTO usuarios (login, senha) VALUES (%s, %s)",
                     ("admin", gerar_hash("admin123")))
    finally:
        conexao.close()
    yield


app = FastAPI(title="Controle de equipamentos", lifespan=inicio)

for modulo in (auth, categorias, fornecedores, equipamentos):
    app.include_router(modulo.router)


# Erros no formato {"erro": "..."}, que é o que o JS do front lê
@app.exception_handler(StarletteHTTPException)
async def erro_http(_req: Request, erro: StarletteHTTPException):
    return JSONResponse({"erro": erro.detail}, status_code=erro.status_code)


@app.exception_handler(RequestValidationError)
async def erro_validacao(_req: Request, _erro: RequestValidationError):
    return JSONResponse({"erro": "Preencha todos os campos obrigatórios."}, status_code=400)


app.mount("/static", StaticFiles(directory=PASTA / "static"), name="static")


@app.get("/", include_in_schema=False)
def pagina():
    return FileResponse(PASTA / "static" / "index.html")
