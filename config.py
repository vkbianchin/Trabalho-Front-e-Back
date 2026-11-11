"""Configurações lidas do arquivo .env (ou das variáveis de ambiente)."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")   # carrega o .env que está ao lado deste arquivo

# Banco MySQL. Com túnel SSH, host/porta são os vistos DE DENTRO do servidor (normalmente 127.0.0.1:3306).
DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "controle_equipamentos"),
    autocommit=True,   # cada comando já é gravado na hora
)

# Túnel SSH (opcional). Se SSH_HOST estiver vazio ou ausente, conecta direto ao MySQL.
SSH = dict(
    host=os.getenv("SSH_HOST"),
    port=int(os.getenv("SSH_PORT", "22")),
    user=os.getenv("SSH_USER"),
    password=os.getenv("SSH_PASSWORD"),
)

SECRET_KEY = os.getenv("SECRET_KEY", "troque-esta-chave")   # assina os tokens
TOKEN_HORAS = 8                                              # validade do token
