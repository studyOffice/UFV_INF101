# Programador: Gabriel Pereira de Calais
# Matrícula: 93506
# Criado em: 20/04/2021
# Atualizado em: 20/04/2021
# Gerencia um arquivo de senhas contendo, em cada linha, o par separado
# por tab: <login_name><tab><hashed_password>. Para melhorar a performance,
# usa-se um dicionário para armazenar os pares (login_name, hashed_password)
# na memória primária.

import uuid
import hashlib
import sys

arqnome = 'passwords.hash'  # nome externo default do arquivo de senhas
# Verifica se o nome do arquivo foi passado como parâmetro na linha comando.
if len(sys.argv) > 1:
    arqnome = sys.argv[1]


def main():
    print('Início do processamento do arquivo de senhas \'{}\'.'.
          format(arqnome))
    # Gera o dicionário a partir do arquivo cujo nome é arqnome.
    senhas_cripto = gere_dicionario(arqnome)
    login_name = input('\nLogin name: ')
    while len(login_name) > 0:
        senha = input('Password: ')
        encSenha = pesquise(senhas_cripto, login_name)
        if encSenha != '\0':
            print('O usuário \'{}\' '.format(login_name), end='')
            if not autenticado(senha, encSenha):
                print('NÃO ', end='')
            print('foi autenticado pelo sistema.')
        else:
            print('O usuário \'{}\' não existe. Está sendo criado...'.
                  format(login_name))
            insira(senhas_cripto, login_name, senha)
        login_name = input('\nLogin name: ')
    # Armazena o dicionário de volta no arquivo de nome arqnome.
    armazene(senhas_cripto, arqnome)
    print('\nFim do processamento do arquivo de senhas.')


# Calcula o hash de senha, usando o conjunto de funções de hash criptográficas
# SHA-2, com 256 bits. Para maiores informações, consulte:
# https://pt.wikipedia.org/wiki/SHA-2
def hash_password(senha):
    # salt é um número aleatório inserido no início do hash para dificultar
    # a quebra do código por algum hacker malicioso.
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + senha.encode()).hexdigest() + ':'         + salt  # concatena-se a pedra de sal ao final para saber depois qual é


# Verifica se a senha em texto claro bate com a senha original criptografada.
def autenticado(clear, hashed):
    decSenha, salt = hashed.split(':')  # separa a senha criptografada e a
                                        # pedra de sal
    return decSenha == hashlib.sha256(salt.encode() +                        clear.encode()).hexdigest()


# Gera um dicionário a partir dos dados lidos do arquivo cujo nome está
# no parâmetro arqnome. Retorna o dicionário gerado.
###                                                                  ###
# COLOQUE AQUI A SUA IMPLEMENTAÇÃO DA FUNÇÃO gere_dicionario(arqnome). #
###                                                                  ###

def gere_dicionario(arqnome):
    try:
        arq = open(arqnome, 'r')
        dicionario = {}
        linha = arq.readline().rstrip('\n')
        while linha != '' :
            senhas = linha.split('\t')
            v0 = senhas[0]
            v1 = senhas[1]
            dicionario[v0] = v1
            linha = arq.readline().rstrip('\n')
        arq.close()
        return dicionario
    except OSError:
        print("O arquivo de senhas 'passwords.hash' não existe. Está sendo criado...")
        arq = open(arqnome, 'w')
        arq.close()
        return {}

# Salva o dicionário dicSenhas em um arquivo cujo nome está no parâmetro
# arqnome. Não retorna nada.
###                                                                      ###
# COLOQUE AQUI A SUA IMPLEMENTAÇÃO DA FUNÇÃO armazene(dicSenhas, arqnome). #
###                                                                      ###

def armazene(dicSenhas, arqnome):
    try:
        arq = open(arqnome, 'w')
        for key in dicSenhas.keys():
            arq.writelines(key+'\t'+dicSenhas[key]+'\n')
        arq.close()
    except OSError:
        print('Erro ao criar o arquivo de senhas!')

# A função pesquise retorna a senha codificada associada a nome.
# Se nome não for encontrado no dicionário dicSenhas, ela retorna
# o caractere nulo.
###                                                                   ###
# COLOQUE AQUI A SUA IMPLEMENTAÇÃO DA FUNÇÃO pesquise(dicSenhas, nome). #
###                                                                   ###

def pesquise(dicSenhas, nome):
    if nome in dicSenhas.keys():
        return dicSenhas[nome]
    else:
        return '\0'

# Insere, no dicionário dicSenhas, o par (login, senha codificada).
###                                                                         ###
# COLOQUE AQUI A SUA IMPLEMENTAÇÃO DA FUNÇÃO insira(dicSenhas, login, senha). #
###                                                                         ###

def insira(dicSenhas, login, senha):
    cripto = hash_password(senha)
    dicSenhas[login] = cripto


if __name__ == '__main__':
    main()
