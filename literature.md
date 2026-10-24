# 10 najważniejszych publikacji o wykorzystaniu LLM do generowania przestrzennych zapytań SQL

## 1. GeoSQL-Eval: First Evaluation of LLMs on PostGIS-Based NL2GeoSQL Queries (2026)

**Link:** https://www.sciencedirect.com/science/article/pii/S0957417426010353

**Tematyka:** Generowanie i ocena przestrzennych zapytań SQL dla PostGIS.

Praca przedstawia GeoSQL-Eval — framework do oceny modeli językowych generujących zapytania przestrzenne SQL — oraz benchmark GeoSQL-Bench. Autorzy analizują m.in. poprawność składniową, zgodność ze schematem bazy danych, semantykę zapytań i poprawność wykonania. Uwzględniają różnorodne funkcje przestrzenne PostGIS i tematyczne bazy danych.

**Znaczenie dla projektu:** Publikacja jest bezpośrednio związana z budową interfejsu NL2SpatialSQL. Może posłużyć jako punkt odniesienia przy projektowaniu własnego zestawu testowego, metryk ewaluacyjnych i procedury porównywania modeli.

## 2. From Questions to Queries: An AI-Powered Multi-Agent Framework for Spatial Text-to-SQL (2026)

**Link:** https://www.tandfonline.com/doi/full/10.1080/17538947.2026.2687193

**Tematyka:** Wieloagentowy system przekształcający pytania w języku naturalnym w przestrzenne zapytania SQL.

Autorzy przedstawiają architekturę, w której poszczególne etapy zadania są rozdzielone pomiędzy wyspecjalizowane komponenty lub agentów. Proces obejmuje interpretację pytania, pozyskiwanie kontekstu o bazie danych, planowanie zapytania, generowanie SQL oraz weryfikację rezultatu. Takie podejście pozwala oddzielić rozumienie intencji użytkownika od generowania i sprawdzania zapytania.

**Znaczenie dla projektu:** Praca może pomóc w zaprojektowaniu architektury aplikacji, szczególnie jeśli system ma analizować schemat bazy, wykrywać błędy SQL i automatycznie poprawiać wygenerowane zapytania.

## 3. Monkuu: A LLM-Powered Natural Language Interface for Geospatial Databases with Dynamic Schema Mapping (2025)

**Link:** https://www.tandfonline.com/doi/abs/10.1080/13658816.2025.2533322

**Tematyka:** Interfejs języka naturalnego do baz geograficznych z dynamicznym mapowaniem schematu.

Monkuu koncentruje się na dopasowywaniu pojęć występujących w pytaniu użytkownika do tabel, kolumn i innych elementów rzeczywistej bazy danych. Istotnym elementem jest dynamiczne mapowanie schematu oraz możliwość doprecyzowania niejednoznacznych nazw geograficznych z udziałem użytkownika. Rozwiązanie uwzględnia więc nie tylko generowanie zapytania, ale również kontekst danych i niepewność interpretacji pytania.

**Znaczenie dla projektu:** Publikacja jest szczególnie przydatna przy implementacji mechanizmu pobierania metadanych, dopasowywania terminów do schematu bazy i zadawania użytkownikowi pytań doprecyzowujących.

## 4. GPT-Based Text-to-SQL for Spatial Databases (2025)

**Link:** https://www.mdpi.com/2220-9964/14/8/288

**Tematyka:** Wykorzystanie modeli GPT do generowania SQL dla baz przestrzennych.

Autorzy analizują generowanie zapytań przestrzennych SQL z wykorzystaniem informacji o schemacie bazy danych, przykładów zapytań oraz dodatkowego kontekstu geograficznego. Podejście uwzględnia również informacje o błędach uzyskanych podczas wykonywania zapytań, które mogą pomóc w poprawieniu kolejnej wersji SQL. Praca opisuje praktyczny sposób przygotowania kontekstu dla modelu językowego bez konieczności trenowania całego modelu od podstaw.

**Znaczenie dla projektu:** To użyteczny punkt wyjścia do stworzenia pierwszego prototypu aplikacji. Można wykorzystać podobną strategię promptowania, dostarczać modelowi schemat bazy i przykładowe zapytania, a następnie stosować kontrolowane poprawianie błędów.

## 5. GS-SQL: Modeling Spatial Semantics in Spatial Text-to-SQL (2024)

**Link:** https://ieeexplore.ieee.org/document/10651125

**Tematyka:** Modelowanie semantyki przestrzennej w systemach Text-to-SQL.

Praca zwraca uwagę na trudności, które pojawiają się przy tłumaczeniu pytań przestrzennych na SQL. Oprócz dopasowania elementów schematu konieczne jest prawidłowe rozpoznanie obiektów geograficznych i relacji przestrzennych. Autorzy przedstawiają metodę uwzględniającą semantykę przestrzenną oraz zbiór GeoSpatialSpider, zawierający przykłady zapytań związanych z danymi geograficznymi.

**Znaczenie dla projektu:** Publikacja może pomóc w opracowaniu mechanizmu interpretowania sformułowań takich jak „w pobliżu”, „wewnątrz”, „przecina się z” czy „najbliższy”. Są to pojęcia, które trzeba przełożyć na odpowiednie operacje i funkcje przestrzenne SQL.

## 6. NALSpatial: An Effective Natural Language Transformation Framework for Queries over Spatial Data (2023)

**Link:** https://dl.acm.org/doi/10.1145/3589132.3625600

**Tematyka:** Systematyczne przekształcanie pytań w języku naturalnym w zapytania dotyczące danych przestrzennych.

NALSpatial przedstawia podejście etapowe, obejmujące rozpoznawanie encji, klasyfikację intencji i generowanie zapytań. System uwzględnia różne rodzaje operacji przestrzennych, m.in. zapytania zakresowe, wyszukiwanie najbliższych sąsiadów, złączenia przestrzenne oraz agregacje. Praca pokazuje, że poprawne tłumaczenie pytań geograficznych wymaga zarówno rozumienia języka, jak i znajomości operacji dostępnych w bazie danych.

**Znaczenie dla projektu:** Publikacja jest przydatna przy projektowaniu pipeline’u tłumaczenia pytań na SQL. Może również pomóc w określeniu zestawu obsługiwanych typów zapytań w pierwszej wersji aplikacji.

## 7. Is ChatGPT a Good Geospatial Data Analyst? Exploring the Integration of Natural Language into Structured Query Language within a Spatial Database (2024)

**Link:** https://www.mdpi.com/2220-9964/13/1/26

**Tematyka:** Wykorzystanie ChatGPT do analizy danych geograficznych za pomocą SQL.

Autorzy badają, w jakim stopniu model językowy może wspierać użytkownika w pracy z przestrzenną bazą danych. Rozważany przepływ obejmuje interpretację pytania, generowanie SQL, wykonanie zapytania oraz przedstawienie wyniku użytkownikowi. Praca omawia możliwości tego podejścia, a także ograniczenia związane z niezawodnością generowanych zapytań i poprawnym rozumieniem danych.

**Znaczenie dla projektu:** Publikacja dobrze uzasadnia potrzebę budowy kompletnego interfejsu, który nie tylko generuje kod SQL, lecz także wykonuje zapytanie i pomaga użytkownikowi zrozumieć wynik.

---

Wnioski z artykułu:

- LLM w większości przypadków generują poprawny przestrzenny SQL, ale skuteczność spada wraz ze złożonością pytania. Najtrudniejsze są złączenia przestrzenne kilku tabel.

- Autorzy porównali różne ustawienia temperatury modelu, czyli parametru, który określa, jak bardzo losowe są odpowiedzi. Najlepsze wyniki dawała temperatura 0, przy której model zawsze wybiera najbardziej prawdopodobną odpowiedź. Porównali też kilka modeli (GPT-4, PaLM 2, LLaMA 2) i najlepiej wypadł GPT-4.

- Autorzy wskazują brak dużego zbioru testowego dla przestrzennego Text-to-SQL. Taki zbiór powinien obejmować różne typy zadań i nieprecyzyjne pytania.

## 8. Large Language Models for Spatial Analysis Queries (2025)

**Link:** https://www.vldb.org/pvldb/vol18/p5451-mokbel.pdf

**Tematyka:** Przegląd zastosowań dużych modeli językowych do zapytań analitycznych dotyczących danych przestrzennych.

Publikacja porządkuje metody wykorzystywania LLM w analizie przestrzennej. Omawia różne sposoby łączenia modeli z danymi i systemami analitycznymi, a także kwestie związane z oceną jakości, ograniczeniami obecnych rozwiązań i kierunkami dalszych badań. Jej zakres jest szerszy niż samo tłumaczenie języka naturalnego na SQL, dzięki czemu dostarcza kontekstu dla całego obszaru badań nad analizą przestrzenną wspieraną przez modele językowe.

**Znaczenie dla projektu:** To wartościowe źródło do przeglądu literatury, identyfikacji luk badawczych i uzasadnienia, dlaczego interfejs języka naturalnego do analizy przestrzennej stanowi interesujący problem badawczy.

---

Wnioski z artykułu:

- Artykuł jest zarysem tutorialu, a nie badaniem. Porządkuje dotychczasowe prace dotyczące wykorzystania LLM w analizie danych przestrzennych.

- Autorzy dzielą podejścia według stopnia ingerencji w model: od gotowego modelu sterowanego promptem, przez douczanie, aż po trenowanie od zera na danych przestrzennych. Głębsze dostosowanie daje wyższą dokładność, ale wymaga więcej pracy.

## 9. Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation (DAIL-SQL, 2023)

**Link:** https://arxiv.org/abs/2308.15363

**Tematyka:** Ocena metod generowania SQL z wykorzystaniem dużych modeli językowych.

Praca analizuje strategie promptowania, wybór przykładów oraz sposób przekazywania kontekstu modelowi. Autorzy przedstawiają DAIL-SQL — podejście wykorzystujące m.in. dobór przykładów do pytania użytkownika i odpowiednią organizację promptu. Badanie dotyczy ogólnego Text-to-SQL, a nie wyłącznie baz przestrzennych, ale dostarcza użytecznych metod oceny jakości i projektowania generatorów SQL.

**Znaczenie dla projektu:** Publikacja może posłużyć do wyboru strategii few-shot prompting, przygotowania przykładów SQL i zaplanowania porównania kilku modeli lub wariantów promptu. Wyników uzyskanych na standardowych bazach relacyjnych nie należy jednak bezpośrednio traktować jako miary jakości generowania PostGIS SQL.

---

Wnioski z artykułu:

- Sposób zbudowania promptu, czyli zapis schematu bazy, dobór przykładów i ich forma, ma istotny wpływ na poprawność generowanego SQL.

- Najlepsze wyniki dawał schemat bazy zapisany jako kod SQL z kluczami głównymi i obcymi oraz przykłady pytanie → SQL dobierane automatycznie pod konkretne pytanie, podobne zarówno w treści pytania, jak i w strukturze zapytania.

- Autorzy podkreślają, że oprócz poprawności liczy się też długość promptu, bo wpływa na koszt. Ich metoda osiągnęła lepsze wyniki niż wcześniejsze rozwiązania, mimo krótszego promptu.

## 10. Benchmarking and Improving Text-to-SQL Generation under Ambiguity (EMNLP 2023)

**Link:** https://aclanthology.org/2023.emnlp-main.436/

**Tematyka:** Generowanie SQL dla niejednoznacznych pytań w języku naturalnym.

Autorzy analizują sytuacje, w których jedno pytanie użytkownika może mieć kilka poprawnych interpretacji. Przedstawiają benchmark AmbiQT oraz metodę LogicalBeam, która ma wspierać generowanie odmiennych interpretacji logicznych. Praca pokazuje, że różne wygenerowane zapytania nie muszą reprezentować różnych znaczeń pytania — mogą być jedynie odmiennymi zapisami podobnej logiki.

**Znaczenie dla projektu:** To ważne źródło przy projektowaniu interfejsu, który powinien wykrywać niejednoznaczność, prezentować możliwe interpretacje i prosić użytkownika o doprecyzowanie pytania przed wykonaniem zapytania SQL.

---

Wnioski z artykułu:

- Jedno pytanie użytkownika można czasem zinterpretować na kilka poprawnych sposobów, co prowadzi do różnych zapytań SQL.

- Badane modele, w tym ChatGPT, zwykle podawały tylko jedną interpretację. Kolejne generowane warianty SQL różniły się zapisem, a nie znaczeniem.

- Według autorów idealny system powinien przedstawić wszystkie możliwe interpretacje, aby użytkownik mógł wybrać właściwą.

## 11. Foundation Models for Geospatial Reasoning: Assessing the Capabilities of Large Language Models in Understanding Geometries and Topological Spatial Relations (2025)

**Link:** https://www.tandfonline.com/doi/full/10.1080/13658816.2025.2511227

**Tematyka:** Ocena zdolności dużych modeli językowych do rozumienia geometrii i relacji topologicznych między obiektami geograficznymi.

Autorzy badają, czy modele językowe potrafią interpretować geometrie zapisane w formacie WKT (_Well-Known Text_) oraz rozpoznawać relacje przestrzenne między obiektami. Analizują m.in. wykorzystanie promptowania i reprezentacji geometrii do wnioskowania o relacjach topologicznych. Wyniki pokazują, że modele językowe mogą wspierać rozumowanie przestrzenne, ale nadal popełniają istotne błędy, co ogranicza możliwość bezwarunkowego polegania na ich interpretacji.

**Znaczenie dla projektu:** Publikacja jest szczególnie przydatna przy projektowaniu mechanizmu interpretacji pojęć przestrzennych, takich jak „wewnątrz”, „przecina się z”, „nakłada się na” czy „dotyka”. Może pomóc w opracowaniu testów sprawdzających, czy system poprawnie przekłada znaczenie pytania użytkownika na odpowiednie operacje i funkcje PostGIS, np. `ST_Contains`, `ST_Intersects` lub `ST_Touches`. Nie jest to jednak bezpośrednio system generujący kompletne zapytania SQL, dlatego najlepiej traktować tę pracę jako uzupełnienie badań nad generowaniem przestrzennego Text-to-SQL.

---

Wnioski z artykułu:

- Modele językowe mają trudność z samodzielnym określaniem relacji przestrzennych między geometriami zapisanymi w formacie WKT.

- Dodanie do promptu kilku przykładów (few-shot) oraz informacji o typie geometrii (punkt, linia, poligon) poprawiało wyniki.

- Prompt nakazujący rozumowanie krok po kroku (Chain-of-Thought) pogarszał wyniki modeli GPT-3.5 i GPT-4

- Autorzy stwierdzają, że w obliczeniach geometrycznych bazy przestrzenne przewyższają LLM. Jako obiecujący kierunek wskazują podejście, w którym LLM tłumaczy pytanie użytkownika na formalne zapytanie, a obliczenia wykonuje baza danych.
