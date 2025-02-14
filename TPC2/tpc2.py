import fileinput
import locale

locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')

class Obra:
    def __init__(self, nome, desc, anoCriacao, periodo, compositor, duracao, _id):
        self.nome = nome
        self.desc = desc
        self.anoCriacao = anoCriacao
        self.periodo = periodo
        self.compositor = compositor
        self.duracao = duracao
        self._id = _id


def parse_obra(campos):
    return Obra(*campos)


def read_obras_csv(file):
    obras = []
    buffer = ""

    next(file)

    for line in file:
        line = line.strip()
        if not line:
            continue

        buffer += line + " "
        campos = split_campos(buffer.strip())

        if len(campos) == 7:
            obras.append(parse_obra(campos))
            buffer = ""

    return obras


def split_campos(linha):
    campos = []
    campo = ""
    inside_quotes = False

    for char in linha:
        if char == '"':
            inside_quotes = not inside_quotes
        elif char == ';' and not inside_quotes:
            campos.append(campo.strip())
            campo = ""
        else:
            campo += char

    campos.append(campo.strip())
    return campos


def inverter_nome(compositor):
    if ',' in compositor:
        partes = compositor.split(',')
        return f"{partes[1].strip()} {partes[0].strip()}"
    return compositor


def lista_compositores_ordered_alphabetically(obras):
    compositores = sorted(set(inverter_nome(obra.compositor) for obra in obras), key=locale.strxfrm)
    return compositores


def lista_obras_por_periodo(obras):
    dicionario = {}
    for obra in obras:
        if obra.periodo not in dicionario:
            dicionario[obra.periodo] = []
        dicionario[obra.periodo].append(obra)
    
    for periodo in dicionario:
        dicionario[periodo].sort(key=lambda obra: locale.strxfrm(obra.nome))
    
    return dicionario


def main():
    obras = read_obras_csv(fileinput.input())

    compositores = lista_compositores_ordered_alphabetically(obras)
    print("---------- Compositores -----------\n")
    for compositor in compositores:
        print(compositor)

    print("---------- Número de obras por periodo -----------\n")
    obras_por_periodo = lista_obras_por_periodo(obras)
    for periodo, obras in obras_por_periodo.items():
        print(f"{periodo} :{len(obras)} Obras\n")

    print("---------- Obras por periodo -----------\n")
    for periodo, obras in obras_por_periodo.items():
        print(f"🎵 {periodo}")
        for obra in obras:
            print(f"{obra.nome} ({obra.anoCriacao})")
        print("\n")


if __name__ == "__main__":
    main()