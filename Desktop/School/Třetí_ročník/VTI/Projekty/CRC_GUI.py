from tkinter import *
from itertools import product

def check_format(input):
    """Checks if inputs are binary."""
    input =  str(input)
    for i in input:
        if i != "0" and i != "1":
            print("Must by binary !")
            return False
    else: 
        return input

def pol_format(bin):
    """Return binary data in polynomial form."""
    bin=bin[::-1]
    pol_members=[]

    for i in reversed(range(len(bin))):
        if bin[i] != "0":
            pol_members.append(f"x^{i}")

    if "x^1" in pol_members:
            pol_members[pol_members.index("x^1")] = "x"
    if "x^0" in pol_members:
            pol_members[pol_members.index("x^0")] = "1"
    pol = " + ".join(pol_members)
    return pol
        

def poly_mod_div(num,den):
    """Returns the remainder of polynomial division. Binary coefficents only!

    Parameters
    ------------
    num (str): Numerator of division
    den (str): Denominator of division

    """
    result = ""
    num = num.lstrip("0"); den = den.lstrip("0")

    while len(num) >= len(den):
        for i in range(len(num)):
            if i <= len(den)-1:
                if num[i] == den[i]:
                    result += "0"
                else:
                    result += "1"
            else:
                result += num[len(den):]
                break

        if result == den:
            return ""
        else:
            result = result.lstrip("0")
            return poly_mod_div(result,den)  
    else: 
        return num


def find_genpol(data):
    """Finds generator polynomials of Hamming (n,k) code. 
    
    Must correcspond with (2^n - 1, 2^n - n - 1) n ∈ ℕ.
    
    Parameters
    ------------
    data (str): Data in binary format.
    degree (int): Degree of generating polynomial (i.e number of security bits).
    """
    k = len(data)

    for i in range(k):
        if 2**i - i - 1 == k:
            n = 2**i - 1 
            r = n - k
            break
    else:
        return ValueError("Must be a Hmming code"), False
        

    genpols = []
    polynomials = []
    permutations = list(product(["0", "1"], repeat = r+1))    
    dividend = "1" + "0"*(n-1) + "1"

    for k in permutations:
        polynomials.append(''.join(k))
    del polynomials[0] # getting rid of 000

    for pol in polynomials:
        if poly_mod_div(dividend,pol) == "" and len(pol.lstrip("0")) == r+1:  
            genpols.append(pol)
    
    return genpols

def error_correction(pol,error_index):
    """Inverts a single bit at the position of error.
    
    Parameters
    ------------
    pol (str): Invalid data in binary format
    error_index (int): Index of error in data (left side starting from zero)
    """

    corrected = ""
    for i in range(len(pol)):
            if i == error_index:
                if pol[i] == "1": 
                    corrected += "0"
                else: 
                    corrected += "1" 
            else:
                corrected += pol[i]
    return corrected


def encoder(data,genpol):
    """Secures binary data with CRC code with given generator polynomial.
    
    Parameters
    ------------
    data (str): Data in binary format
    genpol (str): Generator polynomial of Hamming (n,k) code.
    """

    num = data + "0"*(len(genpol)-1)
    remainder = poly_mod_div(num,genpol) 
    
    if len(remainder) < len(genpol)-1:
        sent_data = data + "0"*((len(genpol)-1) - len(remainder)) + remainder
    else:
        sent_data = data + remainder
    return sent_data


def decoder(received,genpol):
    """Decodes received data, if error was detected durring transmission correction is applied (works only on single error).
    
    Parameters
    ------------
    received (str): Received data in binary format.
    genpol (str): Generator polynomial of Hamming (n,k) code.
    """

    corrected_data = ""
    remainder = poly_mod_div(received,genpol)

    if remainder == "":
        print("No error occured during transmission")
        return received

    else:
        for i in range(len(received)):
            pol = "1" + "0"*i 
            if poly_mod_div(pol,genpol) == remainder:
                error_index = len(received)-1 - i # indexing from left side 0,1,..
                break

        error_deg = len(received)-1 - error_index  # indexing from right side 0,1,..
        corrected_data = error_correction(received,error_index)

        print(f"Error occured during transmission in x^{error_deg}")
        print("Data after error correction --> ",corrected_data)

        return corrected_data, error_deg


def start_gui():
    global root 
    root = Tk()
    root.title("CRC CODER")

    enter_data_label = Label(text="Enter your binary data:")
    wrong_data_label = Label(text="Data must be in binary!")
    not_hamming_label = Label(text="Must be a hamming code.")
    no_data_label = Label(text="No Data!\n")
    wrong_genpol_label = Label(text="Choose one of above-mentioned polynomials:\n")

    enter_data_label.pack()
    
    data_entry = Entry(root,width=30,font="Courier")
    genpol_entry = Entry(root,width=30,font="Courier")
    received_entry = Entry(root,width=30,font="Courier")
    data_entry.pack()

    def third_button():
        """Confirms the entry of received data."""
        received = received_entry.get()

        if check_format(received_entry.get()) == False:
            wrong_data_label.pack()
        else:
            decoded = decoder(received_entry.get(),genpol_entry.get())
            Label(text="Received data").pack()
            Label(text=received,font="Courier").pack()
            Label(text=pol_format(received)).pack()
            Label(text="").pack()

            if encoded == decoded:
                received_button.config(state="disabled")
                Label(text="No error occured during transmission").pack()
                Label(text="").pack()
                Button(text="RESET",command=reset_gui).pack()
                
            else:
                received_button.config(state="disabled")
                corrected_data = decoder(received_entry.get(),genpol_entry.get())
                Label(text=f"Error occured on position: x^{str(corrected_data[1])}").pack()
                Label(text="Corrected sequence is: ").pack()
                Label(text=corrected_data[0],font="Courier").pack()
                Label(text=pol_format(corrected_data[0])).pack()
                Label(text="").pack()
                Button(text="RESET",command=reset_gui).pack()


    def second_button():
        """Confirms the entry of generator polynomial."""
        if check_format(genpol_entry.get()) == False:
            wrong_data_label.pack()
        elif genpol_entry.get() not in find_genpol(data_entry.get()):
            wrong_genpol_label.pack()
        else:
            global encoded; encoded = encoder(data_entry.get(),genpol_entry.get())
            global received_button; received_button = Button(text="OK",command=third_button)
            genpol_entry.config(state="disabled")
            genpol_button.config(state="disabled")
            Label(text="Sequence sent:").pack()
            Label(text=encoded,font="Courier").pack()
            Label(text=pol_format(encoded)).pack()
            Label(text="___________________________________\n").pack()
            Label(text="Enter received data: ").pack()
            received_entry.pack()
            received_button.pack()
            

    def first_button():
        """Confirms the entry data."""
        if check_format(data_entry.get()) == False:
            wrong_data_label.pack()
        elif len(data_entry.get()) == 0:
            no_data_label.pack()
        elif find_genpol(data_entry.get())[1] == False:
            #first_button.config(state="disabled")
            not_hamming_label.pack()
        else:
            global genpol_button; genpol_button = Button(text="OK",command=second_button) 
            data_entry.config(state="disabled")
            check_data.config(state="disabled")
            bin_genpols = [i for i in find_genpol(data_entry.get())]
            Label(text="").pack()
            Label(text="Data:").pack()
            Label(text=data_entry.get(),font="Courier").pack()
            Label(text=pol_format(data_entry.get())+"\n").pack()
            Label(text="Available Generator polynomials:").pack()
            for genp in bin_genpols:
                Label(text=genp+":  "+pol_format(genp)).pack()
            Label(text="").pack()
            Label(text="Choose one of generator polynomials (binary):").pack()
            genpol_entry.pack()   
            genpol_button.pack()
            

    check_data = Button(root,text="OK",command=first_button) 
    check_data.pack()
    root.mainloop()


if __name__ == "__main__":
    def reset_gui():
        root.destroy()
        start_gui()
    start_gui()
