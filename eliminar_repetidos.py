from spotipy_client import SpotipyClient
import funciones as f

def main():
    scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
    spotipy_client = SpotipyClient(scope=scope)
    url_playlist = input('Enlace de la playlist a la que eliminar duplicados: ')

    id_lista = f.id_playlist(url_playlist)
    nombre_original = spotipy_client.nombre_playlist(url_playlist)
    nombre_nuevo = f'{nombre_original} - COPIA'

    print('Obteniendo canciones de la lista...')
    canciones = spotipy_client.obtener_canciones(id_lista)
    print('Eliminando elementos repetidos...')
    canciones = f.eliminar_repetidos(canciones)
    print()

    print('Creando copia de la lista...')
    id_copia = spotipy_client.crear_lista(nombre_nuevo)
    spotipy_client.agregar_canciones_a_playlist(id_copia, canciones)
    print(f'Éxito. La nueva lista fue creada con el nombre {nombre_nuevo}')

if __name__ == '__main__':
    main()
