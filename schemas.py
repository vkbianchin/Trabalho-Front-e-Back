"""Formato dos dados que a API aceita (o Pydantic valida automaticamente)."""
from typing import Annotated

from pydantic import BaseModel, StringConstraints

Nome = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class Login(BaseModel):
    login: str
    senha: str


class Categoria(BaseModel):
    nome: Nome


class Fornecedor(BaseModel):
    nome: Nome
    contato: str | None = None


class Equipamento(BaseModel):
    nome: Nome
    patrimonio: str | None = None
    categoria_id: int
    fornecedor_id: int
