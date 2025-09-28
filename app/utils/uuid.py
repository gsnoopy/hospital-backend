import uuid as py_uuid
import uuid_utils as uuid #type: ignore

# [UUID7 POSTGRES]
# [Gera UUID versão 7 compatível com PostgreSQL usando biblioteca uuid_utils]
# [ENTRADA: nenhuma]
# [SAIDA: py_uuid.UUID - UUID7 como objeto UUID padrão do Python]
# [DEPENDENCIAS: uuid_utils, py_uuid.UUID]
def uuid7_postgres():
    u7 = uuid.uuid7()
    return py_uuid.UUID(str(u7))
