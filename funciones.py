def id_playlist(enlace_playlist : str) -> str:
    '''
    Retorna el id de una playlist dado su enlace
    '''
    pos1 = enlace_playlist.find('playlist/') + len('playlist/')
    pos2 = enlace_playlist.find('?')
    id_playlist = enlace_playlist[pos1 : pos2]
    return id_playlist