import math
import csv
from pathlib import Path

class Nokta:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def mesafe(self, diger):
        x = diger.x - self.x
        y = diger.y - self.y
        return math.hypot(x, y)

class Olcum:
    def __init__(self, zaman, konum, hiz):
        self.zaman = zaman
        self.konum = konum
        self.hiz = hiz

class SurusKaydi:
    def __init__(self, olcumler ):
        self.olcumler = olcumler
    @classmethod
    def dosyadan(cls, yol):
        olcumler = []
        try:
            with open(yol, "r", newline="") as dosya:
                okuyucu = csv.DictReader(dosya)
                for satir in okuyucu:
                    try:
                        zaman = float(satir["t"])
                        x = float(satir["x"])
                        y = float(satir["y"])
                        hiz = float(satir["hiz"])

                        konum = Nokta(x,y)
                        olcum = Olcum(zaman, konum, hiz)
                        olcumler.append(olcum)

                    except (ValueError, KeyError, TypeError):
                        print("Bozuk satir atlandi.")
        except FileNotFoundError:
            print("Hata: Dosya bulunamadi!")
        return cls(olcumler)
    def toplam_mesafe(self):
        toplamMesafe = 0

        for i in range(len(self.olcumler) - 1):
            mevcut_konum = self.olcumler[i].konum
            sonraki_konum = self.olcumler[i + 1].konum

            toplamMesafe += mevcut_konum.mesafe(sonraki_konum)

        return toplamMesafe 

    def max_hiz(self):
        hizlar = []

        for olcum in self.olcumler:
            hizlar.append(olcum.hiz)
        
        if not hizlar:
            return 0
        return max(hizlar)

    def durma_sayisi(self):
        sayac = 0

        for olcum in self.olcumler:
            if olcum.hiz == 0:
                sayac += 1

        return sayac

    def ortalama_hiz(self):
        mesafe = self.toplam_mesafe()

        if len(self.olcumler) < 2:
            return 0
        
        sure = self.olcumler[-1].zaman - self.olcumler[0].zaman

        if sure <= 0:
            return 0
        
        ortalama = mesafe / sure
        return ortalama

    def grafik_ciz(self):
        import matplotlib.pyplot as plt
        
        x_degerleri = []
        y_degerleri = []

        for olcum in self.olcumler:
            x_degerleri.append(olcum.konum.x)
            y_degerleri.append(olcum.konum.y)

        if not self.olcumler:
            print("Grafik için veri bulunamadi!")
            return
        plt.plot(x_degerleri, y_degerleri, marker ="o")
        plt.title("Aracin guzergahi")
        plt.xlabel("X koordinati")
        plt.ylabel("Y koordinati")
        plt.grid(True)
        plt.savefig("surus_grafigi.png")
        plt.show()

    def hiz_asimlari(self, limit):
        asimlar = []

        for olcum in self.olcumler:
            if olcum.hiz > limit:
                asimlar.append(olcum.zaman)
        return asimlar

def sonuclari_yazdir(surus):
    print("Toplam mesafe : ", surus.toplam_mesafe())
    print("Maksimum hiz : ", surus.max_hiz())
    print("Durma sayisi : ", surus.durma_sayisi())
    print("Ortalama hizi : ", surus.ortalama_hiz())
    print("Hiz asimi zamanlari : ", surus.hiz_asimlari(4))

if __name__ == "__main__":
    nokta1 = Nokta(0,0)
    nokta2 = Nokta(3, 4)

    assert nokta1.mesafe(nokta2) == 5

    konum = nokta2
    olcum = Olcum(2, konum, 5)

    assert olcum.hiz == 5
    assert olcum.zaman == 2

    olcum1 = Olcum(0, nokta1, 0)
    olcum2 = Olcum(1, nokta2, 5)
    olcum3 = Olcum(2, Nokta(6, 8), 5)

    kayit = SurusKaydi([olcum1, olcum2, olcum3])

    assert kayit.toplam_mesafe() == 10
    assert kayit.hiz_asimlari(4) == [1, 2]

    print("Bütün testler başarili!")

    surus = SurusKaydi.dosyadan(Path(__file__).with_name("surus.csv"))
    sonuclari_yazdir(surus)
    surus.grafik_ciz()
