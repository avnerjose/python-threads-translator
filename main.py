import socket
import threading
from googletrans import Translator, constants


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    port = 3000

    s.connect((host, port))
    print("-------Tradutor executando------")
    print('--------------------------------')
    while True:
        msg = input("")
        s.sendto(msg.encode("utf-8"), (host, port))
        if msg == "SAIR":
            break
    s.close()


def server(lang):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    port = 3000
    translator = Translator()
    language_in_portuguese = translator.translate(
        constants.LANGUAGES[lang], dest="pt")

    s.bind((host, port))

    while True:
        x = s.recvfrom(1024)
        msg = str(x[0].decode("utf-8"))
        translation = translator.translate(msg, dest=str(lang))
        if msg == "SAIR":
            break
        msg = f'Texto em {language_in_portuguese.text}: {translation.text}'
        print()
        print(msg)
        print('--------------------------------')
    s.close()


if __name__ == "__main__":

    translator = Translator()
    selected_lang = ''

    print("------Tradutor simultâneo-------")
    print("Digite 'SAIR' para encerrar")
    print()
    
    while True:
        text_to_detect = input(
            "Digite uma frase no idioma para o qual quer traduzir: ")
        detect = translator.detect(text_to_detect)
        try:
            language_in_portuguese = translator.translate(
                constants.LANGUAGES[detect.lang], dest="pt")
            print(f'Língua detectada: {language_in_portuguese.text}')
            proceed = input("Deseja prosseguir com essa lingua? [y/n]")
        except:
            print("Língua não detectada, digite novamente.")
            continue
        if proceed == "y":
            selected_lang = detect.lang
            break

    t1 = threading.Thread(target=server, args=(selected_lang,))
    t2 = threading.Thread(target=client)

    t1.start()
    t2.start()
