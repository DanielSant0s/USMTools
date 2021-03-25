import io
import shutil
import os
from os import listdir
from os.path import isfile, join, dirname, splitext


fileList = [ 
    f for f in listdir(dirname(__file__)) if isfile(join(dirname(__file__), f))
]

#Header_Section 0x38
#LBA_Section 0xBFE0
#FileData Individual Section 0x50

DEV_MODE = 0

for file in fileList:
    _, ext = splitext(file)
    if ext == ".PAK":
        print("Resource pack:", file)
        with io.open(file, mode="rb") as rPack:
            rPack.seek(0, 2)
            numOfBytes = rPack.tell()
            print("Total Size:", numOfBytes, "bytes")

            #RESOURCE_PACK_VERSION
            rPack.seek(0, 0)
            rpVersion = rPack.read(4)
            rpVersion = int.from_bytes(rpVersion, 'little')
            #RESOURCE_ENTITY_MASH_VERSION
            rPack.seek(4, 0)
            rpEMV = rPack.read(4)
            rpEMV = int.from_bytes(rpEMV, 'little')
            #RESOURCE_NOENTITY_MASH_VERSION
            rPack.seek(8, 0)
            rpNEMV = rPack.read(4)
            rpNEMV = int.from_bytes(rpNEMV, 'little')
            #RESOURCE_AUTO_MASH_VERSION
            rPack.seek(12, 0)
            rpAMV = rPack.read(4)
            rpAMV = int.from_bytes(rpAMV, 'little')
            #RESOURCE_RAW_MASH_VERSION
            rPack.seek(16, 0)
            rpRMV = rPack.read(4)
            rpRMV = int.from_bytes(rpRMV, 'little')
            #Header Section Size
            rPack.seek(28, 0)
            headerSize = rPack.read(4)
            headerSize = int.from_bytes(headerSize, 'little')
            #LBA_SECTION
            rPack.seek(32, 0)
            lbaSize = rPack.read(4)
            lbaSize = int.from_bytes(lbaSize, 'little')

            if rpVersion == 14:
                print("Game: Ultimate Spider-Man NTSC 1.0")
            elif rpVersion == 10:
                print("Game: Ultimate Spider-Man NTSC 06/20/2005 Prototype")

            if DEV_MODE == 1:
                print("\nDeveloper info:\n")
                print("RESOURCE_PACK_VERSION", rpVersion)
                print("RESOURCE_ENTITY_MASH_VERSION", rpEMV)
                print("RESOURCE_NOENTITY_MASH_VERSION", rpNEMV)
                print("RESOURCE_AUTO_MASH_VERSION", rpAMV)
                print("RESOURCE_RAW_MASH_VERSION", rpRMV)
                print("Header Section Size:", headerSize, "bytes")
                print("LBA Section Size:", lbaSize, "bytes")
            

            #Read LBA
            rPack.seek(headerSize, 0)
            rpLBA = rPack.read(lbaSize)
            rpLBA = [rpLBA[i:i+80] for i in range(0, len(rpLBA), 80)]
            print(len(rpLBA), "Files detected")

            fileIndex = 0
            lbafile = open("lba.txt", mode="w")
            for fileIndex in range(len(rpLBA)):
                fname = rpLBA[fileIndex]
                ndisplay = fname[48:80]
                ndisplay = ndisplay.decode('utf-8')
                filesize = fname[24:28]
                filesize = int.from_bytes(filesize, 'little')
                offset1 = fname[0:4]
                offset1 = int.from_bytes(offset1, 'little')
                offset2 = fname[4:8]
                offset2 = int.from_bytes(offset2, 'little')
                offset3 = fname[8:12]
                offset3 = int.from_bytes(offset3, 'little')
                offset4 = fname[12:16]
                offset4 = int.from_bytes(offset4, 'little')
                offset9 = fname[32:36]
                offset9 = int.from_bytes(offset9, 'little')
                offseta = fname[36:40]
                offseta = int.from_bytes(offseta, 'little')
                offsetb = fname[40:44]
                offsetb = int.from_bytes(offsetb, 'little')
                lbaargs = (ndisplay, "-", hex(filesize), hex(offset1), hex(offset2), hex(offset3), hex(offset4), hex(offset9), hex(offseta), hex(offsetb), "\n")
                ws = ' '.join(lbaargs)
                if DEV_MODE == 1:
                    print(ws)
                lbafile.write(ws)
                fileIndex =+ 1
            lbafile.close()
            print("LBA Extracted")

            folder = "resourcepack"
            try:
                os.mkdir(folder)
            except OSError:
                print ("Creation of the directory %s failed" % folder)
            else:
                print ("Successfully created the directory %s " % folder)
            fileindex = 0
            DataSec = 65536
            rPack.seek(DataSec, 0)
            for fileIndex in range(len(rpLBA)):
                fname = rpLBA[fileIndex]
                ndisplay = fname[48:80]
                ndisplay = ndisplay.decode('utf-8')
                filesize = fname[24:28]
                filesize = int.from_bytes(filesize, 'little')
                filepath = os.path.join(folder, ndisplay + ".nfl")
                filepath = ''.join(x for x in filepath if x.isprintable())
                filePos = rPack.tell()
                print(filepath, hex(filePos))
                nfldata = rPack.read(filesize)
                nflfile = open(filepath, mode="wb")
                nflfile.write(nfldata)
                nflfile.close()
                fileIndex =+ 1
            

input("\nDone.")
