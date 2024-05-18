from PyQt5 import uic  

with open("kelimeEkle.py","w",encoding="utf-8") as fout:
    uic.compileUi("kelimeEkle.ui",fout)
