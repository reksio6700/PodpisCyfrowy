from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
import PySimpleGUI as sg



sg.theme('DarkAmber')

layout = [
            [sg.Text('Wpisz nazwe pliku'), sg.InputText()],
            [sg.Button('Wygeneruj klucz'), sg.Button('Sprawdz poprawność')]]

window = sg.Window('Podpis Cyfrowy', layout)
while True:


    event, plik = window.read()
    if event == sg.WIN_CLOSED:
        break
    text_input = plik[0]
    file = open(text_input, 'rb')


    hash = SHA256.new(file.read())
    if  event == 'Wygeneruj klucz':
        key = RSA.generate(1024)

        sign = PKCS1_v1_5.new(key).sign(hash)

        with open("PodpisCyfrowy.txt", 'wb') as f:
            f.write(b64encode(sign))

        public_key = key.publickey()
        with open("KluczPubliczny.p12", 'wb') as f:
            f.write(public_key.export_key())
        sg.popup('Podpis Cyfrowy oraz Klucz publiczny wygenerowane!')
        break
    if event == 'Sprawdz poprawność':
        key = RSA.importKey(open('KluczPubliczny.p12').read())
        sign_dec = b64decode(open('PodpisCyfrowy.txt', 'r').read())
        verifier = PKCS1_v1_5.new(key)
        if verifier.verify(hash, sign_dec):
            sg.popup('Podpis Cyfrowy prawidłowy!')
        else:
            sg.popup('Podpis Cyfrowy nieprawidłowy!')
        break


window.close()

