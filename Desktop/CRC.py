import numpy as np
from itertools import product

def check_format(input):
    input =  str(input)
    for i in input:
        if i != "0" and i != "1":
            print("Must by binary !")
            return False
    else: 
        return input
        

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
            return "0"
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
        raise ValueError("Must be a Hamming code.")

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
                error_index = len(received)-1 - i # indexing from left side (0,1,..)
                break

        error_deg = len(received)-1 - error_index  # indexing from right side (0,1,..) 
        corrected_data = error_correction(received,error_index)

        print(f"Error occured during transmission in x^{error_deg}")
        print("Data after error correction --> ",corrected_data)

        return corrected_data, error_deg


if __name__ == "__main__":

    data = input("Enter your binary data please: ")
    while check_format(data) == False:
        data = input("Enter your data in BINARY please: ")
    
    print("------------------------------------------------")
    print("List of available generator polynomials: ")
    for pol in find_genpol(data):
        print(pol)  
    print("------------------------------------------------")
    genpol = input("Please choose one generator polynomial: ")
    while genpol not in find_genpol(data):
        genpol = input("Please enter one of above-mentioned: ")

    print("------------------------------------------------")
    sent_data = encoder(data,genpol)
    polynom = np.polynomial.Polynomial([int(i) for i in sent_data][::-1])
    print("Sent data in binary --> ",sent_data)
    print("------------------------------------------------")
    print("Sent data in polynomial form: \n")
    print(polynom)
    
    print("------------------------------------------------")
    received = input("Enter received data in binary please: ")
    while check_format(received) == False:
        received = input("Enter your data in BINARY please: ")
    print("------------------------------------------------")
    decoder(received,genpol)

    # Hamming code examples 

    # data = 11111000001111100000111110
    # genpol = 100101
    # Corect received : 1111100000111110000011111001000
    #

    # data = 11111000001
    # genpol = 10011
    # corect reveived : 111110000010001
    #
    
    # data = 10101100100
    # genpol = 10011
    # correct received : 101011001000111


    