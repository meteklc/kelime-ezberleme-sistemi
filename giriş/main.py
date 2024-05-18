from ast import Index
import enum
import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from kayitsf import *
from anasayfa import *
from anamenu import *
from sifremiunuttum import *
from kelimeEkle import *




#----------------------------------------------

uygulama= QApplication(sys.argv)
anaPencere= QMainWindow()
uiAnaPencere= Ui_MainWindow()
uiAnaPencere.setupUi(anaPencere)

kayitEkrani= QMainWindow()
uiKayitEkrani= Ui_kayitWindow()
uiKayitEkrani.setupUi(kayitEkrani)

sifremiUnuttumEkrani= QMainWindow()
uiSifremiUnuttumEkrani= Ui_SifremiUnuttum()
uiSifremiUnuttumEkrani.setupUi(sifremiUnuttumEkrani)

menuEkrani= QMainWindow()
uiMenuEkrani= Ui_AnaMenu()
uiMenuEkrani.setupUi(menuEkrani)

kelimeEklemeEkrani= QMainWindow()
uikelimeEklemeEkrani= Ui_KelimeEkleme()
uikelimeEklemeEkrani.setupUi(kelimeEklemeEkrani)

anaPencere.show()


#SQL
#------------------------------------------------

import pypyodbc as odbc

DRIVER_NAME= 'SQL SERVER'
DATABASE_NAME= 'kelime oyunu'

connection_string= f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER=.;
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
baglanti = odbc.connect(connection_string)
islem=baglanti.cursor()
baglanti.commit()

#KAYIT KISMI---------------------------------------------------
#METODLAR
#----------------------------------------------
def kayit_ol():
    kayitEkrani.show()
    anaPencere.close()



    #METODLAR
    #-------------------------------------------------
    def kayit_ekle():
        kullaniciAdi=uiKayitEkrani.kayitKullaniciAdiLne.text()
        sifre=uiKayitEkrani.kayitSifreLne.text()
        eposta=uiKayitEkrani.kayitEpostaLne.text()
        

        if kullaniciAdi!= "":
                
            if sifre!="":
                if eposta!="":
                    islem.execute(f"SELECT kullaniciAdi FROM tblKullanici WHERE kullaniciAdi='{kullaniciAdi}'")
                    kullaniciAdiMevcutMu=islem.fetchone()
                    baglanti.commit
                    
                    if kullaniciAdiMevcutMu is not None:
                        try:
                            ekle="insert into dbo.tblKullanici(kullaniciAdi,sifre,eposta) values(?,?,?)"
                            islem.execute(ekle,(kullaniciAdi,sifre,eposta))
                            baglanti.commit()
                            uiKayitEkrani.statusbar.showMessage("Kayit Eklendi !",10000)
                        except:
                            uiKayitEkrani.statusbar.showMessage("Kayit Eklenemedi.",10000)
                    else :
                        uiKayitEkrani.statusbar.showMessage("Bu Kullanici Adi Kullanilmaktadir.",10000)
                    
                else:
                    uiKayitEkrani.statusbar.showMessage("Lütfen Sifre Giriniz !",10000)
            else: 
                
                uiKayitEkrani.statusbar.showMessage("Lütfen Sifre Giriniz !",10000)
                        
        else :
            uiKayitEkrani.statusbar.showMessage("Lütfen Kullanici Adi Giriniz !",10000)
                    
                    
    #BUTONLAR
    #-------------------------------------------------

    uiKayitEkrani.kayitEkleBtn.clicked.connect(kayit_ekle)
    uiKayitEkrani.geriDonBtn.clicked.connect(anaPencere.show)
    uiKayitEkrani.geriDonBtn.clicked.connect(kayitEkrani.close)









#GİRİS KISMI
#def
#------------------------------------------------------
def giris_yap():
    
    kullaniciAdi=uiAnaPencere.kullaniciAdiLne.text()
    sifre=uiAnaPencere.sifreLne.text()
    if kullaniciAdi!= "":
        if sifre!="":
            islem.execute(f"SELECT kullaniciAdi FROM tblKullanici WHERE kullaniciAdi='{kullaniciAdi}'")
            kullaniciAdiMevcutMu=islem.fetchone()

            baglanti.commit()
            
            if kullaniciAdiMevcutMu is not None :
                islem.execute(f"SELECT * FROM tblKullanici WHERE kullaniciAdi='{kullaniciAdi}' and sifre='{sifre}'")
                sifreMevcutMu=islem.fetchone()
                baglanti.commit()
                if sifreMevcutMu is not None :
                    menuEkrani.show()
                    anaPencere.close()
                else : 
                    uiAnaPencere.statusbar.showMessage("Sifre Yanlis !",10000)
                
            else:
                uiAnaPencere.statusbar.showMessage("Kullanici Adi Bulunmamaktadir !",10000)
            
        else:
            uiAnaPencere.statusbar.showMessage("Lütfen Sifre Giriniz !",10000)
        
    else :
        uiAnaPencere.statusbar.showMessage("Lütfen Kullanici Adi Giriniz !",10000)

#ANAMENÜ KISMI
#--------------------------------------------------

#METODLAR
#--------------------------------------------------
def quize_basla():
    print("quize basla")


def kelime_ekleme():
    kelimeEklemeEkrani.show()
    menuEkrani.close()

    
    def kelime_ekle():
        print("kelime ekle")

    uikelimeEklemeEkrani.kelimeEkleBtn.clicked.connect(kelime_ekle)
    uikelimeEklemeEkrani.geriDonBtn.clicked.connect(menuEkrani.show)
    uikelimeEklemeEkrani.geriDonBtn.clicked.connect(kelimeEklemeEkrani.close)



def ayarlar():
    print("ayarlar")

#BUTONLAR
#-----------------------------------------------

uiMenuEkrani.cikisBtn.clicked.connect(anaPencere.show)
uiMenuEkrani.cikisBtn.clicked.connect(menuEkrani.close)
uiMenuEkrani.quizBtn.clicked.connect(quize_basla)
uiMenuEkrani.keliimeEkleBtn.clicked.connect(kelime_ekleme)
uiMenuEkrani.ayarlarBtn.clicked.connect(ayarlar)





#SİFRE DEĞİŞTİRME KISMI
#-------------------------------------------------
def sifre_degis():
    sifremiUnuttumEkrani.show()
    anaPencere.close()
    uiSifremiUnuttumEkrani.geriDonBtn.clicked.connect(anaPencere.show)
    uiSifremiUnuttumEkrani.geriDonBtn.clicked.connect(sifremiUnuttumEkrani.close)




    
#BUTONLAR
#------------------------------------------------

uiAnaPencere.kayitBtn.clicked.connect(kayit_ol)
uiAnaPencere.girisBtn.clicked.connect(giris_yap)
uiAnaPencere.sifremiUnuttumBtn.clicked.connect(sifre_degis)






#---------------------------------------------------------------------------------------------------------------------
sys.exit(uygulama.exec_())
