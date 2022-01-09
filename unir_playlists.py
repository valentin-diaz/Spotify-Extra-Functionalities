from spotipy_client import SpotipyClient

import funciones as f

def main():
    scope = 'playlist-modify-private playlist-modify-public playlist-read-private'
    spotipy_client = SpotipyClient(scope=scope)
    
    cantidad = int(input('¿Cuántas listas deseas unir? '))
    listas = []
    for i in range(cantidad):
        enlace_lista = input(f'ID de la lista {i + 1}: ')
        id_lista = f.id_playlist(enlace_lista)
        listas.append(id_lista)

    nombre_lista_unida = input('Nombre de la nueva lista: ')
    id_lista_unida = spotipy_client.crear_lista(nombre_lista_unida)

    print('Iniciando el merge...')
    print()
    canciones = []
    print('Obteniendo canciones...')
    for l in listas:
        canciones += spotipy_client.obtener_canciones(l)
    
    print('Añadiendo canciones a la nueva lista...')
    spotipy_client.agregar_canciones_a_playlist(id_lista_unida, canciones)

    print('Éxito')


if __name__ == '__main__':
    main()
