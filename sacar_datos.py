import os
import json
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import nest_asyncio
from collections import defaultdict
from itertools import chain
import random

# Crear un archivo usuarios.txt con el siguiente formato y ejecutar el comando
# !twscrape add_accounts ./usuarios.txt username:password:email:email_password
# !twscrape login_accounts

"""
    Abre el archivo json ya existente y va añadiendo claves y valores.
    Los valores siguen a la clave.
    Partimos de un nodo inicial, un "influencer" en el aŕea de la tecnología
    y sacamos sus seguidores, juntamos todos los seguidores y elegimos un perfil aleatorio
    del cual seguir sacando seguidores y así sucesivamente (aplanamos todos los perfiles 
    para elegir entre ellos)
"""

def iniciar():
    comando = "twscrape relogin_failed"
    os.system(comando)


def guardar():
# Cargar el archivo JSON existente
    with open('result.json', 'r') as fp:
        aux = json.load(fp)
    
    # Actualizar el diccionario con nuevos valores
    for clave, valor in diccionario_seguimientos.items():
        if clave in aux:
            aux[clave] += valor
        else:
            # Si la clave no existe, añadir la nueva clave con su valor
            aux[clave] = valor
    
    # Guardar el diccionario actualizado en el mismo archivo
    with open('result.json', 'w') as fp:
        json.dump(aux, fp)
        

nest_asyncio.apply()


diccionario_seguimientos = {}

async def main(id_usuario:int):
    global diccionario_seguimientos
    api = API()  # or API("path-to.db") - default is `accounts.db`

    # ADD ACCOUNTS (for CLI usage see BELOW)
    await api.pool.login_all()

    # or add account with COOKIES (with cookies login not required)
    messages = {}
    aplanado = []
    user_id = id_usuario
    k = 0
    while  True:

        iniciar()
        print(len(aplanado))
        async for mensaje in api.followers(user_id, limit=500):
            """
                añadimos los id de los usuarios que le siguen a la clave del influencer
            """
            if user_id not in messages:
                messages[user_id] = [mensaje.id]
            else:
                messages[user_id] = messages[user_id] + [mensaje.id]
            
        """
            si no tiene seguidores dejamos vacio (o en caso de que la api de twitter no responda)
        """
        if user_id not in messages:
                messages[user_id] = []
            
        """
            aplanamos todos los nodos que tengamos (salvo el inicial), 
            elegimos uno al azar para sacar sus seguidores
        """
        while user_id in messages:
            aplanado =  list(chain.from_iterable(messages.values()))
            indice = random.randint(0, len(aplanado))
            user_id = aplanado[indice]
        
        """
            Guardamos el progreso
        """
        guardar()
        diccionario_seguimientos.update(messages)
    

if __name__ == "__main__":
    asyncio.run(main(285764222))
    