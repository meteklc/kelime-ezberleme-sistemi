from ast import Index
import enum
import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
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
from datetime import datetime
from RaporEkran import *





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

RaporEkrani=QMainWindow()
uiRaporEkrani=Ui_Rapor()
uiRaporEkrani.setupUi(RaporEkrani)

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
    kullaniciAdi = uiKayitEkrani.kayitKullaniciAdiLne.text()
    sifre = uiKayitEkrani.kayitSifreLne.text()
    eposta = uiKayitEkrani.kayitEpostaLne.text()

    if kullaniciAdi and sifre and eposta:
        try:
            # Kullanıcıyı kullanıcı tablosuna ekle
            ekle_kullanici = "INSERT INTO dbo.tblKullanici (kullaniciAdi, sifre, eposta, kacSoru) VALUES (?, ?, ?, ?)"
            islem.execute(ekle_kullanici, (kullaniciAdi, sifre, eposta, 10))
            baglanti.commit()

            # Eklenen kullanıcının ID'sini al
            islem.execute("SELECT IDENT_CURRENT('dbo.tblKullanici')")
            kullaniciID = islem.fetchone()[0]

            # Tüm kelime ID'lerini al
            islem.execute("SELECT kelimeID FROM dbo.tblKelimeler")
            kelimeIDler = islem.fetchall()

            # Her bir kelime için kullanıcının kelime detayını oluştur
            for kelimeID in kelimeIDler:
                ekle_kullanici_kelime_detay = "INSERT INTO dbo.tblKelimeDetay (kelimeSayac, kelimeID, kullaniciID) VALUES (0, ?, ?)"
                islem.execute(ekle_kullanici_kelime_detay, (kelimeID[0], kullaniciID))
                baglanti.commit()

            uiKayitEkrani.statusbar.showMessage("Kayit Eklendi !", 10000)
        except Exception as e:
            print("Hata:", e)
            uiKayitEkrani.statusbar.showMessage("Kayit Eklenemedi.", 10000)
    else:
        uiKayitEkrani.statusbar.showMessage("Tüm alanları doldurun!", 10000)

# BUTONLAR
# -------------------------------------------------

uiKayitEkrani.kayitEkleBtn.clicked.connect(kayit_ekle)
uiKayitEkrani.geriDonBtn.clicked.connect(anaPencere.show)
uiKayitEkrani.geriDonBtn.clicked.connect(kayitEkrani.close)








#G�R�S KISMI
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
dogru_sayac = 0
yanlis_sayac = 0

def quize_basla():
    global dogru_sayac, yanlis_sayac
    quizEkrani.show()
    soru_getir()
    
def soru_getir():       
    global soruSayac
    kullaniciID=user.get_id()

    islem.execute(f"""
        SELECT TOP 1 k.kelime, k.kelimeCumle, k.kelimeGorsel 
        FROM tblKelimeler k
        INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
        WHERE kd.kelimeSayac = 0 AND kd.kullaniciID = ?
        ORDER BY NEWID();""", [kullaniciID])
    
    cekilen_veri = islem.fetchone()
    
    if cekilen_veri:
        cekilen_kelime, cekilen_cumle, cekilen_gorsel = cekilen_veri
        uiQuizEkrani.kelimeLabel.setText(cekilen_kelime)
        uiQuizEkrani.cumleLabel.setText(cekilen_cumle)
        if cekilen_gorsel:
            pixmap = QPixmap(cekilen_gorsel)
            uiQuizEkrani.gorselLabel.setPixmap(pixmap)
        uiQuizEkrani.cevapLne.clear()
        soruSayac += 1
    else:
        uiQuizEkrani.statusbar.showMessage("Yeterince ekli kelime yok!", 10000)
    baglanti.commit()

def cevabi_gir():
    global dogru_sayac, yanlis_sayac

    kullaniciID=user.get_id()
    girilen_kelime = uiQuizEkrani.cevapLne.text()
    mevcut_kelime = uiQuizEkrani.kelimeLabel.text()
    

    islem.execute("""
    SELECT k.*
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE k.kelime = ? AND k.kelimeTurkcesi = ? AND kd.kullaniciID = ?
    """, (mevcut_kelime, girilen_kelime, kullaniciID))
    kelimeDogruMu = islem.fetchone()
    baglanti.commit()
    
    
    if kelimeDogruMu:    
        dogru_sayac += 1
        islem.execute("""
            UPDATE tblKelimeDetay
            SET kelimeSayac = kelimeSayac + 1,
                kelimeBilinmeTarih = ?
            FROM tblKelimeDetay
            INNER JOIN tblKelimeler ON tblKelimeDetay.kelimeID = tblKelimeler.kelimeID
            WHERE tblKelimeler.kelimeTurkcesi = ?
            AND tblKelimeDetay.kullaniciID = ?
        """, (datetime.now().date(), girilen_kelime, kullaniciID))
        
        islem.execute("""
            SELECT kelimeSayac
            FROM tblKelimeDetay
            INNER JOIN tblKelimeler ON tblKelimeDetay.kelimeID = tblKelimeler.kelimeID
            WHERE tblKelimeler.kelimeTurkcesi = ?
            AND tblKelimeDetay.kullaniciID = ?
        """, (girilen_kelime, kullaniciID))
        
        kelimeSayac = islem.fetchone()[0]
        baglanti.commit()

        
        if kelimeSayac == 6:
            islem.execute("""
            UPDATE tblKelimeDetay 
            SET kelimeSayac = kelimeSayac + 1 
            WHERE kelimeID = (SELECT kelimeID FROM tblKelimeler WHERE kelime = ?) 
            AND kullaniciID = ?
            """, (mevcut_kelime, kullaniciID))
            baglanti.commit()
        else:
            islem.execute(f"SELECT kacSoru FROM tblKullanici WHERE kullaniciID = ?",(kullaniciID,))
            kacSoru = islem.fetchone()[0]
            if soruSayac < kacSoru:
                soru_getir()
            else:
                sonraki_kelimeyi_getir()                   
    else :
        yanlis_sayac += 1
        islem.execute("""
        UPDATE tblKelimeDetay 
        SET kelimeSayac = 0 
        WHERE kelimeID = (
            SELECT TOP 1 kelimeID 
            FROM tblKelimeler 
            WHERE kelime = ? 
        ) 
        AND kullaniciID = ?
        """, (mevcut_kelime, kullaniciID))
        
        baglanti.commit()
        soru_getir()
    
def sonraki_kelimeyi_getir():
    
    kullaniciID=user.get_id()
    global soruSayac,dogru_sayac,yanlis_sayac
    
    sorgu_listesi = [
    """
    SELECT k.kelime, k.kelimeCumle, k.kelimeGorsel
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE kd.kelimeSayac = 1 AND ? - kd.kelimeBilinmeTarih >= 1 AND kd.kullaniciID = ?
    """,
    """
    SELECT k.kelime, k.kelimeCumle, k.kelimeGorsel
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE kd.kelimeSayac = 2 AND ? - kd.kelimeBilinmeTarih >= 7 AND kd.kullaniciID = ?
    """,
    """
    SELECT k.kelime, k.kelimeCumle, k.kelimeGorsel
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE kd.kelimeSayac = 3 AND ? - kd.kelimeBilinmeTarih >= 30 AND kd.kullaniciID = ?
    """,
    """
    SELECT k.kelime, k.kelimeCumle, k.kelimeGorsel
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE kd.kelimeSayac = 4 AND ? - kd.kelimeBilinmeTarih >= 90 AND kd.kullaniciID = ?
    """,
    """
    SELECT k.kelime, k.kelimeCumle, k.kelimeGorsel
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE kd.kelimeSayac = 5 AND ? - kd.kelimeBilinmeTarih >= 180 AND kd.kullaniciID = ?
    """,
    """
    SELECT k.kelime, k.kelimeCumle, k.kelimeGorsel
    FROM tblKelimeler k
    INNER JOIN tblKelimeDetay kd ON k.kelimeID = kd.kelimeID
    WHERE kd.kelimeSayac = 6 AND ? - kd.kelimeBilinmeTarih >= 360 AND kd.kullaniciID = ?
    """]
    bulunan_kelime = False
    
    for sorgu in sorgu_listesi:
        islem.execute(sorgu, (datetime.now().date(), kullaniciID))
        cekilen_veriler = islem.fetchall()
        
        if cekilen_veriler:
            bulunan_kelime = True
            for cekilen_veri in cekilen_veriler:
                cekilen_kelime, cekilen_cumle, cekilen_gorsel = cekilen_veri
                uiQuizEkrani.kelimeLabel.setText(cekilen_kelime)
                uiQuizEkrani.cumleLabel.setText(cekilen_cumle)
                if cekilen_gorsel:
                    pixmap = QPixmap(cekilen_gorsel)
                    uiQuizEkrani.gorselLabel.setPixmap(pixmap)
                uiQuizEkrani.cevapLne.clear()
                soruSayac += 1
            return        
    if not bulunan_kelime:
        RaporEkrani.show()
        quizEkrani.close()
            
        global dogru_sayac,yanlis_sayac
        uiRaporEkrani.dogruLabel.setText(str(dogru_sayac))
        uiRaporEkrani.yanlisLabel.setText(str(yanlis_sayac))

        uiRaporEkrani.pushButton.clicked.connect(RaporEkrani.close)            
        dogru_sayac = 0
        yanlis_sayac = 0
soruSayac=0   
    
    
uiQuizEkrani.cevapBtn.clicked.connect(cevabi_gir)



file_path = None

def kelime_ekleme():
    kelimeEklemeEkrani.show()
    menuEkrani.close()
    
    def import_file():
        global file_path
        file_path = filedialog.askopenfilename(title="Gorsel Seciniz", filetypes=[("Gorseller", "*.png"),("Gorseller", "*.jpg")])
        if file_path:
            uikelimeEklemeEkrani.gorselBtn.clicked.disconnect(import_file)
            uikelimeEklemeEkrani.gorselBtn.clicked.connect(file_path_bosalt)
            uikelimeEklemeEkrani.gorselBtn.clicked.connect(import_file)

    def kelime_ekle():
        global file_path
        if file_path:
            gorsel = file_path
            kelime = uikelimeEklemeEkrani.kelimeLne.text()
            kelimeTurkcesi = uikelimeEklemeEkrani.kelimeTrLne.text()
            kelimeCumle = uikelimeEklemeEkrani.kelimeCumleTxt.toPlainText()

            if kelime != "" and kelimeTurkcesi != "" and kelimeCumle != "":
                islem.execute(f"SELECT kelime FROM tblKelimeler WHERE kelime='{kelime}'")
                kelimeMevcutMu = islem.fetchone()
                baglanti.commit()

                if kelimeMevcutMu is None:
                    try:
                        ekle = "insert into dbo.tblKelimeler(kelime,kelimeTurkcesi,kelimeCumle,kelimeGorsel) values(?,?,?,?)"
                        islem.execute(ekle, (kelime, kelimeTurkcesi, kelimeCumle, gorsel))
                        baglanti.commit()
                        uikelimeEklemeEkrani.kelimeLne.clear()
                        uikelimeEklemeEkrani.kelimeTrLne.clear()
                        uikelimeEklemeEkrani.kelimeCumleTxt.clear()
                        uikelimeEklemeEkrani.statusbar.showMessage("Kelime Eklendi !", 10000)
                    except Exception as e:
                        print("Hata:", e)
                        uikelimeEklemeEkrani.statusbar.showMessage("Kelime Eklenemedi.", 10000)
                    try:

                        ekle = "insert into dbo.tblKelimeler(kelime,kelimeTurkcesi,kelimeCumle,kelimeGorsel) values(?,?,?,?)"
                        islem.execute(ekle, (kelime, kelimeTurkcesi, kelimeCumle, gorsel))
                        baglanti.commit()

                        # Eklenen kullanıcının ID'sini al
                        islem.execute("SELECT IDENT_CURRENT('dbo.tblKelimeler')")
                        kelimeID = islem.fetchone()[0]

                        # Tüm kelime ID'lerini al
                        islem.execute("SELECT kullaniciID FROM dbo.tblKullanici")
                        kullaniciIDler = islem.fetchall()

                        # Her bir kelime için kullanıcının kelime detayını oluştur
                        for kullaniciID in kullaniciIDler:
                            ekle_kullanici_kelime_detay = "INSERT INTO dbo.tblKelimeDetay (kelimeSayac, kelimeID, kullaniciID) VALUES (0, ?, ?)"
                            islem.execute(ekle_kullanici_kelime_detay, (kelimeID, kullaniciID[0]))
                            baglanti.commit()
                        uikelimeEklemeEkrani.kelimeLne.clear()
                        uikelimeEklemeEkrani.kelimeTrLne.clear()
                        uikelimeEklemeEkrani.kelimeCumleTxt.clear()
                        uiKayitEkrani.statusbar.showMessage("Kayit Eklendi !", 10000)
                    except Exception as e:
                        print("Hata:", e)
                        uiKayitEkrani.statusbar.showMessage("Kayit Eklenemedi.", 10000)
                else:
                    uikelimeEklemeEkrani.statusbar.showMessage("Bu Kelime Zaten Mevcut.", 10000)
            else:
                uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Tum Alanlari Doldurun!", 10000)
        else:
            uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Gorsel Seciniz!", 10000)

    def gorsel_ekleyiniz():
        uikelimeEklemeEkrani.statusbar.showMessage("Lutfen Gorsel Ekleyiniz!", 10000)

    def file_path_bosalt():
        global file_path
        file_path = None
        uikelimeEklemeEkrani.gorselBtn.clicked.disconnect(file_path_bosalt)
        uikelimeEklemeEkrani.gorselBtn.clicked.disconnect(import_file)
        uikelimeEklemeEkrani.gorselBtn.clicked.connect(import_file)

    uikelimeEklemeEkrani.gorselBtn.clicked.connect(import_file)
    uikelimeEklemeEkrani.kelimeEkleBtn.clicked.connect(kelime_ekle)
    uikelimeEklemeEkrani.geriDonBtn.clicked.connect(menuEkrani.show)
    uikelimeEklemeEkrani.geriDonBtn.clicked.connect(kelimeEklemeEkrani.close)




def ayarlar():
    ayarlarEkrani.show()
    menuEkrani.close()
    def kac_soru():
        kullaniciID=int(user.get_id())
        kacSoru=int(uiAyarlarEkrani.kacSoruBox.text())
        print(kacSoru)
        print(kullaniciID)
        try:
            print(f"update tblKullanici set kacSoru='{kacSoru}' where kullaniciID='{kullaniciID}'")
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
