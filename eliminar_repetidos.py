import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from collections import OrderedDict

scope = 'playlist-modify-private playlist-modify-public playlist-read-private'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
            scope=scope,
            client_id = os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        )
    )

def id_playlist(enlace_playlist : str) -> str:
    '''
    Retorna el id de una playlist dado su enlace
    '''
    pos1 = enlace_playlist.find('playlist/') + len('playlist/')
    pos2 = enlace_playlist.find('?')
    id_playlist = enlace_playlist[pos1 : pos2]
    return id_playlist

def nombre_playlist(enlace_playlist : str) -> str:
    '''
    Retorna el nombre de una playlist dado su enlace
    '''
    respuesta = sp.playlist(
        enlace_playlist,
        fields='name'
    )
    return respuesta['name']

def eliminar_repetidos(lista_ids : list) -> list:
    '''
    Recibe una lista de ids de canciones con posibles repetidos, y retorna una copia de la lista
    sólo con elementos únicos
    '''
    nueva_lista = list(OrderedDict.fromkeys(lista_ids))
    return nueva_lista

def obtener_canciones(id_playlist : str) -> list:
    '''
    Retorna una lista con las id's de todas las canciones pertenecientes a la playlist
    '''
    canciones = []
    respuesta = sp.playlist_items(
        id_playlist
    )
    while True:
        for item in respuesta['items']:
            canciones.append(item['track']['id'])
        if respuesta['next']:
            respuesta = sp.next(respuesta)
        else:
            return canciones

def obtener_listas_usuario():
    listas_usuario = []
    respuesta = sp.current_user_playlists()
    while True:
        for item in respuesta['items']:
            listas_usuario.append(
                {'Nombre' : item['name'], 'ID' : item['id']}
                )
        if respuesta['next']:
            respuesta = sp.next(respuesta)
        else:
            return listas_usuario

def crear_lista(nombre : str) -> str:
    '''
    Crea una nueva playlist y retorna su id
    '''
    sp.user_playlist_create(
        user=sp.me()['id'],
        name=nombre
    )
    for l in obtener_listas_usuario():
        if l['Nombre'] == nombre:
            return l['ID']


def agregar_canciones_a_playlist(id_playlist : str, lista_canciones : list):
    for i in range(0, len(lista_canciones), 100):
        sp.playlist_add_items(
            id_playlist,
            lista_canciones[i : i + 100]
        )

def main():
    url_playlist = input('Enlace de la playlist a la que eliminar duplicados: ')

    id_lista = id_playlist(url_playlist)
    nombre_original = nombre_playlist(url_playlist)
    nombre_nuevo = f'{nombre_original} - COPIA'

    print('Obteniendo canciones de la lista...')
    canciones = obtener_canciones(id_lista)
    print('Eliminando elementos repetidos...')
    canciones = eliminar_repetidos(canciones)
    print()

    print('Creando copia de la lista...')
    id_copia = crear_lista(nombre_nuevo)
    agregar_canciones_a_playlist(id_copia, canciones)
    print(f'Éxito. La nueva lista fue creada con el nombre {nombre_nuevo}')

if __name__ == '__main__':
    main()
