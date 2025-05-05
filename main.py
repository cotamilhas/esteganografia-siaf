import os
from PIL import Image
import colorama
from colorama import Fore, Style
from datetime import datetime
colorama.init(autoreset=True)

def limpar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def listar_imagens():
    imagens = [f for f in os.listdir() if f.lower().endswith('.png')]
    if not imagens:
        print(Fore.RED + "Não há imagens .png nesta pasta.")
        return []
    for i, img in enumerate(imagens):
        print(Fore.CYAN + f"{i+1}. {img}")
    return imagens

def escolher_imagem():
    imagens = listar_imagens()
    if not imagens:
        return None
    while True:
        try:
            escolha = int(input(Fore.YELLOW + "Escolhe o número da imagem: ")) - 1
            if 0 <= escolha < len(imagens):
                return imagens[escolha]
        except ValueError:
            pass
        print(Fore.RED + "Entrada inválida. Tenta outra vez.")

def esconder_texto(imagem_path, mensagem, output_path):
    img = Image.open(imagem_path)
    bin_msg = ''.join(format(ord(c), '08b') for c in mensagem + '\0')
    pixels = img.getdata()
    novos_pixels = []

    i = 0
    for pixel in pixels:
        r, g, b = pixel
        if i < len(bin_msg): r = (r & ~1) | int(bin_msg[i]); i += 1
        if i < len(bin_msg): g = (g & ~1) | int(bin_msg[i]); i += 1
        if i < len(bin_msg): b = (b & ~1) | int(bin_msg[i]); i += 1
        novos_pixels.append((r, g, b))

    img.putdata(novos_pixels)
    img.save(output_path)
    limpar_consola()
    print(Fore.GREEN + f"Mensagem escondida em '{output_path}'.")

def revelar_texto(imagem_path):
    img = Image.open(imagem_path)
    bits = ''
    for pixel in img.getdata():
        for valor in pixel[:3]:
            bits += str(valor & 1)

    msg = ''
    for i in range(0, len(bits), 8):
        char = chr(int(bits[i:i+8], 2))
        if char == '\0':
            break
        msg += char

    limpar_consola()
    print(Fore.GREEN + "Mensagem escondida: " + Fore.YELLOW + msg)

# Menu principal
def main():
    while True:
        print(Fore.GREEN + "\n===== MENU =====")
        print("1. Esconder mensagem (encriptar)")
        print("2. Revelar mensagem (desencriptar)")
        print("0. Sair")

        opcao = input(Fore.YELLOW + "Escolhe uma opção: ")

        if opcao == '1':
            limpar_consola()
            imagem = escolher_imagem()
            if imagem:
                while True:
                    mensagem = input(Fore.YELLOW + "Escreve a mensagem a esconder: ").strip()
                    if mensagem:
                        break
                    limpar_consola()
                    print(Fore.RED + "A mensagem não pode estar vazia. Tenta novamente.")

                
                nome_saida = input(Fore.YELLOW + "Nome do ficheiro de saída (.png): ").strip()
                if not nome_saida:
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    nome_saida = f"saida_{timestamp}.png"
                elif not nome_saida.lower().endswith('.png'):
                    nome_saida += '.png'
                esconder_texto(imagem, mensagem, nome_saida)
        elif opcao == '2':
            limpar_consola()
            imagem = escolher_imagem()
            if imagem:
                revelar_texto(imagem)
        elif opcao == '0':
            print(Fore.GREEN + "Até à próxima!")
            break
        else:
            print(Fore.RED + "Opção inválida. Tenta novamente.")

if __name__ == '__main__':
    main()
