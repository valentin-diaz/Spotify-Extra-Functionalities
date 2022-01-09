from collections import OrderedDict

def id_playlist(enlace_playlist : str) -> str:
    '''
    Retorna el id de una playlist dado su enlace
    '''
    pos1 = enlace_playlist.find('playlist/') + len('playlist/')
    pos2 = enlace_playlist.find('?')
    id_playlist = enlace_playlist[pos1 : pos2]
    return id_playlist

def eliminar_repetidos(lista_ids : list) -> list:
    '''
    Recibe una lista de ids de canciones con posibles repetidos, y retorna una copia de la lista
    sólo con elementos únicos
    '''
    nueva_lista = list(OrderedDict.fromkeys(lista_ids))
    return nueva_lista