import os
import shutil
import argparse
from argparse import RawTextHelpFormatter
import string
import random
from io import TextIOWrapper
from datetime import datetime


def currentDatetime():
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    return str(datetime.fromtimestamp(int(ts), tz=None))


def formatDatetime(string):
    return string.replace(" ", "_").replace(":", "-")


def randomName(length = 40):
   letters = string.ascii_letters + string.digits
   return ''.join(random.choice(letters) for i in range(length))


def makeFileName(fileName, keepName=False, removeExt=False):
    split = os.path.splitext(fileName)
    if keepName:
        name = split[0]
    else:
        name = randomName()
    if removeExt:
        ext = ""
    else:
        ext = split[1]
        
    return name + ext
    

# PARSER
parser = argparse.ArgumentParser(
    description= "Copy all files from a directory to another one with the aim of making it difficult to browse.\n"
                 "By default the subdirectory tree is destroyed and filenames changed to random strings.\n"
                 "The result is saved as text file in the same script folder.",
    formatter_class=RawTextHelpFormatter
    )
parser.add_argument(
    "-v",
    "--verbose",
    help="show the progress (recommended for large folders)",
    action="store_true",
    default=False
    )
parser.add_argument(
    "-d",
    "--dry-run",
    dest="dryrun",
    help="perform a trial run with no changes made. dump file is still made.",
    action="store_true",
    default=False
    )
parser.add_argument(
    "-m",
    "--move",
    help="move instead of copy (pay attention)",
    action="store_true",
    default=False
)
parser.add_argument(
    "-t",
    "--keep-tree",
    dest="keeptree",
    help="preserve the subdirectories",
    action="store_true",
    default=False
)
parser.add_argument(
    "-n",
    "--keep-name",
    dest="keepname",
    help="preserve the original file names.",
    action="store_true",
    default=False
)
parser.add_argument(
    "-e",
    "--remove-ext",
    dest="removeext",
    help="remove the file extensions",
    action="store_true",
    default=False
)

args = parser.parse_args()


# Acquisizione cartelle e conferma
rootPath = 0
while os.path.isdir(rootPath) == False:
    rootPath = input("Enter the full path of the SOURCE folder: ")
destPath = 0
while os.path.isdir(destPath) == False or destPath == rootPath or rootPath in destPath or destPath in rootPath:
    destPath = input("Enter the full path of the DESTINATION folder: ")
print("\nATTENTION: The operation is irreversible!")
confirmation = input("Digit CONFIRM to continue: ")
if confirmation != 'CONFIRM':
    raise SystemExit 


startDatetime = currentDatetime()
original_names_file_title: str = f'dump_{formatDatetime(currentDatetime())}.txt'
equality: str = '>>>'

dump_file = open(original_names_file_title, 'w')


# ciclo dell'albero delle cartelle
for root, dirnames, filenames in os.walk(rootPath):
    for filename in filenames:

        oldPath = os.path.join(root, filename)

        # determino il percorso
        if args.keeptree:
            filedir = root.replace(rootPath, destPath)
            # le cartelle che non esistono nella destinazione vengono create al volo
            if not os.path.exists(filedir): 
                os.mkdir(filedir)
        else:
            filedir = destPath


        # determino il nome del file
        newName = makeFileName(filename, args.keepname, args.removeext)

        # assemblo percorso e nuovo nome
        newPath = os.path.join(filedir, newName)

        if args.verbose:
            print(f'{oldPath} \t{equality}\t {newPath}')


        # prima di copiare affettua un controllo sul nome del file per evitare doppioni
        while os.path.exists(newPath):
            newPath += "(1)"

        if args.dryrun == False:
            if args.move:
                shutil.move(oldPath, newPath)
            else:
                shutil.copy(oldPath, newPath)
        # salvo l'operazione del dump file
        dump_file.write(f'{oldPath} \t{equality}\t {newPath} \n')


# salvo l'orario di fine nel dump file
dump_file.write(f'\n\nROOT DIR: {rootPath}\nDEST DIR: {destPath}\n\nSTART: {startDatetime}\nEND: {currentDatetime()}')
dump_file.close()