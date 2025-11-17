# bukan python kalo ga import
import os
import time
from tabulate import tabulate
import pandas as pd
# path1 = r"C:\Users\Thin\Documents\csv\perpustakaan.csv"
# path2 = r"C:\Users\Thin\Documents\csv\peminjam.csv"
# data = pd.read_csv(path1)
# data_peminjam = pd.read_csv(path2)

# ========================================================================================
def title():
    print('''
        +-----------------------------------------+
          |                                     |
        |            Perpustakaan mini            |
          |                                     |
        |          By Khairil (L0225039)          |
          |                                     |
        +-----------------------------------------+
        ''')

# dummy
data = [["10 dosa besar Soeharto", "Liotohe", 123456789, 5]]
df_perpus = pd.DataFrame(data, columns=["Judul", "Penulis", "ISBN", "Stok"])

data =[["khairil", "10 dosa besar Jokowi", "Liothe", 987654321, 3]]
df_peminjam = pd.DataFrame(data, columns=["Peminjam", "Judul", "Penulis", "ISBN", "Jumlah_yang_dipinjam"])

# ========================================================================================
class perpus:
    def __init__(self, judul, penulis, isbn, stok, peminjam, jumlah_dipinjam):
        self.judul = judul
        self.penulis = penulis
        self.isbn = isbn
        self.stok = stok
        self.peminjam = peminjam
        self.jumlah_dipinjam = jumlah_dipinjam

    # =========================
    # = nambah buku baru
    # =========================
    def tambah():
        bersih()
        while True:
            welcome("Tambah buku")
            try:
                judul = input("Masukkan judul : ")
                penulis = input("Masukkan nama penulis : ")
                isbn = int(input("Masukkan kode unik buku (isbn) : "))
                stok = int(input("Masukkan stok : "))
                konfirmasi = input("Anda yakin ? (y/n) ").lower()
                match konfirmasi:
                    case "y":
                        break
                    case "n":
                        bersih()
                        main()
                    case _:
                        bersih()
                        print("Opsi tidak diketahui...")
                        continue
            except ValueError:
                bersih()
                print("Input ISBN dan Stok harus berupa angka (int)")
                continue

        global df_perpus
        df_buku_baru = pd.DataFrame([[judul, penulis, isbn, stok]],
                                    columns=["Judul", "Penulis", "ISBN", "Stok"])
        # buku_baru = [judul, penulis, isbn, stok]
        # df_buku_baru = pd.DataFrame(buku_baru, columns=["Judul", "Penulis", "ISBN", "Stok"])
        df_perpus = pd.concat([df_perpus, df_buku_baru], ignore_index=1)
        input("Buku berhasil ditambahkan\nTekan enter untuk lanjut...")
        return df_perpus

        # =========================
        # = sesuai nama function, nampilin semua dataframe buku
        # =========================
    def tampil():
        bersih()
        welcome("Daftar Buku")
        print(tabulate(df_perpus, headers="keys", tablefmt="fancy_grid", showindex=False))
        print("\n")

    def pinjam():
        while True:
            welcome("Pinjam buku")
            user = str(input("Masukkan nama peminjam : "))
            
            # validasi...
            if (user == "") or (user == " "):
                bersih()
                print("User tidak boleh kosong!\n\n")
                continue

            judul = input("Masukkan judul buku : ").strip()
            penulis = input("Masukkan penulis buku : ").strip()
            # (flow) skip ke bagian akhir function pinjam, lompat jauh banget

            # =========================
            # = Nyari buku buat guide isbn lebih gampang
            # =========================
            def cari(df, judul, penulis):
                judul, penulis = judul.lower(), penulis.lower()
            
                hasil_cari = df[
                    (df_perpus["Judul"].str.lower().str.contains(judul, na=False)) &
                    (df_perpus["Penulis"].str.lower().str.contains(penulis, na=False))
                ]

                if not hasil_cari.empty:
                    print("Buku berhasil dicari...\n")

                    while True:
                        print(tabulate(hasil_cari, headers="keys", tablefmt="fancy_grid", showindex=False)) # nampilin (beberapa) buku

                        try:
                            isbn_pinjam =  int(input("Masukkan isbn buku yang ingin dipinjam! (lengkap)\n>> "))
                        except ValueError:
                            bersih()
                            # balik ke awal jika input tidak int
                            print("ISBN harus berupa angka! (int)")
                            continue
                        
                        # masuk next function
                        df_perpus_filtered = stok_kurang(isbn_pinjam)
                        if not df_perpus_filtered.empty:
                            break
                else:
                    # balik ke home
                    print("Buku tidak terdata / tersedia")
                    out()
                    bersih()
                    main()

            # =========================
            # = komfirmasi jumlah > update stok
            # =========================
            def stok_kurang(isbn_pinjam):
                mask = df_perpus["ISBN"] == isbn_pinjam
                df_perpus_filtered = df_perpus[mask]

                if not df_perpus_filtered.empty:
                    bersih()
                    print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
                else:
                    bersih()
                    print("ISBN yang anda tulis tidak sesuai\n")
                    while True:
                        # kalo nulis isbn nguawor / kosong masuk sini, konfirmasi, mau masukin ulang apa nggak
                        confirmation = input("Kemabli ke menu utama? (y/n)").lower()
                        match confirmation:
                            case "y": # balik ke home
                                bersih()
                                main()
                            case "n": # balik ke menu pinjam
                                bersih()
                                perpus.pinjam()
                            case _: # opsi y sama n doang bang
                                bersih()
                                print("Input tidak diketahui\n")
                                continue

                while True:
                    # tidak bosan-bosasn aku meminta konfirmasi
                    confirmation = input("Anda yakin ingin meminjam? (y/n)\n>> ")

                    match confirmation:
                        case "y": # mumet counter : 3
                            while True:
                                # konfirmasi mau pinjem berapa buku, sekalian validasi kalo inputmu aneh-aneh
                                try:
                                    jumlah_dipinjam = int(input("Berapa jumlah buku yang ingin di pinjam? (maks 3)\n>> "))
                                except ValueError:
                                    bersih()
                                    print("Input harus angka! (int)\n")
                                    print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
                                    continue

                                if jumlah_dipinjam > 3: # udah dibilangin lo
                                    bersih()
                                    print("Jumlah maks peminjaman adalah 3 buku sekaligus!\n")
                                    print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
                                    continue

                                # =========================
                                # = cek dan update stok
                                # =========================
                                if (df_perpus_filtered["Stok"] >= jumlah_dipinjam).any():
                                    # ngurangin stok buku
                                    df_perpus.loc[df_perpus["ISBN"] == isbn_pinjam, "Stok"] -= jumlah_dipinjam
                                    print("Buku berhasil dipinjam...")
                                    out()
                                    bersih()
                                    break
                                else: # kalo mau pinjem tapi ngelebihin stok buku masuk sini
                                    while True:
                                        print("\nStok buku tidak memadai!\n")

                                        # karena stok buku kurang, disini nanyain lagi
                                        try:
                                            confirmation = int(input("1. Ubah jumlah buku yang ingin dipinjam\n2. Kembali ke Menu Pinjam\n3. Kembali ke Menu Utama\n>> "))
                                        except ValueError: # input int, take it or leave it
                                            bersih()
                                            print("Opsi tidak di ketahui")
                                            continue
                                            
                                        if confirmation == 1:
                                            bersih()
                                            # ku tampilin lagi biar ngeh stok bukunya ada berapa
                                            print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
                                            break
                                        elif confirmation == 2: # kalau mau ganti buku
                                            bersih()
                                            perpus.pinjam()
                                        elif confirmation == 3: # sesuai nama function, balik ke home
                                            main()
                                        else: # :(
                                            bersih()
                                            print("Input tidak diketahui\n")
                                            continue
                                    bersih()
                                    print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))        
                                    continue
                            
                            # =========================
                            # = nambah daftar peminjam
                            # =========================
                            global df_peminjam
                            # kalo tadi main-main sama dataframe buku, sekarang ganti mainin dataframe orang yang pinjem
                            df_peminjam_baru = pd.DataFrame([[user,
                                                            df_perpus_filtered["Judul"].iloc[0],
                                                            df_perpus_filtered["Penulis"].iloc[0],
                                                            df_perpus_filtered["ISBN"].iloc[0],
                                                            jumlah_dipinjam]],
                                                            columns=["Peminjam", "Judul", "Penulis", "ISBN", "Jumlah_yang_dipinjam"])
                            df_peminjam = pd.concat([df_peminjam, df_peminjam_baru], ignore_index=True)
                            return df_peminjam
                        case "n": # ya ini kalo gajadi minjem
                            bersih()
                            main()
                        case _: # input cuman y sama n mas
                            bersih()
                            print("Input tidak diketahui\n")
                            print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
                            continue
            
            bersih()
            # balik ke awal setela nanyain judul sama penulis
            # masuk ke function cari dan seterusnya
            cari(df_perpus, judul, penulis)
            break
        
    
    def peminjam():
        bersih()
        welcome("Daftar Peminjam buku")
        # global df_peminjam
        # if isinstance(df_peminjam, pd.Series):
        #     df_peminjam = df_peminjam.to_frame().T  # Convert row-like Series to DataFrame
        # elif isinstance(df_peminjam, pd.DataFrame):
        #     pass  # Already good
        # else:
        #     df_peminjam = pd.DataFrame(df_peminjam)  # Fallback
        print(tabulate(df_peminjam, headers="keys", tablefmt="fancy_grid", showindex=False))
        print("\n")
        out()
        bersih()

    def hapus():
        perpus.tampil()    
        judul = input("Masukkan judul buku yang ingin dihapus : ").strip()
        global df_perpus
        hasil_cari = df_perpus[df_perpus["Judul"].str.lower().str.contains(judul, na=False)]
        bersih()
        if not hasil_cari.empty:
            print(tabulate(hasil_cari, headers="keys", tablefmt="fancy_grid", showindex=False))

            try:
                isbn_hapus = int(input("Masukkan isbn buku yang mau dihapus! (lengkap)\n>> "))
            except ValueError:
                print("ISBN harus berupa angka! (int)")
            
            filter_search = df_perpus["ISBN"] == isbn_hapus
            df_perpus_filtered =  df_perpus[filter_search]

            if not df_perpus_filtered.empty:
                bersih()
                print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
            
            else:
                print("ISBN yang anda tulis tidak sesuai\n")
                while True:
                    # kalo nulis isbn nguawor / kosong masuk sini, konfirmasi, mau masukin ulang apa nggak
                    confirmation = input("Kemabli ke menu utama? (y/n)").lower()
                    match confirmation:
                        case "y": # balik ke home
                            bersih()
                            main()
                        case "n": # balik ke menu pinjam
                            bersih()
                            perpus.hapus()
                        case _: # opsi y sama n doang bang
                            bersih()
                            print("Input tidak diketahui\n")
                            continue
            
            while True:
                confirmation = input("Anda yakin ingin menghapus buku di atas? (y/n)").lower()
                match confirmation:
                    case "y":
                        isbn_yang_dihapus = df_perpus_filtered.iloc[0]["ISBN"]
                        df_perpus =  df_perpus[df_perpus["ISBN"] != isbn_yang_dihapus]

                        print("Buku berhasil dihapus...")
                        out()
                        bersih()
                        main()
                    case "n":
                        bersih()
                        main()
                    case _:
                        bersih()
                        print("Input tidak diketahui\n")
                        print(tabulate(df_perpus_filtered, headers="keys", tablefmt="fancy_grid", showindex=False))
                        continue

        else:
            print("Buku tidak dapat ditemukan!")
            out()
            bersih()
            main()
        out()
        bersih()

# ========================================================================================
def out():
    input("Tekan Enter untuk lanjut...")    

def bersih():
    os.system("cls")

def welcome(args):
    print("=" * 59)
    print("=", args.center(55, " "), "=")
    print("=" * 59)
    
# ========================================================================================
def main():
    while True:
        title()
        try:
            print("Opsi\n1. Tambah buku\n2. Tampilkan daftar buku\n3. Hapus buku\n4. Pinjam\n5. Tampilkan daftar peminjam\n6. Keluar Program")
            opsi = int(input("Masukkan opsi : "))
        except ValueError:
            bersih()
            print("Input harus angka! (int)\n")
            continue

        match opsi:
            case 1:
                global df_perpus
                df_perpus = perpus.tambah()
                bersih()
                continue
            case 2:
                perpus.tampil()
                input("Tekan Enter untuk lanjut...")
                bersih()
                continue
            case 3:
                bersih()
                perpus.hapus()
                continue
            case 4:
                bersih()
                perpus.pinjam()
                continue
            case 5:
                bersih()
                perpus.peminjam()
                continue
            case 6:
                print("\n\nTerimakasih telah menggunakan program ini")
                print("Program akan tertutup secara otomatis")
                for i in range(3,0,-1):
                    print(i)
                    time.sleep(1)
                break
            case 99:
                pass
            case _:
                bersih()
                print("Input tidak diketahui\n")
                continue

if __name__ == "__main__":
    bersih()
    main()
