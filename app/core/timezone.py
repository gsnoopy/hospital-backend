from datetime import datetime
from zoneinfo import ZoneInfo

# [TIMEZONE CONSTANT]
# [Define o timezone padrão da aplicação como São Paulo]
# [ENTRADA: string "America/Sao_Paulo"]
# [SAIDA: ZoneInfo - objeto de timezone de São Paulo]
# [DEPENDENCIAS: ZoneInfo]
TIMEZONE = ZoneInfo("America/Sao_Paulo")

# [GET CURRENT TIME]
# [Retorna o horário atual no timezone de São Paulo]
# [ENTRADA: nenhuma]
# [SAIDA: datetime - horário atual de São Paulo com timezone]
# [DEPENDENCIAS: datetime.now, TIMEZONE]
def get_current_time():
    return datetime.now(TIMEZONE)

# [UTC TO SAO PAULO]
# [Converte datetime UTC para horário de São Paulo, adicionando timezone UTC se necessário]
# [ENTRADA: utc_dt - datetime em UTC (com ou sem timezone)]
# [SAIDA: datetime - horário convertido para São Paulo]
# [DEPENDENCIAS: ZoneInfo, TIMEZONE]
def utc_to_sao_paulo(utc_dt):
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC"))
    return utc_dt.astimezone(TIMEZONE)

# [SAO PAULO TO UTC]
# [Converte datetime de São Paulo para UTC, adicionando timezone de SP se necessário]
# [ENTRADA: sp_dt - datetime de São Paulo (com ou sem timezone)]
# [SAIDA: datetime - horário convertido para UTC]
# [DEPENDENCIAS: ZoneInfo, TIMEZONE]
def sao_paulo_to_utc(sp_dt):
    if sp_dt.tzinfo is None:
        sp_dt = sp_dt.replace(tzinfo=TIMEZONE)
    return sp_dt.astimezone(ZoneInfo("UTC"))

# [ENSURE TIMEZONE]
# [Garante que um datetime tenha timezone de São Paulo, convertendo se necessário]
# [ENTRADA: dt - datetime com ou sem timezone]
# [SAIDA: datetime - datetime com timezone de São Paulo]
# [DEPENDENCIAS: TIMEZONE]
def ensure_timezone(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=TIMEZONE)
    return dt.astimezone(TIMEZONE)