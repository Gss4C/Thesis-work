def read_and_list(path_to_txtfile): 
    '''
    Input to a txt file containing a column and output a strings list \n
    Python3 necessary
    '''
    lista_file = []
    with open(path_to_txtfile, "r") as file:
        for riga in file:
            riga = riga.strip()  # Rimuovi eventuali spazi o caratteri di newline alla fine della riga
            lista_file.append(riga)
    return lista_file