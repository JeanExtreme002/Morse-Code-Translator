
class MorseCodeTranslator(object):
    """
    Classe para realizar traduções de código morse.
    """

    __morse_code = {
        'A':'.-',
        'B':'-...',
        'C':'-.-.',
        'D':'-..',
        'E':'.',
        'F':'..-.',
        'G':'--.',
        'H':'....',
        'I':'..',
        'J':'.---',
        'K':'-.-',
        'L':'.-..',
        'M':'--',
        'N':'-.',
        'O':'---',
        'P':'.--.',
        'Q':'--.-',
        'R':'.-.',
        'S':'...',
        'T':'-',
        'U':'..-',
        'V':'...-',
        'W':'.--',
        'X':'-..-',
        'Y':'-.--',
        'Z':'--..',

        '1':'.----',
        '2':'..---',
        '3':'...--',
        '4':'....-',
        '5':'.....',
        '6':'-....',
        '7':'--...',
        '8':'---..',
        '9':'----.',
        '0':'-----',

        '.':'.-.-.-',
        ',':'--..--',
        '?':'..--..',
        '‘':'.----.',
        '!':'.-.--',
        '/':'-..-.',
        '(':'-.--.',
        ')':'-.--.-',
        '&':'.-...',
        ':':'---...',
        ';':'-.-.-.',
        '=':'-...-',
        '-':'-....-',
        '_':'..--.-',
        '"':'.-..-.',
        '$':'...-..-',
        '@':'.--.-.',
    }

    errorChar = "�"


    @staticmethod
    def getMorseCodeTable():
        """
        Método para obter um dicionário com os caracteres 
        e seus respectivos códigos morse.
        """
        return MorseCodeTranslator.__morse_code


    @staticmethod
    def isMorse(text):
        """
        Método para verificar se o texto está em código morse ou não.
        """
        return all( 
            map( lambda char: False if not char in [".","-"," ","/","\n",MorseCodeTranslator.errorChar] else True , text) 
        )


    @staticmethod
    def translate(text):
        """
        Método para traduzir o texto.
        """

        new_text = ""

        # Verifica se o texto é um código morse.

        if MorseCodeTranslator.isMorse(text):


            # Divide as letras codificadas do texto.
            text = text.split(" ")
            

            for char in text:

                # Caso o caractere seja uma barra, ele será substituído por espaçamento.

                if char == "/":
                    new_text += " "
                    continue
                # Verifica se é possível converter o caractere.
                if char == MorseCodeTranslator.errorChar:
                    if "\n" in char:
                        new_text += "\n"
                    continue
                

                for (key,value) in MorseCodeTranslator.__morse_code.items():
                    

                    # Verifica se existe uma quebra de linha junto do caractere.
                    # Se sim, sua posição será obtida.

                    if "\n" in char:
                        nextLine_i = char.index("\n")
                    else:
                        nextLine_i = -1

                    # Transforma o código morse para caractere ASCII.

                    if char.replace("\n","") == value:


                        # Adiciona caractere ao novo texto.

                        if nextLine_i != -1:

                            # Verifica se a quebra de linha vem antes ou depois do caractere.
                            if nextLine_i == 0:
                                new_text += "\n" + key
                            else:
                                new_text += key + "\n"
                        else:
                            new_text += key
        

        # Codifica o texto para código morse.
        else:
            for char in text.upper():
                
                # Verifica se o caractere é uma quebra de linha.
                if char == "\n":
                    new_text += "\n"
                    continue
                
                # Caso o caractere seja um espaçamento, ele será substituído por uma barra.
                elif char.isspace():
                    new_text += "/ "
                    continue
                
                # Tenta converter o caractere para código morse.
                try:  
                    new_text += MorseCodeTranslator.__morse_code[char] + " "
                except KeyError:
                    new_text += MorseCodeTranslator.errorChar + " "

            # Retira espaço do início.
            if new_text.endswith("/"):
                new_text = new_text[:-2]

        # Retorna o novo texto.
        return new_text.strip().capitalize()
