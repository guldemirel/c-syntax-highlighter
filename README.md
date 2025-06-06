
Real-Time Grammar-Based Syntax Highlighter 

1. Kullanılan Programlama Dili

Proje Python 3 programlama dili ile geliştirilmiştir. Grafiksel kullanıcı ara yüzü için pythonun kendi içerisinde bulunan Tkinter kütüphanesi kullanılmıştır.

2. Dilin Grameri (Grammar)

Proje kapsamında  C diline benzer yapılar desteklenmektedir:

stmt declaration_stmt | assign_stmt | return_stmt | if_stmt | while_stmt | for_stmt | block
declaration_stmt KEYWORD IDENTIFIER = expr ;
assign_stmt IDENTIFIER = expr ;
return_stmt return expr ;
if_stmt if (expr) stmt
while_stmt while (expr) stmt
for_stmt for (init; cond; update) stmt
block { stmt_list }
stmt_list (stmt)*
expr term ((+|-) term)*
term factor ((*|/) factor)*
factor NUMBER | IDENTIFIER | ( expr )

3. Lexical Analyzer

- Regex tabanlı çözüm uygulanmıştır.
- tokenize() ve tokenize_with_positions() adl iki farklı tokenizer fonksiyonu kullanılmıştır:
- tokenize(): Parser için sadece (tur, deger) döner.
- tokenize_with_positions(): Renklendirme için konum (start, end) bilgisi de döner.

Token Türleri:

- KEYWORD (int, return, if, while, for, vs.)
- IDENTIFIER
- NUMBER
- STRING
- CHAR
- OPERATOR
- SEPARATOR

4. Parser (Top-Down Recursive Descent)

- C dilinin temel yapıları desteklenmektedir:
- Değişken tanımı: int x = 0;
- Atama: x = 1 + 2;
- return ifadesi: return x;
- if / while yapıları ve blok { } içi ifadeler
- for döngüsü: for (int i = 0; i < 10; i = i + 1) { ... }

5. Syntax Highlighting (Sözdizimi Renklendirme)

- tokenize_with_positions() fonksiyonu ile token konumlar belirlenir.
- Tkinter Text widget'ında tag_add() ile renklendirme uygulanır.

Renkler (dark theme):
-	KEYWORD Mavi
-	IDENTIFIER Açık gri
-	NUMBER Yeşilimsi
-	OPERATOR Kırmızı
-	STRING Pembe/Kahverengi
-	CHAR Sarı
- SEPARATOR Mor

6. GUI

Tkinter kütüphanesinin özelliklerinden metin kutusu (Text widget) kullanılmıştır. Her tuşa basıldığında
- Metin tokenize edilir
- Parser kontrolü yapılır
- Renklendirme uygulanır

7. Sonuç

Bu proje, C diline benzeyen bir dil için gerçek zamanlı renklendirme ve  sözdizimi analizi gerçekleştiren bir uygulamadır. Kullanıcıya hem görsel hem mantıksal geri bildirim sunar.
## 📽️ Demo Videosu

👉 [YouTube - Proje Tanıtım ve Demo Videosu](https://www.youtube.com/watch?v=BGcB9kYx7Us)

## 📄 Makale

👉 [Medium - Proje Geliştirme Süreci ve Teknik Detaylar](https://medium.com/@sguldemirel/python-ile-c-diline-%C3%B6zg%C3%BC-ger%C3%A7ek-zamanl%C4%B1-syntax-highlighter-ve-parser-geli%C5%9Ftirmek-d057402ea416)
