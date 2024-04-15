import sys
import os

os.system ("cls")
sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv)>0:
    strFile=sys.argv[1]

def notBits(num_bits):
    Binreverse=""
    for i in range(len(num_bits)):
        if num_bits[i:i+1] == "1":
            Binreverse +=  "0"
        else:
            Binreverse +=  "1"
    return Binreverse

def getValueDec(byteData, field, onlyValue=False):
    decData =0
    hexstrData=""
    hexData=""
    for i in reversed(range(field[0]-1,field[0]-1 + field[1])):
        #print ("--> "  + str(i) + " " + str(hex(byteData[i])))
        hexstrData = hexstrData + str(hex(byteData[i]))[2:]
        hexData = hexData  + " " + str(hex(byteData[i]))
    decData= int(hexstrData,16)
    if not onlyValue:
        strData = "[" + str(decData) + "]" + " - " + str(hex(field[0]-1)) + "    " + hexData
    else:
        strData = str(decData) 
    return strData

def getLineRaster(byteData, iniByte,szWidth):
    BitMapBin=""
    n=1
    if sizeWidth % 32 != 0:
        n=1 
    nBytes = (((sizeWidth - (sizeWidth % 32))/8/4)+n)*4
    #iniByte=int(0x3E)
    #print("===> " + str(nBytes))
    #print("===> " + str(iniByte))
    for n in range(iniByte,iniByte + int(nBytes)):
        #print( "=>>> " + str(hex(byteData[n])))
        BitMapBin += notBits((str(bin(byteData[n]))[2:]).zfill(8))
        BitMapBin= BitMapBin[0:szWidth]
        #print(BitMapBin, end="")
    #print (BitMapBin)
    return BitMapBin
    
    

Signature           = [1,2]
FileSize            = [3,4]
Reserved            = [7,4]
DataOffset          = [11,4]
Size                = [15,4]
Width               = [19,4]
Height              = [23,4]
Planes              = [27,2]
BitCount            = [29,2]
Compression         = [31,4]
ImageSize           = [35,4]
XpixelsPerM         = [39,4]
YpixelsPerM         = [43,4]
ColorsUsed          = [47,4]
ColorsImportant     = [51,4]
ColorTable1         = [55,4]
ColorTable2         = [59,4]

    
with open(strFile, "rb") as f:
    data = f.read()
print("File Name: " + strFile)
print("========== HEADER ==========")
print("Signature        :   "  +  chr(data[0]) + chr(data[1]))
print("FileSize         :   "  +  getValueDec(data,FileSize) ) 
print("Reserved         :   "  +  getValueDec(data,Reserved) )  
print("DataOffset       :   "  +  getValueDec(data, DataOffset)) 

print("========== INFOHEADER ==========")

print("Size             :   "  + getValueDec(data, Size)) 
print("Width            :   "  + getValueDec(data, Width))
print("Height           :   "  + getValueDec(data, Height))
print("Planes           :   "  + getValueDec(data, Planes))
print("BitCount         :   "  + getValueDec(data, BitCount))
print("Compression      :   "  + getValueDec(data, Compression))
print("ImageSize        :   "  + getValueDec(data, ImageSize))
print("XpixelsPerM      :   "  + getValueDec(data, XpixelsPerM))
print("YpixelsPerM      :   "  + getValueDec(data, YpixelsPerM))
print("ColorsUsed       :   "  + getValueDec(data, ColorsUsed))
print("ColorsImportant  :   "  + getValueDec(data, ColorsImportant))

print("========== COLORTABLE ==========")

# cambia dependiendo de la definicion de Bitcount (bits por pixel)
print("Colors...        :   "  + getValueDec(data, ColorTable1))
print("Colors...        :   "  + getValueDec(data, ColorTable2))


print("========= RASTERDATA ===========")


startDataOffset = int(getValueDec(data, DataOffset,True))
sizeWidth = int(getValueDec(data, Width,True))
#nBytes = (((sizeWidth - (sizeWidth % 32))/8/4)+(sizeWidth % 32)) * 4
n=1
if sizeWidth % 32 != 0:
    n=1 
nBytes = (((sizeWidth - (sizeWidth % 32))/8/4)+n)*4


print ("sizeWidth " + str(sizeWidth))
print ("LenData " + str(len(data)))
print ("nBytes " + str(nBytes))
ym=0
nX = int(getValueDec(data, Width,True))
nY = int(getValueDec(data, Height,True))
a = [[0] * nX] * nY
for y in reversed(range(startDataOffset, len(data), int(nBytes))):
    #print (" ::::Y " + str(y) + " === ym" + str(ym))
    #print(getLineRaster(data,y,sizeWidth).replace("0", "  ").replace("1","**"))
    

    for n in range(0,nX):
        
        a[ym][n]= getLineRaster(data,y,sizeWidth).replace("0", "-").replace("1","*")[n:n+1]
        print( "(" + str(ym) + "-" +str(n) + ")=" + str(a[ym][n])+ " ",end="")
        #print (str(a[ym][n]),end="")
        
    print("")
    #print (">>(" + str(0) + "-" +str(2) + ")="+ str(a[0][2]) + " ", end="")
    ym=ym+1
print(" ")
for m in range(0,1):  
    for n in range(0,16):
        print ("(" + str(m) + "-" +str(n) + ")="+ str(a[m][n]) + " ", end="")
    print("")


