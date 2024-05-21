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
import csv, smtplib, ssl
from quizEkrani import *
from ayarlar import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import tkinter as tk
from tkinter import filedialog






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

quizEkrani= QMainWindow()
uiQuizEkrani= Ui_quizEkrani()
uiQuizEkrani.setupUi(quizEkrani)

ayarlarEkrani= QMainWindow()
uiAyarlarEkrani= Ui_ayarlar()
uiAyarlarEkrani.setupUi(ayarlarEkrani)

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

class kullanici:
    def __init__(self, id = 0):
        self._id = id
    def get_id(self):
        return self._id
    def set_id(self, x):
        self._id=x
user = kullanici()
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
                    baglanti.commit()
                    
                    if kullaniciAdiMevcutMu is None:
                        try:
                            ekle="insert into dbo.tblKullanici(kullaniciAdi,sifre,eposta,kacSoru) values(?,?,?,?)"
                            islem.execute(ekle,(kullaniciAdi,sifre,eposta,10))
                            baglanti.commit()
                            uiKayitEkrani.statusbar.showMessage("Kayit Eklendi !",10000)
                        except:
                            uiKayitEkrani.statusbar.showMessage("Kayit Eklenemedi.",10000)
                    else :
                        uiKayitEkrani.statusbar.showMessage("Bu Kullanici Adi Kullanilmaktadir.",10000)
                    
                else:
                    uiKayitEkrani.statusbar.showMessage("Lutfen Sifre Giriniz !",10000)
            else: 
                
                uiKayitEkrani.statusbar.showMessage("Lutfen Sifre Giriniz !",10000)
                        
        else :
            uiKayitEkrani.statusbar.showMessage("Lutfen Kullanici Adi Giriniz !",10000)
                    
                    
    #BUTONLAR
    #-------------------------------------------------

    uiKayitEkrani.kayitEkleBtn.clicked.connect(kayit_ekle)
    uiKayitEkrani.geriDonBtn.clicked.connect(anaPencere.show)
    uiKayitEkrani.geriDonBtn.clicked.connect(kayitEkrani.close)









#G�R�S KISMI
#def
#------------------------------------------------------
def giris_yap(kullaniciID: any):
    
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
                    islem.execute(f"SELECT kullaniciID FROM tblKullanici WHERE kullaniciAdi='{kullaniciAdi}' and sifre='{sifre}'")
                    kullaniciID=islem.fetchone()
                    baglanti.commit()
                    user.set_id(kullaniciID[0])
                    

                    menuEkrani.show()
                    anaPencere.close()
                    
                else : 
                    uiAnaPencere.statusbar.showMessage("Sifre Yanlis !",10000)
                
            else:
                uiAnaPencere.statusbar.showMessage("Kullanici Adi Bulunmamaktadir !",10000)
            
        else:
            uiAnaPencere.statusbar.showMessage("Lutfen Sifre Giriniz !",10000)
        
    else :
        uiAnaPencere.statusbar.showMessage("Lutfen Kullanici Adi Giriniz !",10000)

#ANAMEN� KISMI
#--------------------------------------------------

#METODLAR
#--------------------------------------------------

soruSayac=0
kacSoru=10

def quize_basla():
    quizEkrani.show()

    global soruSayac

    islem.execute(f"SELECT kelime FROM tbl WHERE kelimeSayac=0 AND kelimeID random")
    cekilen_kelime = islem.fetchone()
    
    if cekilen_kelime:
        uiQuizEkrani.kelimeLabel.setText(cekilen_kelime[0])
    else:
        uiQuizEkrani.statusbar.showMessage("Yeterince Ekli kelime yok!",10000)
    baglanti.commit()
        
def cevabi_gir():
    
    girilen_kelime = uiQuizEkrani.cevapLne.text()
    mevcut_kelime = uiQuizEkrani.kelimeLabel.text()
    
    islem.execute(f"SELECT * FROM tbl WHERE kelime=? AND turkcesi=?", (mevcut_kelime, girilen_kelime))
    kelimeDogruMu = islem.fetchone()
    baglanti.commit()
    
    
    if kelimeDogruMu:
        islem.execute(f"UPDATE tbl SET kelimeSayac=kelimeSayac+1, kelimeBilinmeTarihi=? WHERE kelime=?", (datetime.now().date(), mevcut_kelime))
        kelimeSayac = islem.fetchone()[0]
        baglanti.commit()
        
        if kelimeSayac == 6:
            islem.execute(f"UPDATE tbl SET bilinen=1 WHERE kelime=?", (mevcut_kelime,))
            baglanti.commit()
        else: 
            if soruSayac < kacSoru:
                quize_basla()
            else:
                sonraki_kelimeyi_getir()    
    else :
        islem.execute(f"kelimeSayac=0")


def sonraki_kelimeyi_getir():
    global soruSayac
    
    sorgu_listesi = [
        "SELECT kelime FROM tbl WHERE kelimeSayac=1 AND ? - kelimeBilinmeTarihi > 1",
        "SELECT kelime FROM tbl WHERE kelimeSayac=2 AND ? - kelimeBilinmeTarihi > 7",
        "SELECT kelime FROM tbl WHERE kelimeSayac=3 AND ? - kelimeBilinmeTarihi > 30",
        "SELECT kelime FROM tbl WHERE kelimeSayac=4 AND ? - kelimeBilinmeTarihi > 90",
        "SELECT kelime FROM tbl WHERE kelimeSayac=5 AND ? - kelimeBilinmeTarihi > 180",
        "SELECT kelime FROM tbl WHERE kelimeSayac=6 AND ? - kelimeBilinmeTarihi > 360"
    ]
    
    for sorgu in sorgu_listesi:
        islem.execute(sorgu, (datetime.now().date(),))
        cekilen_kelime = islem.fetchone()
        
        if cekilen_kelime:
            uiQuizEkrani.kelimeLabel.setText(cekilen_kelime[0])
            soruSayac += 1
            return        

soruSayac=0   
    
    
uiQuizEkrani.cevapBtn.clicked.connect(cevabi_gir)


def kelime_ekleme():
    kelimeEklemeEkrani.show()
    menuEkrani.close()
    
    def import_file():
        file_path = filedialog.askopenfilename(title="Gorsel Seciniz", filetypes=[("Gorseller", "*.png"),("Gorseller", "*.jpg")])
        if file_path:
            
            def kelime_ekle():
        
                kelime=uikelimeEklemeEkrani.kelimeLne.text()
                kelimeTurkcesi=uikelimeEklemeEkrani.kelimeTrLne.text()
                kelimeCumle=uikelimeEklemeEkrani.kelimeCumleTxt.toPlainText()

                if kelime!= "":
                        
                    if kelimeTurkcesi!="":
                        if kelimeCumle!="":
                            islem.execute(f"SELECT kelime FROM tblKelimeler WHERE kelime='{kelime}'")
                            kelimeMevcutMu=islem.fetchone()
                            baglanti.commit()

                            if kelimeMevcutMu is None:
                                
                                    
                                    try:
                                        ekle="insert into dbo.tblKelimeler(kelime,kelimeTurkcesi,kelimeCumle,kelimeGorsel) values(?,?,?,?)"
                                        islem.execute(ekle,(kelime,kelimeTurkcesi,kelimeCumle,file_path))
                                        baglanti.commit()
                                        uikelimeEklemeEkrani.statusbar.showMessage("Kelime Eklendi !",10000)
                                    except:
                                        uikelimeEklemeEkrani.statusbar.showMessage("Kelime Eklenemedi.",10000)
                            else :
                                uikelimeEklemeEkrani.statusbar.showMessage("Bu Kelime Zaten Mevcut.",10000)
                            
                        else:
                            uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Kelimeyi Bir Cumle Icersinde Kullaniniz!",10000)
                    else: 
                        
                        uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Kelimenin Turkcesini Giriniz !",10000)
                                
                else :
                    uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Kelime Giriniz !",10000)

            uikelimeEklemeEkrani.kelimeEkleBtn.clicked.connect(kelime_ekle)
        else :
            uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Gorsel Ekleyiniz!",10000)
            
            

    def gorsel_ekleyiniz():
        uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Gorsel Ekleyiniz!",10000)

    
    uikelimeEklemeEkrani.gorselBtn.clicked.connect(import_file)
    uikelimeEklemeEkrani.kelimeEkleBtn.clicked.connect(gorsel_ekleyiniz)

    uikelimeEklemeEkrani.geriDonBtn.clicked.connect(menuEkrani.show)
    uikelimeEklemeEkrani.geriDonBtn.clicked.connect(kelimeEklemeEkrani.close)



def ayarlar():
    ayarlarEkrani.show()
    menuEkrani.close()
    def kac_soru():
        kullaniciID=int(user.get_id())
        kacSoru=int(uiAyarlarEkrani.kacSoruBox.text())
        try:
            islem.execute(f"update tblKullanici set kacSoru='{kacSoru}' where kullaniciID='{kullaniciID}'")
            baglanti.commit()
            uiAyarlarEkrani.statusbar.showMessage("Kaydedildi !",10000)
        except:
            uiAyarlarEkrani.statusbar.showMessage("Kaydedilemedi.",10000)
        
    
    uiAyarlarEkrani.kaydetBtn.clicked.connect(kac_soru)
    uiAyarlarEkrani.geriDonBtn.clicked.connect(menuEkrani.show)
    uiAyarlarEkrani.geriDonBtn.clicked.connect(ayarlarEkrani.close)
#BUTONLAR
#-----------------------------------------------

uiMenuEkrani.cikisBtn.clicked.connect(anaPencere.show)
uiMenuEkrani.cikisBtn.clicked.connect(menuEkrani.close)
uiMenuEkrani.quizBtn.clicked.connect(quize_basla)
uiMenuEkrani.keliimeEkleBtn.clicked.connect(kelime_ekleme)
uiMenuEkrani.ayarlarBtn.clicked.connect(ayarlar)





#S�FRE DE���T�RME KISMI
#-------------------------------------------------
def sifre_gonder():
    sifremiUnuttumEkrani.show()
    anaPencere.close()

    
    def kod_yolla():
        eposta=uiSifremiUnuttumEkrani.epostaLne.text()
        if eposta!="":
            islem.execute(f"SELECT eposta FROM tblKullanici WHERE eposta='{eposta}'")
            epostaVarMi=islem.fetchone()
            baglanti.commit

            if epostaVarMi is not None:

                islem.execute(f"SELECT sifre FROM tblKullanici WHERE eposta='{eposta}'")
                sifre=islem.fetchone()
                baglanti.commit

                message = f"""\
                Sifreniz Asagidadir.

                Sifreniz= {sifre[0]}"""
                gondericiEposta="kelime.oyunu.sifre.yolla@gmail.com"
                gondericiSifre="zrzi mieq eieh mtwg"
                smtp_server = "smtp.gmail.com"
                port = 587

                context = ssl.create_default_context()

                try:
                    server = smtplib.SMTP(smtp_server,port)
                    server.ehlo() 
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(gondericiEposta, gondericiSifre)
                    server.sendmail(          #�ALI�MIYOR 
                        gondericiEposta,
                        epostaVarMi[0],
                        message
                    )
                    
                except Exception as e:
                    print(e)
                finally:
                    server.quit() 
                

                
            else:
                uiSifremiUnuttumEkrani.statusbar.showMessage("Bu Epostaya ait bir kullanici bulunamamaktadir!",10000)
        
        else :
            uiSifremiUnuttumEkrani.statusbar.showMessage("Lutfen Epostanizi Giriniz !",10000)



    uiSifremiUnuttumEkrani.kodYollaBtn.clicked.connect(kod_yolla)
    uiSifremiUnuttumEkrani.geriDonBtn.clicked.connect(anaPencere.show)
    uiSifremiUnuttumEkrani.geriDonBtn.clicked.connect(sifremiUnuttumEkrani.close)




    
#BUTONLAR
#------------------------------------------------

uiAnaPencere.kayitBtn.clicked.connect(kayit_ol)
uiAnaPencere.girisBtn.clicked.connect(giris_yap)
uiAnaPencere.sifremiUnuttumBtn.clicked.connect(sifre_gonder)






#---------------------------------------------------------------------------------------------------------------------
sys.exit(uygulama.exec_())
