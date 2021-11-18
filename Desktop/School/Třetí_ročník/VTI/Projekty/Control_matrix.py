def H_to_G(H):
    """Takes unsystematic control matrix as input (list of lists) and assembles it to systematic one (if possible).
    Generating matrix (systematic and unsystematic) is then generated from control matrix. 
    
    Control matrix MUST be binary.
    For more info check Hamming Codes.
    """
    def transpose(M):
        return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

    def print_matrix(name,M):
        print(" "*(len(H[0])//2+2),name)
        for row in M:
            print(str(row).strip("[]").replace(",","").replace("0","O")) # for beter readability :)
        print()
            
    # n,k based on control matrix H not G
    n = len(H[0])
    k = len(H)
    H_T = transpose(H)
    permutations = []

    i = k-1  # len of row (transposed)-1
    j = n-1  # n of rows (transposed)-1

    # Systematic control matrix 
    for row in range(n):
        if i >= 0:
            if H_T[row][i] != 0 and H_T[row][i] != 1:
                raise ValueError("Matrix must be binary")

            elif H_T[row][i] == 1 and H_T[row].count(0) == k-1:
                H_T[j],H_T[row] = H_T[row], H_T[j]
                permutations.append(row)
                i -= 1; j -= 1    
        else: 
            break

    # check if identity matrix is in H_T
    eye = [[0 for _ in range(k)] for _ in range(k)]
    for i in range(k): eye[i][i] = 1 

    for row in eye: 
        if row not in H_T: raise ValueError("Systematic matrix couldn't be generated.")

    Hs = transpose(H_T)

    # Systematic generating matrix 
    G = [[0 for _ in range(n)] for _ in range(n-k)]
    for m in range(0,n-k):
        G[m][m] = 1
        G[m][n-k:] = H_T[m]

    # Generating matrix 
    Gs_T = transpose(G)
    i = len(Gs_T)-1
    for swap in permutations:
        Gs_T[i],Gs_T[swap] = Gs_T[swap], Gs_T[i]
        i -= 1
    Gs = transpose(Gs_T)

    print_matrix("H",H)
    print_matrix("Hs",Hs)
    print_matrix("G",G)
    print_matrix("Gs",Gs)
    return Hs,Gs,G

# examples of control matrices
H =[[0,0,0,1,1,1,1],
    [0,1,1,0,0,1,1],
    [1,0,1,0,1,0,1]]
"""
H =[[1,1,1,0,1,0,0],
    [1,1,0,1,0,1,0],
    [1,0,1,1,0,0,1]]
""" """
H =[[1,0,1,0,0,0,0,0],
    [1,0,0,1,0,0,0,0],
    [1,1,0,0,1,0,0,0],
    [1,1,0,0,0,1,0,0],
    [0,1,0,0,0,0,1,0],
    [0,1,0,0,0,0,0,1]] 
"""
H_to_G(H)


