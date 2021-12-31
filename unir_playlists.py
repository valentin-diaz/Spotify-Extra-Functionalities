import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-modify-private playlist-modify-public playlist-read-private'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
            scope=scope,
            client_id = os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
        )
    )

def id_playlist(nombre_playlist : str) -> str:
    '''
    Retorna el id de una playlist en caso de
    '''

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
    cantidad = int(input('¿Cuántas listas deseas unir? '))
    listas = []
    for i in range(cantidad):
        id_lista = input(f'ID de la lista {i + 1}: ')
        listas.append(id_lista)

    nombre_lista_unida = input('Nombre de la nueva lista: ')
    id_lista_unida = crear_lista(nombre_lista_unida)

    print('Iniciando el merge...')
    print()
    canciones = []
    print('Obteniendo canciones...')
    for l in listas:
        canciones += obtener_canciones(l)
    
    print('Añadiendo canciones a la nueva lista...')
    agregar_canciones_a_playlist(id_lista_unida, canciones)

    print('Éxito')


if __name__ == '__main__':
    main()
