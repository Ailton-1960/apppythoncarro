import pandas as pd
import pymysql

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'sidef2'
}
conn = pymysql.Connect(**config)
id_usuario = 'ailtonfernandes'
cursor = conn.cursor()
cursor.execute("SELECT * FROM sd_usuarios WHERE usuario = %s LIMIT 1", (id_usuario,))
resultado = cursor.fetchall()
descricao = cursor.description

#dr = pd.DataFrame(resultado)
dd = pd.DataFrame(descricao)
# df.info()
#print(dd[0])
print(dd[0])
cursor.close()
conn.close()
