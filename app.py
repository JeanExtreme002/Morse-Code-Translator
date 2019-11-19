
from translator import MorseCodeTranslator
from tkinter import Tk,Label,Text,Frame,Button,Scrollbar,IntVar
import sys

if "win" in sys.platform:
    from winsound import Beep


class App(object):
    """
    Classe principal
    """

    __button_width = 15
    __button_height = 1
    __button_bg = "green2"
    __button_fg = "white"
    __button_font = ("Autumn",27)
    __button_relief = "flat"

    __inputText_height = 5

    __label_fg = "#F5F5F5"
    __label_font = ("Impact",20)

    __outputText_height = 7

    __text_width = 50
    __text_bg = "white"
    __text_fg = "black"
    __text_font = ("Arial",14)

    frequency = 1500

    window_title = "Morse Code Translator"
    window_geometry = [600,500]
    window_bg = "gray50"



    def __init__(self):

        # Cria uma instância de Tk e configura a janela.
        self.__root = Tk()
        self.__root.geometry("{}x{}".format(*self.window_geometry))
        self.__root["bg"] = self.window_bg
        self.__root.title(self.window_title)
        self.__root.resizable(False,False)
        self.__root.focus_force()
        self.__root.bind("<Return>",self.translate)

        self.__playing = False
        self.__waitVar = IntVar()

        # Chama método para construir a interface do programa.
        self.build()



    def build(self):
        """
        Método para construir interface do programa.
        """

        # Cria um título para a entrada do texto que será traduzido.
        Label(
            self.__root,
            bg = self.window_bg,
            font = self.__label_font,
            fg = self.__label_fg,
            text = "Input:",
            pady = 10
            ).pack()


        # Cria frame para colocar o campo de input.
        input_frame = Frame(self.__root,bg=self.window_bg)
        input_frame.pack()

        # Cria um campo para o usuário inserir o texto.
        self.__inputText = Text(
            input_frame,
            width = self.__text_width,
            height = self.__inputText_height,
            bg = self.__text_bg,
            fg= self.__text_fg,
            font = self.__text_font,
            wrap = "word"
            )
        self.__inputText.insert(0.0," Type here...")

        # Cria uma barra de rolagem para o campo de input.
        scrollbar = Scrollbar(input_frame)
        scrollbar.pack(side="right",fill="y")
        self.__inputText.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.__inputText.yview)

        self.__inputText.pack()
        

        # Cria título de campo onde será colocado o texto traduzido.
        Label(
            self.__root,
            bg = self.window_bg,
            font = self.__label_font,
            fg = self.__label_fg,
            text = "Output:",
            pady = 10
            ).pack()


        # Cria frame para colocar o campo de output.
        output_frame = Frame(self.__root,bg=self.window_bg)
        output_frame.pack()


        # Campo para colocar o texto traduzido.
        self.__outputText = Text(
            output_frame,
            width = self.__text_width,
            height = self.__outputText_height,
            bg = self.__text_bg,
            fg= self.__text_fg,
            font = self.__text_font,
            wrap = "word"
            )
        self.__outputText.insert(0.0," The text translation will appear here.")


        # Cria uma barra de rolagem para o campo de output.
        scrollbar = Scrollbar(output_frame)
        scrollbar.pack(side="right",fill="y")
        self.__outputText.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.__outputText.yview)

        self.__outputText.pack()

        
        # Cria frame para inserir os botões.
        buttons_frame = Frame(self.__root,bg=self.window_bg,pady=20)
        buttons_frame.pack()

        # Cria uma "borda" para o botão.
        button1_frame = Frame(buttons_frame,bg="black",padx=2,pady=2)
        button1_frame.pack(side="left")

        # Cria botão para traduzir o texto.
        self.__button1 = Button(
            button1_frame,
            width = self.__button_width,
            height = self.__button_height,
            relief = self.__button_relief,
            bg = self.__button_bg,
            fg = self.__button_fg,
            font = self.__button_font,
            text = "Translate",
            command = self.translate
        )
        self.__button1.pack()



        # Se o OS do usuário for Windows, será criado um botão
        # para reproduzir o som do codigo morse.
        if "win" in sys.platform:

            Label(buttons_frame,bg=self.window_bg,padx=5).pack(side="left")

            # Cria uma "borda" para o botão.
            button2_frame = Frame(buttons_frame,bg="black",padx=2,pady=2)
            button2_frame.pack(side="left")

            # Cria botão para reproduzir som do código morse.
            self.__button2 = Button(
                button2_frame,
                width = self.__button_width,
                height = self.__button_height,
                relief = self.__button_relief,
                bg = self.__button_bg,
                fg = self.__button_fg,
                font = self.__button_font,
                text = "Play",
                command = self.play
            )
            self.__button2.pack()

        self.__root.mainloop()



    def play(self):
        """
        Método para reproduzir o som do código morse.
        """

        # Para a reprodução.
        if self.__playing:
            self.__playing = False
            return

        # Obtém o texto do output e verifica se é um código morse.
        text = self.__outputText.get(0.0,"end")
        if not text or text.isspace() or not MorseCodeTranslator.isMorse(text): return

        # Informa que o som do código morse está sendo reproduzido.
        self.__playing = True
        self.__button2.config(text = "Stop")


        # Divide texto em palavras.
        for char in text.split(" "):

            # Obtém cada letra da palavra.
            for l in char:

                if not self.__playing:
                    break
                
                # Verifica se o caractere é de erro.
                if l == MorseCodeTranslator.errorChar:
                    continue

                # Toca um beep por 0,3 segundos cado seja um ponto.
                if l == ".":
                    Beep(self.frequency,300)

                # Toca um beep por 0.6 segundos caso seja um traço.
                elif l == "-":
                    Beep(self.frequency,600)

                # Dorme por 2.1 segundos caso seja o início de uma nova palavra.
                elif l == "/":
                    self.wait(2100)
            
            
            if not self.__playing:
                break

            # Aguarda 0.9 segundos.
            self.wait(900)


        # Informa que a reprodução acabou.
        self.__playing = False
        self.__button2.config(text = "Play")



    def translate(self,event=None):
        """
        Método do botão para traduzir o texto.
        """


        # Obtém o input do usuário.
        text = self.__inputText.get(0.0,"end")
        if not text: return

        # Apaga o texto do campo de output e insere o input do usuário traduzido.
        self.__outputText.delete(0.0,"end")
        self.__outputText.insert(0.0,MorseCodeTranslator.translate(text))



    def wait(self,ms):
        """
        Método para aguardar um tempo em Ms.
        """

        self.__waitVar.set(0)
        self.__root.after(ms,self.__waitVar.set,1)
        self.__root.wait_variable(self.__waitVar)
        self.__waitVar.set(0)



if __name__ == "__main__":
    App()

    
