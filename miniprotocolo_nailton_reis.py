"""
ALUNO: Nailton Reis
TURMA: Tecnologia em Sistemas para Internet — Redes de Computadores II
DATA: 27/10/2026
PROTOCOLO ESCOLHIDO: TCP

REGISTRO DAS ALTERAÇÕES

ALTERAÇÃO 01
O que foi implementado: comando MINUSCULA.
Entrada testada: MINUSCULA|REDES DE COMPUTADORES
Saída obtida: RESPOSTA|redes de computadores

ALTERAÇÃO 02
O que foi implementado: comando INVERTER.
Entrada testada: INVERTER|socket
Saída obtida: RESPOSTA|tekcos

ALTERAÇÃO 03
O que foi implementado: comando PALAVRAS.
Entrada testada: PALAVRAS|redes de computadores
Saída obtida: RESPOSTA|O texto possui 3 palavras

ALTERAÇÃO 04
O que foi implementado: comando SOMA.
Entrada testada: SOMA|10,5
Saída obtida: RESPOSTA|15

ALTERAÇÃO 05
O que foi implementado: comando PING.
Entrada testada: PING|
Saída obtida: PONG|Servidor ativo

ALTERAÇÃO 06
O que foi implementado: comando AJUDA e menu de comandos atualizado.
Entrada testada: AJUDA|
Saída obtida: RESPOSTA|ECO, MAIUSCULA, MINUSCULA, INVERTER, TAMANHO, PALAVRAS, SOMA, HORA, PING, AJUDA, SAIR
"""

"""
DEMONSTRAÇÃO: TCP E UDP COM UM MINIPROTOCOLO

Este único arquivo pode funcionar como:
1. Servidor TCP
2. Cliente TCP
3. Servidor UDP
4. Cliente UDP

Para testar entre dois computadores:
- os dois computadores devem estar na mesma rede;
- execute o servidor em um computador;
- execute o cliente no outro computador;
- no cliente, informe o endereço IP do servidor.

Formato das mensagens do nosso miniprotocolo:

    COMANDO|CONTEÚDO

Exemplos:

    ECO|Olá
    MAIUSCULA|redes de computadores
    TAMANHO|quantos caracteres existem aqui?
    HORA|
    SAIR|

O objetivo não é criar um sistema profissional. O objetivo é observar, com
um código pequeno, as diferenças entre TCP e UDP.
"""

import socket
from datetime import datetime


# O servidor TCP usará a porta 9000.
PORTA_TCP = 9000

# O servidor UDP usará a porta 9001.
PORTA_UDP = 9001

# 0.0.0.0 permite que o servidor receba comunicações pelas interfaces de rede
# disponíveis no computador.
HOST_SERVIDOR = "127.0.0.1"


# ALTERAÇÃO 04 — converte o texto para inteiro ou, se não for possível, para decimal
def converter_numero(texto):
    try:
        return int(texto)
    except ValueError:
        return float(texto)


def processar_mensagem(mensagem):
    """Interpreta uma mensagem do nosso miniprotocolo."""

    # Toda mensagem precisa possuir o separador |.
    if "|" not in mensagem:
        return "ERRO|Use o formato COMANDO|CONTEUDO"

    # split("|", 1) separa apenas no primeiro caractere |.
    comando, conteudo = mensagem.split("|", 1)

    # Convertemos o comando para maiúsculo para aceitar eco, Eco ou ECO.
    comando = comando.upper()

    # Regra simples de alerta que será mostrada somente no servidor.
    if len(conteudo) > 100:
        print("[ALERTA] O conteúdo possui mais de 100 caracteres.")

    if comando == "ECO":
        return "RESPOSTA|" + conteudo

    if comando == "MAIUSCULA":
        return "RESPOSTA|" + conteudo.upper()

    # ALTERAÇÃO 01 — comando MINUSCULA
    if comando == "MINUSCULA":
        return "RESPOSTA|" + conteudo.lower()

    # ALTERAÇÃO 02 — comando INVERTER
    if comando == "INVERTER":
        return "RESPOSTA|" + conteudo[::-1]

    if comando == "TAMANHO":
        quantidade = len(conteudo)
        return "RESPOSTA|O texto possui " + str(quantidade) + " caracteres"

    # ALTERAÇÃO 03 — comando PALAVRAS
    if comando == "PALAVRAS":
        return "RESPOSTA|O texto possui " + str(len(conteudo.split())) + " palavras"

    # ALTERAÇÃO 04 — comando SOMA
    if comando == "SOMA":
        try:
            primeiro, segundo = conteudo.split(",")
            resultado = converter_numero(primeiro) + converter_numero(segundo)
        except ValueError:
            return "ERRO|Informe dois números separados por vírgula"

        return "RESPOSTA|" + str(resultado)

    if comando == "HORA":
        horario = datetime.now().strftime("%H:%M:%S")
        return "RESPOSTA|Agora são " + horario

    # ALTERAÇÃO 05 — comando PING
    if comando == "PING":
        return "PONG|Servidor ativo"

    # ALTERAÇÃO 06 — comando AJUDA
    if comando == "AJUDA":
        return "RESPOSTA|ECO, MAIUSCULA, MINUSCULA, INVERTER, TAMANHO, PALAVRAS, SOMA, HORA, PING, AJUDA, SAIR"

    if comando == "SAIR":
        return "FIM|Conversa encerrada"

    # Se nenhum comando conhecido foi encontrado, retornamos um erro.
    print("[ALERTA] Comando desconhecido:", comando)
    return "ERRO|Comando desconhecido"


def enviar_tcp(conexao, mensagem):
    """Envia uma mensagem TCP terminada por uma quebra de linha."""

    # O \n funciona como delimitador, indicando o final da mensagem.
    texto_com_delimitador = mensagem + "\n"

    # A rede transporta bytes. Por isso, convertemos o texto para UTF-8.
    dados = texto_com_delimitador.encode("utf-8")

    # sendall() solicita o envio de todos os bytes.
    conexao.sendall(dados)


def receber_tcp(conexao):
    """Recebe bytes até encontrar o delimitador de final de mensagem."""

    dados = b""

    while True:
        # Receber um byte por vez é simples para fins didáticos.
        # Uma aplicação real normalmente usaria um buffer mais eficiente.
        byte = conexao.recv(1)

        # recv() retorna b"" quando o outro lado encerra a conexão.
        if not byte:
            return None

        # Ao encontrar \n, a mensagem está completa.
        if byte == b"\n":
            break

        dados += byte

    # Convertemos os bytes recebidos novamente para texto.
    return dados.decode("utf-8")


def executar_servidor_tcp():
    """Executa um servidor TCP que atende um cliente por vez."""

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar a porta logo após encerrar e executar novamente.
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST_SERVIDOR, PORTA_TCP))
    servidor.listen()

    print(f"Servidor TCP esperando em {HOST_SERVIDOR}:{PORTA_TCP}")

    # accept() aguarda a conexão de um cliente TCP.
    conexao, endereco_cliente = servidor.accept()

    print("Cliente conectado:", endereco_cliente)

    while True:
        mensagem = receber_tcp(conexao)

        if mensagem is None:
            print("O cliente desconectou.")
            break

        print("Recebido por TCP:", mensagem)

        resposta = processar_mensagem(mensagem)
        enviar_tcp(conexao, resposta)

        print("Enviado por TCP:", resposta)

        if mensagem.upper().startswith("SAIR|"):
            break

    conexao.close()
    servidor.close()

    print("Servidor TCP encerrado.")


def executar_cliente_tcp():
    """Executa o cliente TCP."""

    ip_servidor = input("IP do servidor TCP: ")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # O TCP estabelece uma conexão antes de trocar dados.
    cliente.connect((ip_servidor, PORTA_TCP))

    print("Conectado ao servidor TCP.")
    mostrar_comandos()

    while True:
        mensagem = input("Mensagem: ")

        enviar_tcp(cliente, mensagem)

        resposta = receber_tcp(cliente)

        if resposta is None:
            print("O servidor encerrou a conexão.")
            break

        print("Servidor:", resposta)

        if mensagem.upper().startswith("SAIR|"):
            break

    cliente.close()

    print("Cliente TCP encerrado.")


def executar_servidor_udp():
    """Executa um servidor UDP que recebe e responde datagramas."""

    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST_SERVIDOR, PORTA_UDP))

    print(f"Servidor UDP esperando em {HOST_SERVIDOR}:{PORTA_UDP}")

    while True:
        # recvfrom() devolve um datagrama e o endereço de quem o enviou.
        dados, endereco_cliente = servidor.recvfrom(1024)

        mensagem = dados.decode("utf-8")

        print("Recebido por UDP de", endereco_cliente, ":", mensagem)

        resposta = processar_mensagem(mensagem)

        # No UDP, informamos o destino em cada envio.
        servidor.sendto(resposta.encode("utf-8"), endereco_cliente)

        print("Enviado por UDP:", resposta)

        if mensagem.upper().startswith("SAIR|"):
            break

    servidor.close()

    print("Servidor UDP encerrado.")


def executar_cliente_udp():
    """Executa o cliente UDP."""

    ip_servidor = input("IP do servidor UDP: ")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Cliente UDP pronto.")
    print("Observe que não utilizamos connect() como no exemplo TCP.")
    mostrar_comandos()

    while True:
        mensagem = input("Mensagem: ")

        # sendto() envia um datagrama para o endereço informado.
        cliente.sendto(
            mensagem.encode("utf-8"),
            (ip_servidor, PORTA_UDP),
        )

        # O programa espera o datagrama de resposta.
        dados, endereco_servidor = cliente.recvfrom(1024)

        resposta = dados.decode("utf-8")

        print("Resposta de", endereco_servidor, ":", resposta)

        if mensagem.upper().startswith("SAIR|"):
            break

    cliente.close()

    print("Cliente UDP encerrado.")


def mostrar_comandos():
    """Mostra exemplos das mensagens aceitas pelo servidor."""

    print()
    print("Comandos disponíveis:")
    print("ECO|Olá")
    print("MAIUSCULA|redes de computadores")
    # ALTERAÇÃO 06 — novos comandos no menu
    print("MINUSCULA|REDES DE COMPUTADORES")
    print("INVERTER|socket")
    print("TAMANHO|quantos caracteres existem aqui?")
    print("PALAVRAS|redes de computadores")
    print("SOMA|10,5")
    print("HORA|")
    print("PING|")
    print("AJUDA|")
    print("SAIR|")
    print()


def mostrar_menu():
    """Mostra os quatro modos de execução disponíveis."""

    print("=" * 50)
    print("DEMONSTRAÇÃO DE TCP E UDP")
    print("=" * 50)
    print("1 - Servidor TCP")
    print("2 - Cliente TCP")
    print("3 - Servidor UDP")
    print("4 - Cliente UDP")
    print("=" * 50)


# O bloco abaixo só executa quando abrimos este arquivo diretamente.
if __name__ == "__main__":
    mostrar_menu()

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        executar_servidor_tcp()
    elif opcao == "2":
        executar_cliente_tcp()
    elif opcao == "3":
        executar_servidor_udp()
    elif opcao == "4":
        executar_cliente_udp()
    else:
        print("Opção inválida.")
