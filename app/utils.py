from datetime import datetime
from models import Branch, db
import subprocess
import redis
import time
import os
from flask import current_app

# Configuração do Redis
LOCK_KEY = "update_asset_status_lock"
LOCK_TIMEOUT = 360  # 6 minutos

redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', '127.0.0.1'),
    port=int(os.getenv('REDIS_PORT', '6379')),
    db=0,
    decode_responses=True
)

# Função para obter o uptime de um ativo
def get_asset_uptime(branch_number):
    """Obtém o uptime de um ativo baseado no campo last_online."""
    # Verifica o uptime no Redis primeiro
    uptime = redis_client.get(f"asset_uptime:{branch_number}")
    if uptime:
        return uptime  # Se encontrado no Redis, retorna diretamente

    # Caso não tenha no Redis, consulta o banco de dados
    asset = Branch.query.filter_by(branch_number=branch_number).first()
    if asset:
        uptime = asset.get_uptime()
        redis_client.setex(f"asset_uptime:{branch_number}", 120, uptime)  # Armazena no Redis por 1 hora
        return uptime

    return "Ativo não encontrado"

# Função para verificar se o host está online
def is_host_online(ip):
    """Verifica se o host está online via ping."""
    try:
        subprocess.check_output(['ping', '-c', '1', ip], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

# Atualiza o status dos ativos no Redis e no banco de dados
def update_asset_status(app):
    with app.app_context():
        if redis_client.setnx(LOCK_KEY, time.time() + LOCK_TIMEOUT):
            try:
                redis_client.expire(LOCK_KEY, LOCK_TIMEOUT)  # Expira o lock
                print("Executando update_asset_status")

                # Atualiza o status dos ativos
                assets = Branch.query.all()
                for asset in assets:
                    branch_key = asset.branch_number  # Identificador único
                    redis_status = redis_client.get(f"asset_status:{branch_key}")

                    if redis_status:
                        asset.status = redis_status  # Usa valor do Redis se presente
                    else:
                        # Verifica o status do ativo via ping
                        if is_host_online(asset.ip_address):
                            if asset.status == "offline":
                                asset.status = "online"
                                asset.last_online = datetime.utcnow()

                                # Armazena status e uptime no Redis
                                redis_client.setex(f"asset_status:{branch_key}", 120, "online")
                                uptime = asset.get_uptime()
                                redis_client.setex(f"asset_uptime:{branch_key}", 120, uptime)
                        else:
                            if asset.status == "online":
                                asset.status = "offline"
                                asset.last_online = None
                                redis_client.setex(f"asset_status:{branch_key}", 120, "offline")

                db.session.commit()

            finally:
                redis_client.delete(LOCK_KEY)  # Libera o lock
        else:
            # Caso o lock ainda exista, verifica a expiração
            lock_value = redis_client.get(LOCK_KEY)
            if lock_value and float(lock_value) < time.time():
                print("Lock expirado. Reassumindo controle.")
                redis_client.set(LOCK_KEY, time.time() + LOCK_TIMEOUT)
            else:
                print("update_asset_status já está em execução. Aguardando o próximo ciclo.")

# Função para alternar a visibilidade de um ativo
def toggle_asset_visibility(branch_number):
    """Alterna a visibilidade de um ativo."""
    asset = Branch.query.filter_by(branch_number=branch_number).first()
    if asset:
        asset.visible = not asset.visible
        db.session.commit()
        # Atualiza a visibilidade no Redis
        redis_client.setex(f"asset_visibility:{branch_number}", 120, asset.visible)

# Função para obter o uptime do sistema
def get_system_uptime():
    """Retorna o uptime do sistema."""
    try:
        uptime = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
        return uptime
    except subprocess.CalledProcessError:
        return "Erro ao obter o uptime"

