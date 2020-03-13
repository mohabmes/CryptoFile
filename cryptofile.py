from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from utils import *

class CryptoFile_GUI():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x600")
        self.window.resizable(0, 0)
        self.window.title("CryptoFile")
        self.create_widgets()

    def run(self):
        self.window.mainloop()

    def create_widgets(self):
        paths_lbl = ttk.LabelFrame(self.window, text="Paths")
        paths_lbl.grid(row=1,padx=5, pady=5)

        listPathVars = tk.Variable()
        files_lb = tk.Listbox(paths_lbl, height=5, listvariable=listPathVars, exportselection=False)
        files_lb.grid(row=1, columnspan=3, column=0, sticky='WE', \
                     padx=5, pady=5, ipadx=155)

        addFile_btn = tk.Button(paths_lbl, text="Add File(s) ", command=lambda: selectFiles())\
            .grid(row=2, column=0, ipadx=5)

        addDir_btn = tk.Button(paths_lbl, text="Add Directory", command=lambda: selectDirectory()).\
            grid(row=2, column=1, ipadx=5)

        rmFile_btn = tk.Button(paths_lbl, text=" Remove Item ", command=lambda: deleteSelectedItem())
        rmFile_btn.grid(row=2, column=2, padx=5, pady=2)

        # --------------------------------------------------------
        options_lbl = ttk.LabelFrame(self.window, text="Options")
        options_lbl.grid(row=2, column=0, sticky='WE', \
                       padx=5, pady=5)

        delFileOption = ttk.Checkbutton(options_lbl, text="Delete original file(s).")
        delFileOption.grid(row=1, column=2,padx=5, pady=2)

        compressFileOption = ttk.Checkbutton(options_lbl, text="Compress the file(s). ")
        compressFileOption.grid(row=2, column=2,padx=5, pady=2)

        # --------------------------------------------------------
        pswd_lbl = ttk.LabelFrame(self.window, text="Password")
        pswd_lbl.grid(row=3, sticky='WE', padx=5, pady=5)

        password = ttk.Entry(pswd_lbl, show="*", justify='center')
        password.grid(row=1, column=1, sticky='WE',\
                      ipadx=155, ipady=5, padx=5, pady=5)

        menu_label = ttk.Label(pswd_lbl, text="Must be at least 16 characters!")
        menu_label.grid(row=2, column=1, padx=5, pady=5)

        # --------------------------------------------------------
        oper_lbl = ttk.LabelFrame(self.window, text="Operation")
        oper_lbl.grid(row=4, sticky='WE', padx=5, pady=5)

        encrypt = tk.Button(oper_lbl, text="Encrypt", command=lambda: prepareEncrypt()).\
            grid(row=2, column=0, padx=5, pady=5, ipadx=78)
        decrypt = tk.Button(oper_lbl, text="Decrypt", command=lambda: prepareDecrypt()).\
            grid(row=2, column=1, padx=5, pady=5, ipadx=78)

        # --------------------------------------------------------
        log_lbl = ttk.LabelFrame(self.window, text="Log")
        log_lbl.grid(row=5, sticky='WE', padx=5, pady=5)

        logger = tk.Text(log_lbl, height=5, width=30)
        logger.grid(row=1, column=0, ipadx=115, ipady=12, padx=5, pady=5)

        # --------------------------------------------------------
        foot_lbl = ttk.Label(self.window, text="Made by: Mohab Elsheikh (@mohabmes)")
        foot_lbl.config(font=("arial", 8))
        foot_lbl.grid()

        def selectFiles():
            filename = askopenfilename()
            appendToPathsList(filename)

        def selectDirectory():
            dirname = askdirectory()
            if len(dirname):
                filesname = scan_directory(dirname)
                for file in filesname:
                    appendToPathsList(file)

        def appendToPathsList(x):
            files_lb.insert(0, x)

        def getAllSelectedFile():
            all = listPathVars.get()
            return list(all)

        def deleteSelectedItem():
            selectedIndex = files_lb.curselection()
            files_lb.delete(selectedIndex)

        def getPassword():
            passtxt = str(password.get())
            if passtxt is None:
                return None
            else:
                return passtxt

        def prepareEncrypt():
            filespath = getAllSelectedFile()
            password = getPassword()

            if filespath is not None and len(filespath)==0:
                log('No File(s) added')
            elif password is None:
                log('Password field is empty')
            elif len(password) < 16:
                log("Password is too short")
            else:
                log('Start Encrypting ...')
                startEncrypt(filespath, password)

        def startEncrypt(listOfFiles, password):
            for file in listOfFiles:
                res_fl = encrypt_file(file, password)
                if res_fl is not None:
                    log(res_fl)
            log('Done')

        def prepareDecrypt():
            filespath = getAllSelectedFile()
            password = getPassword()

            if filespath is not None and len(filespath)==0:
                log('No File(s) added')
            elif password is None:
                log('Password field is empty')
            elif len(password) < 16:
                log("Password is too short")
            else:
                log('Start Decrypting ...')
                startDecrypt(filespath, password)

        def startDecrypt(listOfFiles, password):
            for file in listOfFiles:
                if '.enc' in file:
                    res_lg = decrypt_file(file, password)
                    if res_lg is not None:
                        log(res_lg)
                else:
                    log('Unknown file format : {}'.format(file))
            log('Done')

        def log(message):
            log_data = timestamp() + message + '\n'
            logger.insert('1.0', log_data)
        log('Ready')



def encrypt(plaintext, key, iv_sz=16):
    iv = get_random_bytes(iv_sz)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    try:
        return iv + cipher.encrypt(plaintext)
    except:
        return "Unable to encrypt"


def decrypt(ciphertext, key, iv_sz=16):
    iv = ciphertext[:iv_sz]
    cipher = AES.new(key, AES.MODE_CFB, iv)

    try:
        plaintext = cipher.decrypt(ciphertext[iv_sz:])
    except:
        return "Unable to decrypt"

    return plaintext.decode('utf-8', 'ignore')


def encrypt_file(file_name, key, del_plain=False):
    # read the plaintext file content
    try:
        with open(file_name, 'rb') as file:
            plaintext = file.read()
            ciphertext = encrypt(plaintext, key)
    except IOError:
        return "Could not read file:", file_name

    # create the new encrypted file
    try:
        with open(file_name + ".enc", 'wb') as nfile:
            nfile.write(ciphertext)
    except IOError:
        return "Could not create: ", nfile

    # delete the original plaintext file
    if del_plain:
        removeFile(file_name)


def decrypt_file(file_name, key, del_cipher=False):
    # read the encrypted file content
    try:
        with open(file_name, 'rb') as file:
            ciphertext = file.read()
        plaintext = decrypt(ciphertext, key)
    except IOError:
        return "Could not read file: ", file_name

    # create the plaintext file content
    try:
        with open(file_name[:-4], 'w') as nfile:
            nfile.write(plaintext)
    except IOError:
        return "Could not create: ", file_name

    # delete the encrypted file
    if del_cipher:
        removeFile(file_name)


if __name__ == '__main__':
    CryptoFile_GUI().run()
