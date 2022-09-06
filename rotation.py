import copy

spiece = [[0,1,1],
          [1,1,0]]

'''
npiece should be 
    [[0 1],
     [1,1],
     [1,0]]
'''
def rightRotation(spiece):
    #sCols, sRows
    #nsRows,nsCols
    nRows = len(spiece)
    nCols = len(spiece[0])
    nsRows, nsCols = (nCols,nRows)
    nspiece = [[0]*nsCols for row in range(nsRows)]
    print("Starting Right spin")
    for nRow in range(nsRows):
        for nCol in range(nsCols):
            sblock = spiece[nCol][nRows - nRow]
            nspiece[nRow][nCol] = sblock

    print(f"right spin performed:")
    print(nspiece)
    print()
    return nspiece


# def rightRotation(spiece):
#     #3 left rotations is a right rotation
#     for i in range(2):
#         spiece = leftRotation(spiece)
#     print("left spin performed")
#     print(spiece)

spiece = rightRotation(spiece)

