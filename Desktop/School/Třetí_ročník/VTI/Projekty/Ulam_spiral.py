import turtle as trt
from math import sqrt

def is_prime(n):
    if n < 2:
        return False
    for factor in range(2,int(sqrt(n))+1):
        if n % factor == 0:
            return False
    else:
        return True

trt.title("Calculating the Ulam spiral")
trt.tracer(0, 0) 
trt.bgcolor("black")
trt.penup()

side_width = 200
start = 1

count = 0
line_length = 1
polynomial_primes = [] 

# coefficients of quadratic polynomial 4n^2 +bn + c
b = int(-2); c = int(41) 

# examples of polynomials
# b = int(6); c = int(1) # b is even - diagonal
# b = int(3); c = int(1) # b is odd - vertical
# b = int(1); c = int(1) # b is odd - horizontal

for p,n in enumerate(range(start,side_width**2+start)):
    polynomial_primes.append(4*p**2 + b*p + c)
    trt.forward(6)
    if n == start:
        if is_prime(n):
            trt.dot(5,"white")
        else:
            trt.dot(4,"#EB1055") 
        continue

    if is_prime(n) and n in polynomial_primes:
        trt.dot(4,"yellow")
    elif is_prime(n):
        trt.dot(4,"#14CCE2") 

    count += 1
    if count == line_length:
        count = 0
        trt.left(90) 
        if trt.heading() in (0, 180): 
            line_length += 1 

trt.title(f"Ulam spiral of {side_width**2} natural numbers starting at number {start}. Yellow: {4}n^2 + {b}n + {c}; for n ∈ ℕ ")
trt.update()
trt.mainloop()