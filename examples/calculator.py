print("Welcome to the calculator!")

calisitor = True

while calisitor:
    print()
    print("==== MENU ====")
    print("1. Toplama (+)")
    print("2. Çıkarma (-)")
    print("3. Çarpma (*)")
    print("4. Bölme (/)")
    print("5. Mod alma (%)")
    print("0. Çıkış")
    print("================")

    secim = input("Bir işlem seçin (0-5): ")

    # çıkış kontrolü
    if secim == "0":
        print("Hesap makinesinden çıkılıyor. Hoşça kalın!")
        calisitor = False
    else:
        if secim < "1" or secim > "5":
            print("Geçersiz işlem numarası! Lütfen tekrar deneyin.")

        #sayıları al
        s1 = float(input("Birinci sayıyı girin: "))
        s2 = float(input("İkinci sayıyı girin: "))

        print("-----------")

        if secim == "1":
            print(f"{s1} + {s2} = {s1 + s2}")

        elif secim == "2":
            print(f"{s1} - {s2} = {s1 - s2}")

        elif secim == "3":
            print(f"{s1} * {s2} = {s1 * s2}")

        elif secim == "4":           
            if s2 != 0:
                print(f"{s1} / {s2} = {s1 / s2}")
            else:
                print("Hata: Bir sayı sıfıra bölünemez!")

        elif secim == "5":
            print(f"{s1} % {s2} = {s1 % s2}")

        print("-----------")
