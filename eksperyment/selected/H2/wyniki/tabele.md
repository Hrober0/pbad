# PB2: tabele wyników (generowane)

Plik generuje `python run_h2.py report` (2026-11-25). Nie edytować ręcznie — opis i wnioski są w [../opracowanie.md](../opracowanie.md), metoda w [../ocena.md](../ocena.md).

Model `claude-sonnet-5-5`, effort `medium`, kontekst K2. Wariantów: 85, prób: 850 (powtórzeń na wariant: 10 × 85 wariantów). Tokeny: 7 965 900 wejściowych, 361 253 wyjściowych. Główna seria to części 2a–2g (84 warianty, 840 prób); część 2h to pytanie dodatkowe dopisane po dyskusji wyników.

## 1. Każdy wariant

Rodzaj dominujący (ile prób tego rodzaju), rozkład wartości z powtórzeń, mediana i zakres, liczba wierszy wyniku (mediana), w ilu próbach model podał przyjętą wartość w uwagach, ile różnych SQL.

| # | Pytanie | Rodzaj | Rozkład wartości | Mediana | Zakres | Wiersze | Ujawnił | Różne SQL |
|---|---|---|---|---|---|---|---|---|
| 1a | Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 500 ×10 | 500 m | 500–500 | 6 | 10/10 | 8 |
| 1b | Idę pieszo. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 800 ×7, 1 000 ×3 | 800 m | 800–1 000 | 19 | 10/10 | 4 |
| 1c | Jadę samochodem. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 1 000 ×9, 1 500 ×1 | 1 000 m | 1 000–1 500 | 27 | 10/10 | 8 |
| 1d | Wymień apteki niedaleko Dworca Centralnego. | PROMIEŃ (10/10) | 500 ×6, 1 000 ×4 | 500 m | 500–1 000 | 7 | 10/10 | 9 |
| 1e | Mam 10 minut do odjazdu pociągu. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 500 ×10 | 500 m | 500–500 | 7 | 10/10 | 8 |
| 2a | Wymień szpitale w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 2 000 ×10 | 2 000 m | 2 000–2 000 | 6 | 10/10 | 8 |
| 2b | Idę pieszo. Wymień szpitale w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 1 500 ×6, 2 000 ×4 | 1 500 m | 1 500–2 000 | 4 | 10/10 | 9 |
| 2c | Jadę samochodem. Wymień szpitale w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 3 000 ×10 | 3 000 m | 3 000–3 000 | 17 | 10/10 | 5 |
| 3a | Wymień apteki w pobliżu stacji Warszawa Płudy. | PROMIEŃ (10/10) | 1 000 ×8, 1 500 ×2 | 1 000 m | 1 000–1 500 | 1 | 10/10 | 9 |
| 3b | Idę pieszo. Wymień apteki w pobliżu stacji Warszawa Płudy. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 1 | 10/10 | 7 |
| 3c | Jadę samochodem. Wymień apteki w pobliżu stacji Warszawa Płudy. | PROMIEŃ (10/10) | 2 000 ×5, 1 500 ×5 | 1 750 m | 1 500–2 000 | 3 | 10/10 | 9 |
| 4a | Wymień szpitale w pobliżu stacji Warszawa Płudy. | PROMIEŃ (10/10) | 3 000 ×10 | 3 000 m | 3 000–3 000 | 0 | 10/10 | 8 |
| 4b | Idę pieszo. Wymień szpitale w pobliżu stacji Warszawa Płudy. | PROMIEŃ (10/10) | 2 000 ×6, 1 500 ×4 | 2 000 m | 1 500–2 000 | 0 | 10/10 | 10 |
| 4c | Jadę samochodem. Wymień szpitale w pobliżu stacji Warszawa Płudy. | PROMIEŃ (10/10) | 5 000 ×10 | 5 000 m | 5 000–5 000 | 0 | 9/10 | 7 |
| 5a | Wymień apteki w pobliżu stacji Tłuszcz. | PROMIEŃ (10/10) | 1 000 ×6, 1 500 ×4 | 1 000 m | 1 000–1 500 | 2 | 10/10 | 4 |
| 5b | Idę pieszo. Wymień apteki w pobliżu stacji Tłuszcz. | PROMIEŃ (10/10) | 1 000 ×6, 1 500 ×4 | 1 000 m | 1 000–1 500 | 4 | 10/10 | 9 |
| 5c | Jadę samochodem. Wymień apteki w pobliżu stacji Tłuszcz. | PROMIEŃ (10/10) | 2 000 ×5, 3 000 ×4, 1 500 ×1 | 2 000 m | 1 500–3 000 | 5 | 10/10 | 10 |
| 6a | Wymień przystanki autobusowe w pobliżu kiosku Ciasteczkowo. | PROMIEŃ (10/10) | 300 ×10 | 300 m | 300–300 | 11 | 10/10 | 9 |
| 6b | Idę pieszo. Wymień przystanki autobusowe w pobliżu kiosku Ciasteczkowo. | PROMIEŃ (10/10) | 500 ×10 | 500 m | 500–500 | 38 | 10/10 | 5 |
| 6c | Jadę samochodem. Wymień przystanki autobusowe w pobliżu kiosku Ciasteczkowo. | PROMIEŃ (10/10) | 500 ×10 | 500 m | 500–500 | 38 | 10/10 | 2 |
| 7a | Wymień przystanki autobusowe w pobliżu Lotniska Chopina. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 115 | 10/10 | 9 |
| 7b | Idę pieszo. Wymień przystanki autobusowe w pobliżu Lotniska Chopina. | PROMIEŃ (10/10) | 1 000 ×7, 800 ×3 | 1 000 m | 800–1 000 | 115 | 10/10 | 6 |
| 7c | Jadę samochodem. Wymień przystanki autobusowe w pobliżu Lotniska Chopina. | PROMIEŃ (10/10) | 1 000 ×7, 1 500 ×3 | 1 000 m | 1 000–1 500 | 115 | 10/10 | 9 |
| 8a | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | BRAK_SQL (10/10) | brak_sql ×10 | – | – | 0 | 9/10 | 1 |
| 8b | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | PROMIEŃ (10/10) | 1 250 ×10 | 1 250 m | 1 250–1 250 | 3 | 10/10 | 6 |
| 8c | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | BRAK_SQL (10/10) | brak_sql ×10 | – | – | 0 | 9/10 | 1 |
| 8d | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | PROMIEŃ (10/10) | 3 000 ×6, 3 750 ×4 | 3 000 m | 3 000–3 750 | 18 | 10/10 | 10 |
| 9a | Wymień kawiarnie w centrum Warszawy. | PROMIEŃ (10/10) | 1 500 ×8, 2 000 ×2 | 1 500 m | 1 500–2 000 | 219 | 10/10 | 6 |
| 9b | Wymień kawiarnie w centrum Płocka. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 7 | 10/10 | 3 |
| 9c | Wymień kawiarnie w centrum. | PROMIEŃ (10/10) | 1 000 ×6, 1 500 ×4 | 1 000 m | 1 000–1 500 | 151 | 10/10 | 7 |
| 10a | Wymień apteki w centrum Warszawy. | PROMIEŃ (10/10) | 1 500 ×7, 2 000 ×3 | 1 500 m | 1 500–2 000 | 40 | 10/10 | 6 |
| 10b | Wymień apteki w centrum Płocka. | PROMIEŃ (10/10) | 1 500 ×8, 1 000 ×2 | 1 500 m | 1 000–1 500 | 25 | 10/10 | 6 |
| 11a | Wymień duże parki w Warszawie. | PRÓG (10/10) | 200 000 ×8, 100 000 ×1, 300 000 ×1 | 200 000 m² | 100 000–300 000 | 14 | 10/10 | 5 |
| 11b | Wymień duże parki w Radomiu. | PRÓG (10/10) | 100 000 ×9, 50 000 ×1 | 100 000 m² | 50 000–100 000 | 0 | 10/10 | 7 |
| 11c | Wymień duże parki w Płocku. | PRÓG (10/10) | 50 000 ×9, 100 000 ×1 | 50 000 m² | 50 000–100 000 | 1 | 10/10 | 4 |
| 12a | Wymień małe parki w Warszawie. | PRÓG (10/10) | 10 000 ×10 | 10 000 m² | 10 000–10 000 | 239 | 10/10 | 6 |
| 12b | Wymień małe parki w Radomiu. | PRÓG (10/10) | 10 000 ×10 | 10 000 m² | 10 000–10 000 | 51 | 10/10 | 5 |
| 12c | Wymień małe parki w Płocku. | PRÓG (10/10) | 10 000 ×10 | 10 000 m² | 10 000–10 000 | 19 | 10/10 | 6 |
| 13a | Jak daleko w linii prostej w metrach jest z Łazienek do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 2 778.4 ×8, 2 041.5 ×2 | 2 778.4 m | 2 041.5–2 778.4 | 1 | 8/10 | 8 |
| 13b | Jak daleko w linii prostej w metrach jest z Łazienek Królewskich do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 2 041.5 ×6, 2 778.4 ×3, 2 619.4 ×1 | 2 041.5 m | 2 041.5–2 778.4 | 1 | 3/10 | 8 |
| 14a | Jak daleko w linii prostej w metrach jest z Łazienek do Pola Mokotowskiego? | ODLEGŁOŚĆ (10/10) | 753.7 ×10 | 753.7 m | 753.7–753.7 | 1 | 4/10 | 1 |
| 14b | Jak daleko w linii prostej w metrach jest z Łazienek Królewskich do Pola Mokotowskiego? | ODLEGŁOŚĆ (10/10) | 753.7 ×10 | 753.7 m | 753.7–753.7 | 1 | 0/10 | 1 |
| 15a | Jak daleko w linii prostej w metrach jest od pomnika Chopina do Pałacu Kultury i Nauki? | PUSTY_WYNIK (8/10) | pusty_wynik ×8, 93 072.3 ×1, 51 581.6 ×1 | – | – | 0 | 10/10 | 6 |
| 15b | Jak daleko w linii prostej w metrach jest od pomnika Chopina w Łazienkach do Pałacu Kultury i Nauki? | PUSTY_WYNIK (10/10) | pusty_wynik ×10 | – | – | 0 | 5/10 | 10 |
| 16a | Jak daleko w linii prostej w metrach jest od Syrenki Warszawskiej do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (9/10) | 837.2 ×5, 706.3 ×2, pusty_wynik ×1, 1 934.8 ×1, 31 754.6 ×1 | 837.2 m | 706.3–31 754.6 | 1 | 2/10 | 10 |
| 16b | Jak daleko w linii prostej w metrach jest od pomnika Syrenki nad Wisłą do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 837.2 ×6, 706.3 ×4 | 837.2 m | 706.3–837.2 | 1 | 1/10 | 10 |
| 17a | Jak daleko w linii prostej w metrach jest od pomnika Kopernika do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (9/10) | 1 066.9 ×6, 949.3 ×3, pusty_wynik ×1 | 1 066.9 m | 949.3–1 066.9 | 1 | 8/10 | 10 |
| 17b | Jak daleko w linii prostej w metrach jest od pomnika Mikołaja Kopernika na Krakowskim Przedmieściu do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 1 066.9 ×6, 1 089.7 ×2, 949.3 ×2 | 1 066.9 m | 949.3–1 089.7 | 1 | 2/10 | 10 |
| 18 | Jak daleko w linii prostej w metrach jest od Kolumny Zygmunta do Pałacu Kultury i Nauki? | PUSTY_WYNIK (10/10) | pusty_wynik ×10 | – | – | 0 | 6/10 | 8 |
| 19 | Jak daleko w linii prostej w metrach jest od palmy na rondzie de Gaulle'a do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (5/10) | 1 018.5 ×3, pusty_wynik ×3, brak_sql ×2, 997.7 ×1, 3 889 ×1 | 1 018.5 m | 997.7–3 889 | 1 | 3/10 | 9 |
| 20 | Jak daleko w linii prostej w metrach jest od pomnika Małego Powstańca do Pałacu Kultury i Nauki? | PUSTY_WYNIK (9/10) | pusty_wynik ×9, 1 969.1 ×1 | – | – | 0 | 2/10 | 9 |
| 21a | Jak daleko w metrach jest od Pałacu Kultury i Nauki do najbliższej stacji metra i jak się ona nazywa? | ODLEGŁOŚĆ (10/10) | 147 ×5, 146.6 ×4, 311.5 ×1 | 147 m | 146.6–311.5 | 1 | 10/10 | 10 |
| 21b | Jak daleko w metrach jest od Łazienek Królewskich do najbliższej stacji metra i jak się ona nazywa? | ODLEGŁOŚĆ (10/10) | 797.1 ×9, 797 ×1 | 797.1 m | 797–797.1 | 1 | 10/10 | 3 |
| 22a | Ile kawiarni w Warszawie jest w odległości do 200 metrów od stacji metra? | LICZBA (10/10) | 72 ×10 | 72 szt. | 72–72 | 1 | 10/10 | 8 |
| 22b | Wymień kawiarnie w pobliżu stacji metra. | PROMIEŃ (10/10) | 300 ×10 | 300 m | 300–300 | 142 | 10/10 | 5 |
| 22c | Wymień kawiarnie w pobliżu stacji metra Centrum. | PROMIEŃ (10/10) | 500 ×8, 300 ×2 | 500 m | 300–500 | 42.5 | 10/10 | 9 |
| 23a | Wymień apteki w pobliżu stacji Radom Główny. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 15 | 10/10 | 6 |
| 23b | Wymień apteki w pobliżu stacji Siedlce. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 5 | 10/10 | 8 |
| 23c | Wymień apteki w pobliżu stacji Celestynów. | PROMIEŃ (10/10) | 2 000 ×4, 1 500 ×4, 1 000 ×2 | 1 500 m | 1 000–2 000 | 3 | 10/10 | 10 |
| 23d | Wymień apteki w pobliżu stacji Krusze. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 0 | 10/10 | 9 |
| 24 | Jadę samochodem. Wymień apteki w pobliżu stacji Krusze. | PROMIEŃ (10/10) | 2 000 ×8, 1 500 ×1, 3 000 ×1 | 2 000 m | 1 500–3 000 | 0 | 10/10 | 9 |
| 25a | Wymień apteki bardzo blisko Dworca Centralnego. | PROMIEŃ (10/10) | 300 ×9, 500 ×1 | 300 m | 300–500 | 3 | 10/10 | 7 |
| 25b | Wymień apteki w okolicy Dworca Centralnego. | PROMIEŃ (10/10) | 500 ×10 | 500 m | 500–500 | 6 | 10/10 | 6 |
| 25c | Wymień apteki w zasięgu krótkiego spaceru od Dworca Centralnego. | PROMIEŃ (10/10) | 500 ×5, 800 ×5 | 650 m | 500–800 | 12.5 | 10/10 | 10 |
| 25d | Wymień apteki rzut beretem od Dworca Centralnego. | PROMIEŃ (10/10) | 500 ×7, 300 ×3 | 500 m | 300–500 | 6 | 10/10 | 5 |
| 26 | Wymień najbliższe apteki od Dworca Centralnego. | K_NAJBLIŻSZYCH (10/10) | 10 ×10 | 10 szt. | 10–10 | 10 | 9/10 | 5 |
| 27a | Poruszam się na wózku inwalidzkim. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 1 000 ×9, 500 ×1 | 1 000 m | 500–1 000 | 26 | 10/10 | 2 |
| 27b | Jestem z małym dzieckiem. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 1 000 ×7, 800 ×2, 700 ×1 | 1 000 m | 700–1 000 | 27 | 10/10 | 7 |
| 27c | Jestem na rowerze. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 1 500 ×10 | 1 500 m | 1 500–1 500 | 43 | 10/10 | 6 |
| 27d | Pilnie potrzebuję leków. Wymień apteki w pobliżu Dworca Centralnego. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 27 | 10/10 | 5 |
| 29a | Wymień apteki w pobliżu stacji Warszawa Centralna. | PROMIEŃ (10/10) | 500 ×9, 1 000 ×1 | 500 m | 500–1 000 | 6 | 10/10 | 6 |
| 29b | Jadę samochodem. Wymień apteki w pobliżu stacji Warszawa Centralna. | PROMIEŃ (10/10) | 1 000 ×10 | 1 000 m | 1 000–1 000 | 26.5 | 10/10 | 7 |
| 28a | List pharmacies near Warsaw Central railway station. | PROMIEŃ (10/10) | 500 ×10 | 500 m | 500–500 | 6 | 10/10 | 4 |
| 28b | I'm driving. List pharmacies near Warsaw Central railway station. | PROMIEŃ (10/10) | 500 ×6, 1 000 ×4 | 500 m | 500–1 000 | 7 | 10/10 | 6 |
| 30 | Jak daleko w linii prostej w metrach jest od pomnika Chopina do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 895 ×3, 1 038 ×3, 2 423.5 ×1, 93 222 ×1, 1 009.4 ×1, 1 032 ×1 | 1 035 m | 895–93 222 | 1 | 3/10 | 10 |
| 31 | Jak daleko w linii prostej w metrach jest od pomnika Chopina w Łazienkach do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 2 434 ×2, 51 582 ×1, 2 434.2 ×1, 2 423.5 ×1, 1 032 ×1, 51 708.5 ×1, 2 264 ×1, 51 709 ×1, 93 072 ×1 | 2 434.1 m | 1 032–93 072 | 1 | 2/10 | 10 |
| 32 | Jak daleko w linii prostej w metrach jest od Syrenki Warszawskiej do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 2 055 ×2, 837 ×2, 2 054.9 ×2, 1 900 ×1, 2 122.6 ×1, 834 ×1, 1 935 ×1 | 1 995.0 m | 834–2 122.6 | 1 | 3/10 | 10 |
| 33 | Jak daleko w linii prostej w metrach jest od pomnika Syrenki nad Wisłą do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 1 893 ×4, 706.3 ×2, 2 054.9 ×2, 2 055 ×1, 64 306 ×1 | 1 893 m | 706.3–64 306 | 1 | 1/10 | 10 |
| 34 | Jak daleko w linii prostej w metrach jest od pomnika Kopernika do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 949.3 ×7, 949 ×2, 1 089.7 ×1 | 949.3 m | 949–1 089.7 | 1 | 2/10 | 10 |
| 35 | Jak daleko w linii prostej w metrach jest od Kolumny Zygmunta do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 1 801.3 ×4, 1 636 ×4, 1 801 ×2 | 1 801 m | 1 636–1 801.3 | 1 | 7/10 | 10 |
| 36 | Jak daleko w linii prostej w metrach jest od palmy na rondzie de Gaulle'a do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 2 859.4 ×2, 880.8 ×2, 881 ×2, 1 018.5 ×1, 2 973.9 ×1, 1 261.5 ×1, 96 323.1 ×1 | 1 140 m | 880.8–96 323.1 | 1 | 2/10 | 10 |
| 37 | Jak daleko w linii prostej w metrach jest od pomnika Małego Powstańca do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (9/10) | 2 226 ×3, 2 420 ×2, 1 969 ×1, 1 965 ×1, 2 226.1 ×1, 2 420.2 ×1, pusty_wynik ×1 | 2 226 m | 1 965–2 420.2 | 1 | 2/10 | 10 |
| 38 | Jak daleko w linii prostej w metrach jest z Łazienek do Pałacu Kultury i Nauki? | ODLEGŁOŚĆ (10/10) | 2 778.4 ×6, 2 778 ×2, 2 041.5 ×1, 2 193.6 ×1 | 2 778.4 m | 2 041.5–2 778.4 | 1 | 8/10 | 10 |
| 39 | Jak daleko w metrach jest od Pałacu Kultury i Nauki do najbliższej stacji metra i jak się ona nazywa? | ODLEGŁOŚĆ (10/10) | 146.6 ×6, 147 ×3, 299.8 ×1 | 146.6 m | 146.6–299.8 | 1 | 10/10 | 8 |
| 40 | Jak daleko w linii prostej w metrach jest od metra do Gmachu Głównego Politechniki Warszawskiej? | PUSTY_WYNIK (10/10) | pusty_wynik ×10 | – | – | 0 | 10/10 | 9 |

## 2. Porównania kierunkowe (czynniki S, M, O)

`ROŚNIE`: mediana B ≥ 1.25 × mediana A; `MALEJE`: mediana B ≤ mediana A / 1.25; `BEZ_ZMIANY`: pomiędzy. „Zakresy rozłączne”: każda wartość B jest większa (albo mniejsza) od każdej wartości A. Wariant jest niestabilny, gdy mniej niż 60% prób ma ten sam rodzaj interpretacji z odczytaną wartością (np. model odmawia).

### S: sytuacja pytającego

| A | B | Mediana A | Mediana B | B/A | Zakresy rozłączne | Wynik |
|---|---|---|---|---|---|---|
| 1b | 1c | 800 | 1 000 | 1.25 | nie | ROŚNIE |
| 2b | 2c | 1 500 | 3 000 | 2.00 | tak | ROŚNIE |
| 3b | 3c | 1 000 | 1 750 | 1.75 | tak | ROŚNIE |
| 4b | 4c | 2 000 | 5 000 | 2.50 | tak | ROŚNIE |
| 5b | 5c | 1 000 | 2 000 | 2.00 | nie | ROŚNIE |
| 6b | 6c | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| 7b | 7c | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| 8b | 8d | 1 250 | 3 000 | 2.40 | tak | ROŚNIE |
| 8d | 8c | 3 000 | – | – | – | NIESTABILNY (niestabilny: 8c) |

### M: miejsce

| A | B | Mediana A | Mediana B | B/A | Zakresy rozłączne | Wynik |
|---|---|---|---|---|---|---|
| 1a | 3a | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 1b | 3b | 800 | 1 000 | 1.25 | nie | ROŚNIE |
| 1c | 3c | 1 000 | 1 750 | 1.75 | nie | ROŚNIE |
| 1a | 5a | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 1b | 5b | 800 | 1 000 | 1.25 | nie | ROŚNIE |
| 1c | 5c | 1 000 | 2 000 | 2.00 | nie | ROŚNIE |
| 2a | 4a | 2 000 | 3 000 | 1.50 | tak | ROŚNIE |
| 2b | 4b | 1 500 | 2 000 | 1.33 | nie | ROŚNIE |
| 2c | 4c | 3 000 | 5 000 | 1.67 | tak | ROŚNIE |

### O: rodzaj i skala obiektu

| A | B | Mediana A | Mediana B | B/A | Zakresy rozłączne | Wynik |
|---|---|---|---|---|---|---|
| 1a | 2a | 500 | 2 000 | 4.00 | tak | ROŚNIE |
| 1b | 2b | 800 | 1 500 | 1.88 | tak | ROŚNIE |
| 1c | 2c | 1 000 | 3 000 | 3.00 | tak | ROŚNIE |
| 3a | 4a | 1 000 | 3 000 | 3.00 | tak | ROŚNIE |
| 3b | 4b | 1 000 | 2 000 | 2.00 | tak | ROŚNIE |
| 3c | 4c | 1 750 | 5 000 | 2.86 | tak | ROŚNIE |
| 6a | 7a | 300 | 1 000 | 3.33 | tak | ROŚNIE |
| 6b | 7b | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 6c | 7c | 500 | 1 000 | 2.00 | tak | ROŚNIE |

### Podsumowanie czynników

| Czynnik | Porównań | Rozstrzygniętych | Rośnie | w tym zakresy rozłączne | Bez zmiany | Maleje | Odpadło | Opis |
|---|---|---|---|---|---|---|---|---|
| S: sytuacja pytającego | 9 | 8 | 6 | 4 | 2 | 0 | 1 | **wyraźny wpływ** |
| M: miejsce | 9 | 9 | 9 | 4 | 0 | 0 | 0 | **wyraźny wpływ** |
| O: rodzaj i skala obiektu | 9 | 9 | 9 | 9 | 0 | 0 | 0 | **wyraźny wpływ** |

### Wrażliwość na próg ilorazu

| Czynnik | iloraz ≥ 1.25 | iloraz ≥ 1.5 | iloraz ≥ 2.0 |
|---|---|---|---|
| S: sytuacja pytającego | 6/8 — wyraźny wpływ | 5/8 — częściowy wpływ | 4/8 — częściowy wpływ |
| M: miejsce | 9/9 — wyraźny wpływ | 6/9 — wyraźny wpływ | 3/9 — częściowy wpływ |
| O: rodzaj i skala obiektu | 9/9 — wyraźny wpływ | 9/9 — wyraźny wpływ | 8/9 — wyraźny wpływ |

## 3. Porównania bez oczekiwanego kierunku (w tym część 2f)

| Porównanie | A | B | Mediana A | Mediana B | B/A | Zakresy rozłączne | Wynik |
|---|---|---|---|---|---|---|---|
| „w pobliżu” a „niedaleko” | 1a | 1d | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| sytuacja wywnioskowana (pośpiech) | 1a | 1e | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| sytuacja wywnioskowana (pośpiech) | 1b | 1e | 800 | 500 | 0.62 | tak | MALEJE |
| domyślny środek transportu w 15 minut | 8a | 8b | – | 1 250 | – | – | NIESTABILNY (niestabilny: 8a) |
| domyślny środek transportu w 15 minut | 8a | 8d | – | 3 000 | – | – | NIESTABILNY (niestabilny: 8a) |
| domyślny środek transportu w 15 minut | 8a | 8c | – | – | – | – | NIESTABILNY (niestabilny: 8a, 8c) |
| brak informacji → pieszo | 1a | 1b | 500 | 800 | 1.60 | tak | ROŚNIE |
| brak informacji → pieszo | 2a | 2b | 2 000 | 1 500 | 0.75 | nie | MALEJE |
| brak informacji → pieszo | 3a | 3b | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| brak informacji → pieszo | 4a | 4b | 3 000 | 2 000 | 0.67 | tak | MALEJE |
| brak informacji → pieszo | 5a | 5b | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| brak informacji → pieszo | 6a | 6b | 300 | 500 | 1.67 | tak | ROŚNIE |
| brak informacji → pieszo | 7a | 7b | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| brak informacji → samochodem | 1a | 1c | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| brak informacji → samochodem | 2a | 2c | 2 000 | 3 000 | 1.50 | tak | ROŚNIE |
| brak informacji → samochodem | 3a | 3c | 1 000 | 1 750 | 1.75 | nie | ROŚNIE |
| brak informacji → samochodem | 4a | 4c | 3 000 | 5 000 | 1.67 | tak | ROŚNIE |
| brak informacji → samochodem | 5a | 5c | 1 000 | 2 000 | 2.00 | nie | ROŚNIE |
| brak informacji → samochodem | 6a | 6c | 300 | 500 | 1.67 | tak | ROŚNIE |
| brak informacji → samochodem | 7a | 7c | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| „centrum” w różnych miastach | 9a | 9b | 1 500 | 1 000 | 0.67 | tak | MALEJE |
| „centrum” w różnych miastach | 9a | 9c | 1 500 | 1 000 | 0.67 | nie | MALEJE |
| „centrum” w różnych miastach | 10a | 10b | 1 500 | 1 500 | 1.00 | nie | BEZ_ZMIANY |
| „centrum” w różnych miastach | 9a | 10a | 1 500 | 1 500 | 1.00 | nie | BEZ_ZMIANY |
| „centrum” w różnych miastach | 9b | 10b | 1 000 | 1 500 | 1.50 | nie | ROŚNIE |
| próg „duży”: Warszawa → mniejsze miasto | 11a | 11b | 200 000 | 100 000 | 0.50 | nie | MALEJE |
| próg „duży”: Warszawa → mniejsze miasto | 11a | 11c | 200 000 | 50 000 | 0.25 | nie | MALEJE |
| próg „duży”: Warszawa → mniejsze miasto | 11b | 11c | 100 000 | 50 000 | 0.50 | nie | MALEJE |
| próg „mały”: Warszawa → mniejsze miasto | 12a | 12b | 10 000 | 10 000 | 1.00 | nie | BEZ_ZMIANY |
| próg „mały”: Warszawa → mniejsze miasto | 12a | 12c | 10 000 | 10 000 | 1.00 | nie | BEZ_ZMIANY |
| próg „mały”: Warszawa → mniejsze miasto | 12b | 12c | 10 000 | 10 000 | 1.00 | nie | BEZ_ZMIANY |
| „mały” → „duży” w tym samym mieście | 12a | 11a | 10 000 | 200 000 | 20.00 | tak | ROŚNIE |
| „mały” → „duży” w tym samym mieście | 12b | 11b | 10 000 | 100 000 | 10.00 | tak | ROŚNIE |
| „mały” → „duży” w tym samym mieście | 12c | 11c | 10 000 | 50 000 | 5.00 | tak | ROŚNIE |
| 2f: gradient miejscowości (od Warszawy) | 1a | 23a | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 2f: gradient miejscowości (od Warszawy) | 1a | 23b | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 2f: gradient miejscowości (od Warszawy) | 1a | 5a | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 2f: gradient miejscowości (od Warszawy) | 1a | 23c | 500 | 1 500 | 3.00 | tak | ROŚNIE |
| 2f: gradient miejscowości (od Warszawy) | 1a | 23d | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 2f: gradient miejscowości (kolejne kroki) | 23a | 23b | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| 2f: gradient miejscowości (kolejne kroki) | 23b | 5a | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| 2f: gradient miejscowości (kolejne kroki) | 5a | 23c | 1 000 | 1 500 | 1.50 | nie | ROŚNIE |
| 2f: gradient miejscowości (kolejne kroki) | 23c | 23d | 1 500 | 1 000 | 0.67 | nie | MALEJE |
| 2f: wieś, samochodem | 23d | 24 | 1 000 | 2 000 | 2.00 | tak | ROŚNIE |
| 2f: wieś, samochodem | 1c | 24 | 1 000 | 2 000 | 2.00 | nie | ROŚNIE |
| 2f: siła określenia (od „w pobliżu”) | 1a | 25a | 500 | 300 | 0.60 | nie | MALEJE |
| 2f: siła określenia (od „w pobliżu”) | 1a | 25b | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| 2f: siła określenia (od „w pobliżu”) | 1a | 25c | 500 | 650 | 1.30 | nie | ROŚNIE |
| 2f: siła określenia (od „w pobliżu”) | 1a | 25d | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| 2f: sytuacja wywnioskowana (od braku informacji) | 1a | 27a | 500 | 1 000 | 2.00 | nie | ROŚNIE |
| 2f: sytuacja wywnioskowana (od braku informacji) | 1a | 27b | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 2f: sytuacja wywnioskowana (od braku informacji) | 1a | 27c | 500 | 1 500 | 3.00 | tak | ROŚNIE |
| 2f: sytuacja wywnioskowana (od braku informacji) | 1a | 27d | 500 | 1 000 | 2.00 | tak | ROŚNIE |
| 2f: sytuacja wywnioskowana (od „pieszo”) | 1b | 27a | 800 | 1 000 | 1.25 | nie | ROŚNIE |
| 2f: sytuacja wywnioskowana (od „pieszo”) | 1b | 27b | 800 | 1 000 | 1.25 | nie | ROŚNIE |
| 2f: sytuacja wywnioskowana (od „pieszo”) | 1b | 27c | 800 | 1 500 | 1.88 | tak | ROŚNIE |
| 2f: sytuacja wywnioskowana (od „pieszo”) | 1b | 27d | 800 | 1 000 | 1.25 | nie | ROŚNIE |
| 2f: język pytania | 1a | 28a | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| 2f: język pytania | 1c | 28b | 1 000 | 500 | 0.50 | nie | MALEJE |
| 2f: język pytania | 28a | 28b | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| 2f: kontrola sformułowania („Dworzec Centralny” → „stacja Warszawa Centralna”) | 1a | 29a | 500 | 500 | 1.00 | nie | BEZ_ZMIANY |
| 2f: kontrola sformułowania („Dworzec Centralny” → „stacja Warszawa Centralna”) | 1c | 29b | 1 000 | 1 000 | 1.00 | nie | BEZ_ZMIANY |
| 2f: gradient od „stacji Warszawa Centralna” | 29a | 23a | 500 | 1 000 | 2.00 | nie | ROŚNIE |
| 2f: gradient od „stacji Warszawa Centralna” | 29a | 23b | 500 | 1 000 | 2.00 | nie | ROŚNIE |
| 2f: gradient od „stacji Warszawa Centralna” | 29a | 23d | 500 | 1 000 | 2.00 | nie | ROŚNIE |
| 2f: gradient od „stacji Warszawa Centralna” | 29a | 29b | 500 | 1 000 | 2.00 | nie | ROŚNIE |

## 4. Część 2b: przyjęta prędkość

„Promień / 15 min” to prędkość wyliczona z promienia w linii prostej. Model czasem zmniejsza promień o współczynnik krętości dróg, więc ważniejsza jest prędkość, którą sam podaje w uwagach.

| # | Wariant | Rozkład promienia | Promień / 15 min (km/h) | Prędkość podana w uwagach (km/h) | Uwagi wspominają krętość dróg |
|---|---|---|---|---|---|
| 8a | Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | brak_sql ×10 | – | – | 0/10 |
| 8b | Idę pieszo. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | 1 250 ×10 | 5.0 ×10 | 5 ×10 | 0/10 |
| 8d | Jadę rowerem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | 3 000 ×6, 3 750 ×4 | 12.0 ×6, 15.0 ×4 | 15 ×10 | 6/10 |
| 8c | Jadę samochodem. Wymień szpitale, do których dotrę w 15 minut od Dworca Centralnego. | brak_sql ×10 | – | – | 0/10 |

## 5. Część 2f: gradient miejscowości

Apteki „w pobliżu stacji …”. Liczba aptek wokół stacji: [../pytania.md](../pytania.md#część-2f-dodatkowe-kontrasty-eksploracja--16-wariantów).

| # | Stacja | Rozkład promienia | Mediana | Wiersze (mediana) | Prób z pustym wynikiem |
|---|---|---|---|---|---|
| 1a | Dworzec Centralny | 500 ×10 | 500 | 6 | 0/10 |
| 29a | stacja Warszawa Centralna | 500 ×9, 1 000 ×1 | 500 | 6 | 0/10 |
| 29b | stacja Warszawa Centralna, samochodem | 1 000 ×10 | 1 000 | 26.5 | 0/10 |
| 23a | Radom Główny | 1 000 ×10 | 1 000 | 15 | 0/10 |
| 23b | Siedlce | 1 000 ×10 | 1 000 | 5 | 0/10 |
| 5a | Tłuszcz | 1 000 ×6, 1 500 ×4 | 1 000 | 2 | 0/10 |
| 23c | Celestynów | 2 000 ×4, 1 500 ×4, 1 000 ×2 | 1 500 | 3 | 0/10 |
| 23d | Krusze | 1 000 ×10 | 1 000 | 0 | 10/10 |
| 24 | Krusze, samochodem | 2 000 ×8, 1 500 ×1, 3 000 ×1 | 2 000 | 0 | 10/10 |

## 6. Części 2c i 2d

| # | Pytanie | Rozkład wartości | Wiersze (mediana) | Prób z pustym wynikiem |
|---|---|---|---|---|
| 9a | Wymień kawiarnie w centrum Warszawy. | 1 500 ×8, 2 000 ×2 (m) | 219 | 0/10 |
| 9b | Wymień kawiarnie w centrum Płocka. | 1 000 ×10 (m) | 7 | 0/10 |
| 9c | Wymień kawiarnie w centrum. | 1 000 ×6, 1 500 ×4 (m) | 151 | 0/10 |
| 10a | Wymień apteki w centrum Warszawy. | 1 500 ×7, 2 000 ×3 (m) | 40 | 0/10 |
| 10b | Wymień apteki w centrum Płocka. | 1 500 ×8, 1 000 ×2 (m) | 25 | 0/10 |
| 11a | Wymień duże parki w Warszawie. | 200 000 ×8, 100 000 ×1, 300 000 ×1 (m²) | 14 | 0/10 |
| 11b | Wymień duże parki w Radomiu. | 100 000 ×9, 50 000 ×1 (m²) | 0 | 9/10 |
| 11c | Wymień duże parki w Płocku. | 50 000 ×9, 100 000 ×1 (m²) | 1 | 1/10 |
| 12a | Wymień małe parki w Warszawie. | 10 000 ×10 (m²) | 239 | 0/10 |
| 12b | Wymień małe parki w Radomiu. | 10 000 ×10 (m²) | 51 | 0/10 |
| 12c | Wymień małe parki w Płocku. | 10 000 ×10 (m²) | 19 | 0/10 |

## 7. Część 2e: rozpoznanie obiektu

Kandydaci i wartości wzorcowe: [../pytania.md](../pytania.md#kandydaci-w-bazie-i-odległości-wzorcowe).

| # | Pytanie | Rozkład wyników | Ocena obiektu |
|---|---|---|---|
| 13a | Jak daleko w linii prostej w metrach jest z Łazienek do Pałacu Kultury i Nauki? | 2 778.4 ×8, 2 041.5 ×2 | poprawny ×10 |
| 13b | Jak daleko w linii prostej w metrach jest z Łazienek Królewskich do Pałacu Kultury i Nauki? | 2 041.5 ×6, 2 778.4 ×3, 2 619.4 ×1 | poprawny ×10 |
| 14a | Jak daleko w linii prostej w metrach jest z Łazienek do Pola Mokotowskiego? | 753.7 ×10 | poprawny ×10 |
| 14b | Jak daleko w linii prostej w metrach jest z Łazienek Królewskich do Pola Mokotowskiego? | 753.7 ×10 | poprawny ×10 |
| 15a | Jak daleko w linii prostej w metrach jest od pomnika Chopina do Pałacu Kultury i Nauki? | pusty_wynik ×8, 93 072.3 ×1, 51 581.6 ×1 | pusty ×8, duża_pomyłka ×2 |
| 15b | Jak daleko w linii prostej w metrach jest od pomnika Chopina w Łazienkach do Pałacu Kultury i Nauki? | pusty_wynik ×10 | pusty ×10 |
| 16a | Jak daleko w linii prostej w metrach jest od Syrenki Warszawskiej do Pałacu Kultury i Nauki? | 837.2 ×5, 706.3 ×2, pusty_wynik ×1, 1 934.8 ×1, 31 754.6 ×1 | pomyłka ×7, duża_pomyłka ×2, pusty ×1 |
| 16b | Jak daleko w linii prostej w metrach jest od pomnika Syrenki nad Wisłą do Pałacu Kultury i Nauki? | 837.2 ×6, 706.3 ×4 | pomyłka ×10 |
| 17a | Jak daleko w linii prostej w metrach jest od pomnika Kopernika do Pałacu Kultury i Nauki? | 1 066.9 ×6, 949.3 ×3, pusty_wynik ×1 | poprawny ×9, pusty ×1 |
| 17b | Jak daleko w linii prostej w metrach jest od pomnika Mikołaja Kopernika na Krakowskim Przedmieściu do Pałacu Kultury i Nauki? | 1 066.9 ×6, 1 089.7 ×2, 949.3 ×2 | poprawny ×10 |
| 18 | Jak daleko w linii prostej w metrach jest od Kolumny Zygmunta do Pałacu Kultury i Nauki? | pusty_wynik ×10 | pusty ×10 |
| 19 | Jak daleko w linii prostej w metrach jest od palmy na rondzie de Gaulle'a do Pałacu Kultury i Nauki? | 1 018.5 ×3, pusty_wynik ×3, brak_sql ×2, 997.7 ×1, 3 889 ×1 | poprawny ×4, pusty ×3, brak_sql ×2, duża_pomyłka ×1 |
| 20 | Jak daleko w linii prostej w metrach jest od pomnika Małego Powstańca do Pałacu Kultury i Nauki? | pusty_wynik ×9, 1 969.1 ×1 | pusty ×9, poprawny ×1 |
| 21a | Jak daleko w metrach jest od Pałacu Kultury i Nauki do najbliższej stacji metra i jak się ona nazywa? | 147 ×5, 146.6 ×4, 311.5 ×1 | poprawny ×10 |
| 21b | Jak daleko w metrach jest od Łazienek Królewskich do najbliższej stacji metra i jak się ona nazywa? | 797.1 ×9, 797 ×1 | poprawny ×10 |
| 22a | Ile kawiarni w Warszawie jest w odległości do 200 metrów od stacji metra? | 72 ×10 | poprawny ×10 |
| 22b | Wymień kawiarnie w pobliżu stacji metra. | promień: 300 ×10; wiersze: 142 ×8, 143 ×2 | – |
| 22c | Wymień kawiarnie w pobliżu stacji metra Centrum. | promień: 500 ×8, 300 ×2; wiersze: 43 ×5, 42 ×3, 15 ×2 | – |

### Przyczyny pustych wyników w 2e

Diagnoza automatyczna: każde podzapytanie wykonane osobno; podajemy to, które zwraca 0 wierszy.

| # | Diagnoza | Prób |
|---|---|---|
| 15a | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument', name %Chopin%) | 6 |
| 15a | 0 wierszy: PKiN (gis_osm_pois_free, fclass 'attraction', name %Pałac Kultury i Nauki%) | 1 |
| 15a | 0 wierszy: PKiN (gis_osm_pois_free, fclass 'attraction', name %Pałac Kultury%) | 1 |
| 15b | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument', name %Chopin%) | 10 |
| 16a | 0 wierszy: PKiN (gis_osm_pois_free, fclass 'attraction', name %Pałac Kultury%) | 1 |
| 17a | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument', name %Kopernik%) | 1 |
| 18 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument', name %Kolumna Zygmunta%) | 5 |
| 18 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument','memorial','attraction', name %Kolumna Zygmunta%) | 3 |
| 18 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument','memorial','attraction','viewpoint', name %Kolumna Zygmunta%) | 2 |
| 19 | 0 wierszy: PKiN (gis_osm_pois_free, fclass 'attraction', name %Pałac Kultury i Nauki%) | 2 |
| 19 | Nie da się rzetelnie wyrazić tego pytania jednym zapytaniem. Palma na rondzie de Gaulle'a nie jest osobnym typem obiektu w bazie (gis_osm_natural_free ma tylko  | 1 |
| 19 | Nie da się rzetelnie odpowiedzieć na to pytanie jednym zapytaniem. Baza nie zawiera obiektu 'palma na rondzie de Gaulle'a' (tabela natural zawiera tylko drzewa  | 1 |
| 19 | wynik NULL; 0 wierszy: PKiN (gis_osm_pois_free, fclass 'attraction', name %Pałac Kultury%) | 1 |
| 20 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument','memorial', name %Małego Powstańca%) | 3 |
| 20 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument', name %Małego Powstańca%) | 2 |
| 20 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'memorial','monument', name %Małego Powstańca%) | 1 |
| 20 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'memorial', name %Małego Powstańca%) | 1 |
| 20 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'memorial', name %Ma_ego Powsta_ca%) | 1 |
| 20 | 0 wierszy: obiekt z pytania (gis_osm_pois_free, fclass 'monument', name %Ma_ego Powsta_ca%) | 1 |

### Wybrany kandydat w każdej próbie

| # | Próba | Wynik | Kandydat | Ocena |
|---|---|---|---|---|
| 13a | 1 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13a | 2 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13a | 3 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 4 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 5 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 6 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 7 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 8 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 9 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13a | 10 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13b | 1 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13b | 2 | 2 619.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN poligon | poprawny |
| 13b | 3 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13b | 4 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13b | 5 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13b | 6 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13b | 7 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13b | 8 | 2 041.5 | Łazienki Królewskie [landuse_a, park, Warszawa] geometria → PKiN poligon | poprawny |
| 13b | 9 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 13b | 10 | 2 778.4 | Łazienki Królewskie [landuse_a, park, Warszawa] środek → PKiN środek poligonu | poprawny |
| 14a | 1 | 753.7 | między obrysami parków | poprawny |
| 14a | 2 | 753.7 | między obrysami parków | poprawny |
| 14a | 3 | 753.7 | między obrysami parków | poprawny |
| 14a | 4 | 753.7 | między obrysami parków | poprawny |
| 14a | 5 | 753.7 | między obrysami parków | poprawny |
| 14a | 6 | 753.7 | między obrysami parków | poprawny |
| 14a | 7 | 753.7 | między obrysami parków | poprawny |
| 14a | 8 | 753.7 | między obrysami parków | poprawny |
| 14a | 9 | 753.7 | między obrysami parków | poprawny |
| 14a | 10 | 753.7 | między obrysami parków | poprawny |
| 14b | 1 | 753.7 | między obrysami parków | poprawny |
| 14b | 2 | 753.7 | między obrysami parków | poprawny |
| 14b | 3 | 753.7 | między obrysami parków | poprawny |
| 14b | 4 | 753.7 | między obrysami parków | poprawny |
| 14b | 5 | 753.7 | między obrysami parków | poprawny |
| 14b | 6 | 753.7 | między obrysami parków | poprawny |
| 14b | 7 | 753.7 | między obrysami parków | poprawny |
| 14b | 8 | 753.7 | między obrysami parków | poprawny |
| 14b | 9 | 753.7 | między obrysami parków | poprawny |
| 14b | 10 | 753.7 | między obrysami parków | poprawny |
| 15a | 1 | – | brak wyniku | pusty |
| 15a | 2 | – | brak wyniku | pusty |
| 15a | 3 | – | brak wyniku | pusty |
| 15a | 4 | – | brak wyniku | pusty |
| 15a | 5 | – | brak wyniku | pusty |
| 15a | 6 | – | brak wyniku | pusty |
| 15a | 7 | – | brak wyniku | pusty |
| 15a | 8 | – | brak wyniku | pusty |
| 15a | 9 | 93 072.3 | Pomnik Fryderyka Chopina [pois, memorial, Radom] geometria → PKiN poligon | duża_pomyłka |
| 15a | 10 | 51 581.6 | Pomnik Fryderka Chopina [pois, memorial, powiat sochaczewski] geometria → PKiN poligon | duża_pomyłka |
| 15b | 1 | – | brak wyniku | pusty |
| 15b | 2 | – | brak wyniku | pusty |
| 15b | 3 | – | brak wyniku | pusty |
| 15b | 4 | – | brak wyniku | pusty |
| 15b | 5 | – | brak wyniku | pusty |
| 15b | 6 | – | brak wyniku | pusty |
| 15b | 7 | – | brak wyniku | pusty |
| 15b | 8 | – | brak wyniku | pusty |
| 15b | 9 | – | brak wyniku | pusty |
| 15b | 10 | – | brak wyniku | pusty |
| 16a | 1 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 16a | 2 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16a | 3 | – | brak wyniku | pusty |
| 16a | 4 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 16a | 5 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16a | 6 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16a | 7 | 1 934.8 | Syrenka [pois, pharmacy, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Golibroda Warszawski Syren) | duża_pomyłka |
| 16a | 8 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16a | 9 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16a | 10 | 31 754.6 | środek wszystkich obiektów %Syrenk% w województwie (ST_Collect) | duża_pomyłka |
| 16b | 1 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16b | 2 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16b | 3 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16b | 4 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16b | 5 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 16b | 6 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 16b | 7 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 16b | 8 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 16b | 9 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 16b | 10 | 837.2 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 17a | 1 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17a | 2 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17a | 3 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17a | 4 | – | brak wyniku | pusty |
| 17a | 5 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17a | 6 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17a | 7 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17a | 8 | 949.3 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN poligon | poprawny |
| 17a | 9 | 949.3 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN poligon | poprawny |
| 17a | 10 | 949.3 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN poligon | poprawny |
| 17b | 1 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 2 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 3 | 1 089.7 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN środek poligonu (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 4 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 5 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 6 | 949.3 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN poligon | poprawny |
| 17b | 7 | 949.3 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN poligon | poprawny |
| 17b | 8 | 1 089.7 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN środek poligonu (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 9 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 17b | 10 | 1 066.9 | Mikołaj Kopernik [pois, memorial, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Mikołaj Kopernik) | poprawny |
| 18 | 1 | – | brak wyniku | pusty |
| 18 | 2 | – | brak wyniku | pusty |
| 18 | 3 | – | brak wyniku | pusty |
| 18 | 4 | – | brak wyniku | pusty |
| 18 | 5 | – | brak wyniku | pusty |
| 18 | 6 | – | brak wyniku | pusty |
| 18 | 7 | – | brak wyniku | pusty |
| 18 | 8 | – | brak wyniku | pusty |
| 18 | 9 | – | brak wyniku | pusty |
| 18 | 10 | – | brak wyniku | pusty |
| 19 | 1 | 1 018.5 | Palma [pois, artwork, Warszawa] geometria → PKiN środek poligonu | poprawny |
| 19 | 2 | – | brak wyniku | pusty |
| 19 | 3 | – | BRAK_SQL | – |
| 19 | 4 | 997.7 | Palma [pois, artwork, Warszawa] geometria → PKiN punkt | poprawny |
| 19 | 5 | – | brak wyniku | pusty |
| 19 | 6 | – | BRAK_SQL | – |
| 19 | 7 | 1 018.5 | Palma [pois, artwork, Warszawa] geometria → PKiN środek poligonu | poprawny |
| 19 | 8 | – | brak wyniku | pusty |
| 19 | 9 | 1 018.5 | Palma [pois, artwork, Warszawa] geometria → PKiN środek poligonu | poprawny |
| 19 | 10 | 3 889 | środek wszystkich punktów %palma% (ST_Collect) | duża_pomyłka |
| 20 | 1 | – | brak wyniku | pusty |
| 20 | 2 | – | brak wyniku | pusty |
| 20 | 3 | – | brak wyniku | pusty |
| 20 | 4 | – | brak wyniku | pusty |
| 20 | 5 | – | brak wyniku | pusty |
| 20 | 6 | – | brak wyniku | pusty |
| 20 | 7 | – | brak wyniku | pusty |
| 20 | 8 | – | brak wyniku | pusty |
| 20 | 9 | – | brak wyniku | pusty |
| 20 | 10 | 1 969.1 | Mały Powstaniec [pois, memorial, Warszawa] geometria → PKiN środek poligonu | poprawny |
| 21a | 1 | 146.6 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 2 | 147 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 3 | 147 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 4 | 146.6 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 5 | 147 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 6 | 146.6 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 7 | 147 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 8 | 146.6 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 9 | 147 | Centrum (Centrum → poligon PKiN) | poprawny |
| 21a | 10 | 311.5 | Centrum (Centrum → punkt wewnątrz poligonu PKiN) | poprawny |
| 21b | 1 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 2 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 3 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 4 | 797 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 5 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 6 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 7 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 8 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 9 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 21b | 10 | 797.1 | Politechnika (Politechnika ← obrys Łazienek) | poprawny |
| 22a | 1 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 2 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 3 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 4 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 5 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 6 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 7 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 8 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 9 | 72 | stacje metra (tory subway) | poprawny |
| 22a | 10 | 72 | stacje metra (tory subway) | poprawny |

## 7a. Część 2g: próba naprawy (K2 + wskazówka o wyszukiwaniu po nazwie)

Te same pytania co w 2e, w kontekście dopisana jedna ogólna wskazówka (pytania.md, część 2g).

| 2g | 2e | Obiekt | 2e: ocena obiektu | 2g: ocena obiektu | 2g: rozkład wyników |
|---|---|---|---|---|---|
| 30 | 15a | Jak daleko w linii prostej w metrach jest od pomnika Chopina do Pałacu | pusty ×8, duża_pomyłka ×2 | pomyłka ×8, poprawny ×1, duża_pomyłka ×1 | 895 ×3, 1 038 ×3, 2 423.5 ×1, 93 222 ×1, 1 009.4 ×1, 1 032 ×1 |
| 31 | 15b | Jak daleko w linii prostej w metrach jest od pomnika Chopina w Łazienk | pusty ×10 | poprawny ×5, duża_pomyłka ×4, pomyłka ×1 | 2 434 ×2, 51 582 ×1, 2 434.2 ×1, 2 423.5 ×1, 1 032 ×1, 51 708.5 ×1, 2 264 ×1, 51 709 ×1, 93 072 ×1 |
| 32 | 16a | Jak daleko w linii prostej w metrach jest od Syrenki Warszawskiej do P | pomyłka ×7, duża_pomyłka ×2, pusty ×1 | poprawny ×5, pomyłka ×3, duża_pomyłka ×2 | 2 055 ×2, 837 ×2, 2 054.9 ×2, 1 900 ×1, 2 122.6 ×1, 834 ×1, 1 935 ×1 |
| 33 | 16b | Jak daleko w linii prostej w metrach jest od pomnika Syrenki nad Wisłą | pomyłka ×10 | pomyłka ×9, duża_pomyłka ×1 | 1 893 ×4, 706.3 ×2, 2 054.9 ×2, 2 055 ×1, 64 306 ×1 |
| 34 | 17a | Jak daleko w linii prostej w metrach jest od pomnika Kopernika do Pała | poprawny ×9, pusty ×1 | poprawny ×10 | 949.3 ×7, 949 ×2, 1 089.7 ×1 |
| 35 | 18 | Jak daleko w linii prostej w metrach jest od Kolumny Zygmunta do Pałac | pusty ×10 | poprawny ×10 | 1 801.3 ×4, 1 636 ×4, 1 801 ×2 |
| 36 | 19 | Jak daleko w linii prostej w metrach jest od palmy na rondzie de Gaull | poprawny ×4, pusty ×3, brak_sql ×2, duża_pomyłka ×1 | duża_pomyłka ×5, poprawny ×5 | 2 859.4 ×2, 880.8 ×2, 881 ×2, 1 018.5 ×1, 2 973.9 ×1, 1 261.5 ×1, 96 323.1 ×1 |
| 37 | 20 | Jak daleko w linii prostej w metrach jest od pomnika Małego Powstańca  | pusty ×9, poprawny ×1 | duża_pomyłka ×7, poprawny ×2, pusty ×1 | 2 226 ×3, 2 420 ×2, 1 969 ×1, 1 965 ×1, 2 226.1 ×1, 2 420.2 ×1, pusty_wynik ×1 |
| 38 | 13a | Jak daleko w linii prostej w metrach jest z Łazienek do Pałacu Kultury | poprawny ×10 | poprawny ×10 | 2 778.4 ×6, 2 778 ×2, 2 041.5 ×1, 2 193.6 ×1 |
| 39 | 21a | Jak daleko w metrach jest od Pałacu Kultury i Nauki do najbliższej sta | poprawny ×10 | poprawny ×10 | 146.6 ×6, 147 ×3, 299.8 ×1 |

### Przyczyny pustych wyników i pomyłek w 2g

| # | Próba | Wynik | Kandydat / diagnoza | Ocena |
|---|---|---|---|---|
| 30 | 1 | 895 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 30 | 3 | 1 038 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN punkt w poligonie | pomyłka |
| 30 | 4 | 895 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 30 | 5 | 895 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 30 | 6 | 93 222 | Pomnik Fryderyka Chopina [pois, memorial, Radom] geometria → PKiN punkt w poligonie | duża_pomyłka |
| 30 | 7 | 1 009.4 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN punkt | pomyłka |
| 30 | 8 | 1 032 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN środek poligonu | pomyłka |
| 30 | 9 | 1 038 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN punkt w poligonie | pomyłka |
| 30 | 10 | 1 038 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN punkt w poligonie | pomyłka |
| 31 | 2 | 51 582 | Pomnik Fryderka Chopina [pois, memorial, powiat sochaczewski] geometria → PKiN poligon | duża_pomyłka |
| 31 | 5 | 1 032 | Fortepian Chopina [pois, memorial, Warszawa] geometria → PKiN środek poligonu | pomyłka |
| 31 | 7 | 51 708.5 | Pomnik Fryderka Chopina [pois, memorial, powiat sochaczewski] geometria → PKiN środek poligonu | duża_pomyłka |
| 31 | 9 | 51 709 | Pomnik Fryderka Chopina [pois, memorial, powiat sochaczewski] geometria → PKiN środek poligonu | duża_pomyłka |
| 31 | 10 | 93 072 | Pomnik Fryderyka Chopina [pois, memorial, Radom] geometria → PKiN poligon | duża_pomyłka |
| 32 | 2 | 837 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 32 | 5 | 2 122.6 | Stadion Syrenki [pois_a, pitch, Warszawa] środek → PKiN środek poligonu (w granicy 2 m także: Stadion Syrenki) | duża_pomyłka |
| 32 | 7 | 837 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt | pomyłka |
| 32 | 8 | 834 | Syrenka [pois, artwork, Warszawa] geometria → PKiN punkt w poligonie | pomyłka |
| 32 | 9 | 1 935 | Syrenka [pois, pharmacy, Warszawa] geometria → PKiN punkt (w granicy 2 m także: Golibroda Warszawski Syren) | duża_pomyłka |
| 33 | 1 | 2 055 | Syrenka Warszawska [pois_a, memorial, Warszawa] środek → PKiN środek poligonu | pomyłka |
| 33 | 2 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 33 | 3 | 1 893 | Syrenka Warszawska [pois_a, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 33 | 4 | 1 893 | Syrenka Warszawska [pois_a, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 33 | 5 | 64 306 | Syrenka Białobrzeska [pois, artwork, powiat białobrzeski] geometria → PKiN środek poligonu | duża_pomyłka |
| 33 | 6 | 1 893 | Syrenka Warszawska [pois_a, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 33 | 7 | 2 054.9 | Syrenka Warszawska [pois_a, memorial, Warszawa] środek → PKiN środek poligonu | pomyłka |
| 33 | 8 | 706.3 | Syrenka [pois, artwork, Warszawa] geometria → PKiN poligon | pomyłka |
| 33 | 9 | 2 054.9 | Syrenka Warszawska [pois_a, memorial, Warszawa] środek → PKiN środek poligonu | pomyłka |
| 33 | 10 | 1 893 | Syrenka Warszawska [pois_a, memorial, Warszawa] geometria → PKiN poligon | pomyłka |
| 36 | 1 | 2 859.4 | Las Palmas [pois, beauty_shop, Warszawa] geometria → PKiN punkt | duża_pomyłka |
| 36 | 5 | 2 973.9 | Las Palmas [pois, cafe, Warszawa] geometria → PKiN środek poligonu | duża_pomyłka |
| 36 | 8 | 2 859.4 | Las Palmas [pois, beauty_shop, Warszawa] geometria → PKiN punkt | duża_pomyłka |
| 36 | 9 | 1 261.5 | Pizza pod Palmą [pois, fast_food, Warszawa] geometria → PKiN punkt w poligonie | duża_pomyłka |
| 36 | 10 | 96 323.1 | Palmyra Kebab [pois, fast_food, Płock] geometria → PKiN środek poligonu | duża_pomyłka |
| 37 | 1 | 2 420 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] punkt wewnątrz → PKiN punkt w poligonie | duża_pomyłka |
| 37 | 2 | 2 420 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] punkt wewnątrz → PKiN punkt w poligonie | duża_pomyłka |
| 37 | 3 | 2 226 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] geometria → PKiN poligon | duża_pomyłka |
| 37 | 5 | 2 226 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] geometria → PKiN poligon | duża_pomyłka |
| 37 | 7 | 2 226 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] geometria → PKiN poligon | duża_pomyłka |
| 37 | 8 | 2 226.1 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] geometria → PKiN poligon | duża_pomyłka |
| 37 | 9 | 2 420.2 | Szkoła Podstawowa nr 32 im. Małego Powstańca [pois_a, school, Warszawa] punkt wewnątrz → PKiN punkt w poligonie | duża_pomyłka |
| 37 | 10 | – | nie ustalono | pusty |

## 8. Puste wyniki przy pytaniach z promieniem

Przy pustym wyniku skrypt powtarza zapytanie z promieniem 10⁸ m. Jeśli nadal nic nie zwraca, zawiódł punkt odniesienia, a nie promień.

| # | Promień (rozkład) | Punkt odniesienia znaleziony | nie znaleziony |
|---|---|---|---|
| 4a | 3 000 ×10 | 10 | 0 |
| 4b | 2 000 ×6, 1 500 ×4 | 10 | 0 |
| 4c | 5 000 ×10 | 0 | 10 |
| 23d | 1 000 ×10 | 10 | 0 |
| 24 | 2 000 ×8, 1 500 ×1, 3 000 ×1 | 10 | 0 |

## 9. Ujawnianie założeń i powtarzalność

| Część | Prób | Uwagi niepuste | Ujawnił wartość/założenie | Warianty z jednym SQL we wszystkich próbach | Warianty z jedną wartością we wszystkich próbach |
|---|---|---|---|---|---|
| 2a | 230 | 230 | 229 | 0/23 | 11/23 |
| 2b | 40 | 40 | 38 | 2/4 | 3/4 |
| 2c | 50 | 50 | 50 | 0/5 | 1/5 |
| 2d | 60 | 60 | 60 | 0/6 | 3/6 |
| 2e | 180 | 180 | 104 | 2/18 | 6/18 |
| 2f | 180 | 180 | 179 | 0/18 | 9/18 |
| 2g | 100 | 100 | 40 | 0/10 | 0/10 |
| 2h | 10 | 10 | 10 | 0/1 | 1/1 |

## 10. Czy więcej powtórzeń coś zmienia? Pierwsze 5 prób a wszystkie

Dla każdego wariantu z przyjętą wartością (części 2a–2d i 2f): rodzaj dominujący i mediana z prób 1–5 oraz ze wszystkich prób. Wypisane są tylko warianty, w których coś się zmieniło. Części 2e i 2g pomijamy, bo mediana odległości miesza tam różne obiekty; dla nich patrz ocena obiektu w sekcji 7.

| # | Pierwsze 5: rodzaj, mediana, rozkład | Wszystkie: rodzaj, mediana, rozkład |
|---|---|---|
| 3c | PROMIEŃ, 2 000; 2 000 ×3, 1 500 ×2 | PROMIEŃ, 1 750; 2 000 ×5, 1 500 ×5 |
| 5c | PROMIEŃ, 3 000; 3 000 ×3, 2 000 ×2 | PROMIEŃ, 2 000; 2 000 ×5, 3 000 ×4, 1 500 ×1 |
| 7c | PROMIEŃ, 1 500; 1 500 ×3, 1 000 ×2 | PROMIEŃ, 1 000; 1 000 ×7, 1 500 ×3 |
| 8d | PROMIEŃ, 3 750; 3 750 ×3, 3 000 ×2 | PROMIEŃ, 3 000; 3 000 ×6, 3 750 ×4 |
| 25c | PROMIEŃ, 500; 500 ×4, 800 ×1 | PROMIEŃ, 650; 500 ×5, 800 ×5 |

Wariantów ze zmianą rodzaju dominującego, mediany albo stabilności: 5 z 56.

| Czynnik | Pierwsze 5 prób | Wszystkie próby |
|---|---|---|
| S: sytuacja pytającego | 7/8 — wyraźny wpływ | 6/8 — wyraźny wpływ |
| M: miejsce | 9/9 — wyraźny wpływ | 9/9 — wyraźny wpływ |
| O: rodzaj i skala obiektu | 9/9 — wyraźny wpływ | 9/9 — wyraźny wpływ |

| Porównanie | Pierwsze 5 prób | Wszystkie próby |
|---|---|---|
| brak informacji → samochodem: 7a → 7c | ROŚNIE | BEZ_ZMIANY |
| 2f: siła określenia (od „w pobliżu”): 1a → 25c | BEZ_ZMIANY | ROŚNIE |

## 11. Replikacja (osobna seria z 24.11, 2 próby na wariant, poza analizą)

Prób: 112. Ten sam rodzaj interpretacji co dominujący w serii głównej: 108/112. Wartość w zakresie min–max serii głównej: 99/112 (próby bez wartości, np. odmowa albo pusty wynik, liczą się tu jako poza zakresem nawet przy zgodnym rodzaju).

| # | Seria główna | Replikacja | Ocena obiektu (2e) |
|---|---|---|---|
| 8a | BRAK_SQL [] | promień 1 000, promień 1 250 | – |
| 8c | BRAK_SQL [] | brak_sql, brak_sql | – |
| 15a | PUSTY_WYNIK [] | odległość 1 032.5, pusty_wynik | {'pomyłka': 1, 'pusty': 1} |
| 15b | PUSTY_WYNIK [] | pusty_wynik, pusty_wynik | {'pusty': 2} |
| 18 | PUSTY_WYNIK [] | pusty_wynik, pusty_wynik | {'pusty': 2} |
| 19 | ODLEGŁOŚĆ [997.7, 1018.5, 3889.0] | odległość 1 018.5, brak_sql | {'poprawny': 1} |
| 20 | PUSTY_WYNIK [] | pusty_wynik, pusty_wynik | {'pusty': 2} |

Ręcznych korekt odczytu: 0 (wyniki/korekty.json).
