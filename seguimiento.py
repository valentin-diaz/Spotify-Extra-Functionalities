import os
import json

from spotipy_client import SpotipyClient

import funciones as f

def main():
    scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
    spotipy_client = SpotipyClient(scope=scope)
    
    # url_playlist_tracked = input('Enlace de la playlist a la que seguir: ')
    urls_playlist_tracked = [
        'https://open.spotify.com/playlist/4fUtYGBX3dLZUNwkeUVU0C?si=8dcba40c00864e09',
        'https://open.spotify.com/playlist/45OtjePIeRGfLNIbJFuKq0?si=5ea20bc4ccbd437d'
        ]
    # url_playlist_target = input('Enlace de la playlist a la que actualizar automáticamente: ')
    url_playlist_target = 'https://open.spotify.com/playlist/0b2ypdNLBvMpTufMMm7wss?si=ef2afaf7299f4d30'

    id_playlist_target = f.id_playlist(url_playlist_target)

    for i in urls_playlist_tracked:
        print('=' * 45)
        print(f'CICLO {i}')
        id_playlist_tracked = f.id_playlist(i)

        # Obtener las canciones de la versión anterior de la playlist guardada en cache_playlists\
        ruta_cache = os.path.join('cache_playlists', f'{id_playlist_tracked}.json')
        if not os.path.exists(ruta_cache):
            spotipy_client.playlist_a_archivo(id_playlist_tracked)
        
        with open(ruta_cache, 'rb') as c:
            canciones_anteriores = json.load(c)['canciones']
        
        # Obtener las canciones de la versión actual de la playlist
        canciones_actuales = spotipy_client.obtener_canciones(id_playlist_tracked)

        print()
        print('ACTUALES')
        print(canciones_actuales)
        print('ANTERIORES')
        print(canciones_anteriores)

        canciones_agregar = set(canciones_actuales) - set(canciones_anteriores)
        canciones_eliminar = set(canciones_anteriores) - set(canciones_actuales)
        
        print()
        print('AGREGAR')
        print(canciones_agregar)
        print('QUITAR')
        print(canciones_eliminar)

        # Realizar los cambios en target
        spotipy_client.agregar_canciones_a_playlist(
            id_playlist=id_playlist_target,
            lista_canciones=list(canciones_agregar)
        )

        spotipy_client.playlist_a_archivo(id_playlist_tracked)

if __name__ == '__main__':
    main()