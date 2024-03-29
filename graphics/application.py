from utilities import (
    InstructionMemory, 
    decode_assembly, 
    reverse_sign_op,
    ProgramCounter, 
    Accumulator, 
    Compiler, 
    RAM
)
from graphics import (
    _ControllFrame, 
    _InputFrame, 
    _InfoFrame, 
    _RamFrame
)
from constants import (
    INPUT_TXT_PATH,
    SHEET_PATH, 
    menomic 
)
from    tkinter  import ttk
import  tkinter  as tk
from    PIL      import Image, ImageTk

class Application(tk.Tk) :

    def __init__(self, *args, **kwargs) :
        """
        It creates a window with a title, a background color, a style, a container, and a bunch of
        frames
        """
        super().__init__(*args, **kwargs)

        self.title("Memory Management Project - Computer Architecture - Ahmet Y. | Kerem K. | Musatafa Mer T. | Emir Çetin M.")

        self.configure(background="gray")

        self.style = ttk.Style(self)

        self.style.theme_use("clam")
        self.style.configure("TFrame", background="light gray", borderwidth=1, relief="relief", padding=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        cPad = 10
        self.container = ttk.Frame(self, padding=(cPad))
        self.container.grid(row=0, column=0, padx=cPad, pady=cPad)

        self.controllerSection = _ControllFrame(self.container, self)
        self.controllerSection.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.infoSection = _InfoFrame(self.container, self)
        self.infoSection.grid(row=0, column=0, sticky="nsew")

        self.inputSection = _InputFrame(self.container, self)
        self.inputSection.grid(row=1, column=0, sticky="nsew")

        self.ramSection = _RamFrame(self.container, self)
        self.ramSection.grid(row=0, column=1, rowspan=2, sticky="nsew")

        for frame in self.container.winfo_children():
            frame.grid_configure(padx=5, pady=5, ipadx=20, ipady=20)
            frame.configure(borderwidth=1, relief='solid')

    def showPhoto(self) :
        """
        It opens a photo and displays it in a label.
        """

        if self.controllerSection.photoButton.cget("text") == "Open Sheet":
            self.controllerSection.photoButton.config(text="Close Sheet")

            scale = 1
            photo = Image.open(SHEET_PATH).resize((505*scale, 308*scale), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(photo)
            self.label = ttk.Label(self.container, image=photo)
            self.label.image = photo
            self.label.grid(row=0, column=3, rowspan=3, sticky="nsew")
            # put background to label
            self.label.configure(background="light gray")
        else :
            self.controllerSection.photoButton.config(text="Open Sheet")
            self.label.grid_forget()

    def loadMachine(self) :
        """
        It loads the machine with the instructions from the input file
        """
        try :
            self.instructions = decode_assembly(INPUT_TXT_PATH)
            self.number_of_instructions = len(self.instructions)
        except :
            raise (f"Given assembly code is not valid. Or {INPUT_TXT_PATH} does not exist !")
            
        self.ram = RAM()
        self.acc = Accumulator()
        self.pc = ProgramCounter()
        self.im = InstructionMemory(self.instructions)

    def runCompiler(self) :
        """
        It takes the input from the user, compiles it, and then updates the GUI with the results
        """

        if (self.inputSection.inputArea.get("1.0", tk.END).rstrip() == "") :
            self.controllerSection.nextButton.config(state="disabled", text="End")

        instruction, value, lineNo, acc = Compiler.compile_instruction(self.acc, self.ram, self.pc, self.im)
        instructionValue = reverse_sign_op(value)
        accValue = reverse_sign_op(acc)

        self.infoSection.updateInfoScreen(str(lineNo), str(str(menomic[instruction])+" "+str(instructionValue)), str(str(value[0])+" "+str(value[1:])), str(instructionValue), str(int(instructionValue, 16)), str(acc[0])+" "+str(acc[1:]), str(accValue), str(int(accValue, 16)))

        self.ramSection.updateRamScreen()

        if self.pc.get() >= self.number_of_instructions:
            self.controllerSection.nextButton.config(state="disabled", text="End")
