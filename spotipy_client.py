import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotipyClient:
    def __init__(self, scope) -> None:
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=scope,
                client_id = os.getenv('SPOTIPY_CLIENT_ID'),
                client_secret = os.getenv('SPOTIPY_CLIENT_SECRET'),
                redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
                )
            )
    
    def nombre_playlist(self, enlace_playlist : str) -> str:
        '''
        Retorna el nombre de una playlist dado su enlace
        '''
        respuesta = self.sp.playlist(
            enlace_playlist,
            fields='name'
        )
        return respuesta['name']
    
    def obtener_canciones(self, id_playlist : str) -> list:
        '''
        Retorna una lista con las id's de todas las canciones pertenecientes a la playlist
        '''
        canciones = []
        respuesta = self.sp.playlist_items(
            id_playlist
        )
        while True:
            for item in respuesta['items']:
                canciones.append(item['track']['id'])
            if respuesta['next']:
                respuesta = self.sp.next(respuesta)
            else:
                return canciones
    
    def obtener_listas_usuario(self):
        listas_usuario = []
        respuesta = self.sp.current_user_playlists()
        while True:
            for item in respuesta['items']:
                listas_usuario.append(
                    {'Nombre' : item['name'], 'ID' : item['id']}
                    )
            if respuesta['next']:
                respuesta = self.sp.next(respuesta)
            else:
                return listas_usuario
    
    def crear_lista(self, nombre : str) -> str:
        '''
        Crea una nueva playlist y retorna su id
        '''
        self.sp.user_playlist_create(
            user=self.sp.me()['id'],
            name=nombre
        )
        for l in self.obtener_listas_usuario():
            if l['Nombre'] == nombre:
                return l['ID']
    
    def agregar_canciones_a_playlist(self, id_playlist : str, lista_canciones : list):
        for i in range(0, len(lista_canciones), 100):
            self.sp.playlist_add_items(
                id_playlist,
                lista_canciones[i : i + 100]
            )