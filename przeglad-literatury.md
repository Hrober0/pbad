# Przegląd literatury - LLM jako interfejs do danych przestrzennych

## 1. GeoSQL-Eval: First Evaluation of LLMs on PostGIS-Based NL2GeoSQL Queries (2026)

**Link:** https://www.sciencedirect.com/science/article/pii/S0957417426010353

**Tematyka:** Generowanie i ocena przestrzennych zapytań SQL dla PostGIS.

Praca przedstawia GeoSQL-Eval - framework do oceny modeli językowych generujących zapytania przestrzenne SQL.
Autorzy analizują m.in. poprawność składniową, zgodność ze schematem bazy danych, semantykę zapytań i poprawność wykonania.
Framework uwzględnia różnorodne funkcje przestrzenne PostGIS i tematyczne bazy danych.

**Znaczenie dla projektu:** Publikacja może posłużyć jako punkt odniesienia przy projektowaniu własnego zestawu testowego, metryk ewaluacyjnych i procedury porównywania modeli.

**Wnioski z artykułu:**

- Poprawna składnia SQL nie gwarantuje, że zapytanie zwróci oczekiwane wyniki.
- W zapytaniach przestrzennych ważne jest prawidłowe dobranie funkcji PostGIS, parametrów i układu współrzędnych.
- Ocena modeli powinna uwzględniać nie tylko poprawność zapytania, ale także zgodność ze schematem bazy danych i poprawność wyników.
- Osobno warto analizować błędy związane z niejednoznacznością pytań, funkcjami przestrzennymi i strukturą bazy danych.

## 2. From Questions to Queries: An AI-Powered Multi-Agent Framework for Spatial Text-to-SQL (2026)

**Link:** https://www.tandfonline.com/doi/full/10.1080/17538947.2026.2687193

**Tematyka:** Wieloagentowy system przekształcający pytania w języku naturalnym w przestrzenne zapytania SQL.

Autorzy przedstawiają architekturę, w której poszczególne etapy zadania są rozdzielone pomiędzy wyspecjalizowane komponenty lub agentów. Proces obejmuje interpretację pytania, pozyskiwanie kontekstu o bazie danych, planowanie zapytania, generowanie SQL oraz weryfikację rezultatu. Takie podejście pozwala oddzielić rozumienie intencji użytkownika od generowania i sprawdzania zapytania.

**Znaczenie dla projektu:** Praca może pomóc w zaprojektowaniu architektury aplikacji, szczególnie jeśli system ma analizować schemat bazy, wykrywać błędy SQL i automatycznie poprawiać wygenerowane zapytania.

**Wnioski z artykułu:**

- Weryfikowanie wygenerowanych zapytań i poprawianie ich na podstawie błędów wykonania może zwiększyć niezawodność systemu.
- Złożone zapytania przestrzenne mogą wymagać bardziej rozbudowanego procesu generowania i weryfikacji niż proste zapytania.
- Nie zawsze warto stosować architekturę wieloagentową - prostsze rozwiązania mogą być szybsze i tańsze dla łatwych zadań.
- Typowe błędy dotyczą m.in. obliczania odległości, wyboru geometrii oraz sposobu wykonywania agregacji.

## 3. Monkuu: A LLM-Powered Natural Language Interface for Geospatial Databases with Dynamic Schema Mapping (2025)

**Link:** https://www.tandfonline.com/doi/abs/10.1080/13658816.2025.2533322

**Tematyka:** Interfejs języka naturalnego do baz geograficznych z dynamicznym mapowaniem schematu.

Monkuu koncentruje się na dopasowywaniu pojęć występujących w pytaniu użytkownika do tabel, kolumn i innych elementów rzeczywistej bazy danych. Istotnym elementem jest dynamiczne mapowanie schematu oraz możliwość doprecyzowania niejednoznacznych nazw geograficznych z udziałem użytkownika. Rozwiązanie uwzględnia więc nie tylko generowanie zapytania, ale również kontekst danych i niepewność interpretacji pytania.

**Znaczenie dla projektu:** Publikacja jest szczególnie przydatna przy implementacji mechanizmu pobierania metadanych, dopasowywania terminów do schematu bazy i zadawania użytkownikowi pytań doprecyzowujących.

**Wnioski z artykułu:**

- Większa ilość informacji o schemacie bazy danych nie zawsze prowadzi do lepszych wyników.
- Dynamiczne dobieranie informacji o schemacie może być skuteczniejsze niż przekazywanie całego schematu modelowi.
- RAG może pomijać istotne informacje, natomiast pełny schemat może przeciążać kontekst modelu.
- Poprawne rozpoznanie intencji użytkownika jest równie ważne jak dobranie tabel i kolumn - przykładowo pytanie o liczbę obiektów wymaga agregacji, a nie zwrócenia wszystkich rekordów.
- Dodatkowe opisy schematu, reguły dotyczące danych i wyjaśnienia niejednoznacznych nazw mogą poprawiać jakość zapytań.

## 4. GPT-Based Text-to-SQL for Spatial Databases (2025)

**Link:** https://www.mdpi.com/2220-9964/14/8/288

**Tematyka:** Wykorzystanie modeli GPT do generowania SQL dla baz przestrzennych.

Autorzy analizują generowanie zapytań przestrzennych SQL z wykorzystaniem informacji o schemacie bazy danych, przykładów zapytań oraz dodatkowego kontekstu geograficznego. Podejście uwzględnia również informacje o błędach uzyskanych podczas wykonywania zapytań, które mogą pomóc w poprawieniu kolejnej wersji SQL. Praca opisuje praktyczny sposób przygotowania kontekstu dla modelu językowego bez konieczności trenowania całego modelu od podstaw.

**Znaczenie dla projektu:** To użyteczny punkt wyjścia do stworzenia pierwszego prototypu aplikacji. Można wykorzystać podobną strategię promptowania, dostarczać modelowi schemat bazy i przykładowe zapytania, a następnie stosować kontrolowane poprawianie błędów.

**Wnioski z artykułu:**

- Generowanie zapytań przestrzennych wymaga nie tylko informacji o tabelach i kolumnach, ale także wiedzy o funkcjach przestrzennych oraz znaczeniu danych geograficznych.
- Podpowiedzi dotyczące schematu mogą pomóc w rozwiązywaniu problemów z nieistniejącymi kolumnami, tabelami i niejednoznacznymi nazwami.
- Wiedza o systemie bazodanowym, opisy geograficzne i wskazówki dotyczące schematu wpływają na jakość generowanych zapytań.

## 5. GS-SQL: Modeling Spatial Semantics in Spatial Text-to-SQL (2024)

**Link:** https://ieeexplore.ieee.org/document/10651125

**Tematyka:** Modelowanie semantyki przestrzennej w systemach Text-to-SQL.

Praca zwraca uwagę na trudności, które pojawiają się przy tłumaczeniu pytań przestrzennych na SQL. Oprócz dopasowania elementów schematu konieczne jest prawidłowe rozpoznanie obiektów geograficznych i relacji przestrzennych. Autorzy przedstawiają metodę uwzględniającą semantykę przestrzenną oraz zbiór GeoSpatialSpider, zawierający przykłady zapytań związanych z danymi geograficznymi.

**Znaczenie dla projektu:** Publikacja może pomóc w opracowaniu mechanizmu interpretowania sformułowań takich jak „w pobliżu”, „wewnątrz”, „przecina się z” czy „najbliższy”. Są to pojęcia, które trzeba przełożyć na odpowiednie operacje i funkcje przestrzenne SQL.

**Wnioski z artykułu:**

- Rozpoznawanie znaczenia przestrzennego pytania i uwzględnianie go przy dopasowywaniu elementów schematu może poprawiać jakość generowanych zapytań.
- Poprawne rozpoznanie encji przestrzennych pomaga modelowi lepiej dobierać tabele, kolumny i operacje.
- Prostsze funkcje przestrzenne, takie jak `ST_Area`, `ST_Perimeter` i `ST_Length`, mogą być łatwiejsze do obsłużenia niż zapytania wymagające bardziej złożonych relacji między obiektami.
- Zapytania wykorzystujące wiele argumentów, złożone relacje przestrzenne lub zagnieżdżoną składnię stanowią większe wyzwanie.
- Ocena powinna uwzględniać znaczenie zapytania i jego wyniki, a nie tylko zgodność wygenerowanego kodu z jednym wzorcem SQL.

## 6. NALSpatial: An Effective Natural Language Transformation Framework for Queries over Spatial Data (2023)

**Link:** https://dl.acm.org/doi/10.1145/3589132.3625600

**Tematyka:** Systematyczne przekształcanie pytań w języku naturalnym w zapytania dotyczące danych przestrzennych.

NALSpatial przedstawia podejście etapowe, obejmujące rozpoznawanie encji, klasyfikację intencji i generowanie zapytań. System uwzględnia różne rodzaje operacji przestrzennych, m.in. zapytania zakresowe, wyszukiwanie najbliższych sąsiadów, złączenia przestrzenne oraz agregacje. Praca pokazuje, że poprawne tłumaczenie pytań geograficznych wymaga zarówno rozumienia języka, jak i znajomości operacji dostępnych w bazie danych.

**Znaczenie dla projektu:** Publikacja jest przydatna przy projektowaniu pipeline’u tłumaczenia pytań na SQL. Może również pomóc w określeniu zestawu obsługiwanych typów zapytań w pierwszej wersji aplikacji.

**Wnioski z artykułu:**

- Tłumaczenie pytania na zapytanie przestrzenne można podzielić na rozpoznawanie intencji i parametrów oraz generowanie zapytania.
- Ważne jest rozpoznawanie takich informacji jak lokalizacja, próg odległości, liczba najbliższych obiektów i rodzaj relacji przestrzennej.
- System obsługuje cztery typy zapytań: zakresowe, wyszukiwanie najbliższych sąsiadów, złączenia przestrzenne i agregacje.
- Autorzy raportują, że system poprawnie tłumaczy zdecydowaną większość testowanych zapytań i odpowiada w ciągu kilku sekund.
- Wyników nie można bezpośrednio porównywać z innymi systemami, ponieważ NALSpatial wykorzystuje odmienną architekturę i bazę SECONDO, a nie PostGIS.

## 7. Is ChatGPT a Good Geospatial Data Analyst? Exploring the Integration of Natural Language into Structured Query Language within a Spatial Database (2024)

**Link:** https://www.mdpi.com/2220-9964/13/1/26

**Tematyka:** Wykorzystanie ChatGPT do analizy danych geograficznych za pomocą SQL.

Autorzy badają, w jakim stopniu model językowy może wspierać użytkownika w pracy z przestrzenną bazą danych. Rozważany przepływ obejmuje interpretację pytania, generowanie SQL, wykonanie zapytania oraz przedstawienie wyniku użytkownikowi. Praca omawia możliwości tego podejścia, a także ograniczenia związane z niezawodnością generowanych zapytań i poprawnym rozumieniem danych.

**Znaczenie dla projektu:** Publikacja dobrze uzasadnia potrzebę budowy kompletnego interfejsu, który nie tylko generuje kod SQL, lecz także wykonuje zapytanie i pomaga użytkownikowi zrozumieć wynik.

**Wnioski z artykułu:**

- LLM w większości przypadków generują poprawny przestrzenny SQL, ale skuteczność spada wraz ze złożonością pytania. Najtrudniejsze są złączenia przestrzenne kilku tabel.
- Autorzy wskazują brak dużego zbioru testowego dla przestrzennego Text-to-SQL. Taki zbiór powinien obejmować różne typy zadań i nieprecyzyjne pytania.

## 8. Large Language Models for Spatial Analysis Queries (2025)

**Link:** https://www.vldb.org/pvldb/vol18/p5451-mokbel.pdf

**Tematyka:** Krótki przegląd sposobów wykorzystania dużych modeli językowych w analizie danych przestrzennych.

Publikacja zestawia dotychczasowe prace o LLM w analizie przestrzennej. Grupuje je według tego, jak bardzo model jest dostosowywany do danych przestrzennych, oraz według rodzaju zastosowań (m.in. ruch drogowy, trajektorie, punkty POI). Nie zawiera własnych eksperymentów ani szczegółowego omówienia wyników.

**Znaczenie dla projektu:** Przydatna głównie we wstępie, do pokazania szerszego kontekstu i umiejscowienia naszego podejścia (gotowy model sterowany promptem) wśród innych sposobów wykorzystania LLM.

**Wnioski z artykułu:**

- Publikacja ma charakter krótkiego przeglądu i porządkuje dotychczasowe prace dotyczące wykorzystania LLM w analizie danych przestrzennych.
- Autorzy wyróżniają cztery podejścia, uporządkowane według stopnia ingerencji w model: użycie gotowego modelu sterowanego promptem, douczenie modelu na danych z zadania (fine-tuning), wytrenowanie modelu od zera na danych przestrzennych oraz dodatkową zmianę sposobu jego uczenia pod zadania przestrzenne. Głębsze dostosowanie daje wyższą dokładność, ale wymaga więcej pracy.

## 9. Text-to-SQL Empowered by Large Language Models: A Benchmark Evaluation (2024)

**Link:** https://www.vldb.org/pvldb/vol17/p1132-gao.pdf

**Tematyka:** Ocena metod generowania SQL z wykorzystaniem dużych modeli językowych.

Praca analizuje strategie promptowania, wybór przykładów oraz sposób przekazywania kontekstu modelowi.
Autorzy przedstawiają DAIL-SQL - podejście wykorzystujące m.in. dobór przykładów do pytania użytkownika i odpowiednią organizację promptu.
Badanie dotyczy ogólnego Text-to-SQL, a nie wyłącznie baz przestrzennych, ale dostarcza użytecznych metod oceny jakości i projektowania generatorów SQL.

**Znaczenie dla projektu:** Publikacja może posłużyć do wyboru strategii few-shot prompting, przygotowania przykładów SQL i zaplanowania porównania kilku modeli lub wariantów promptu. Wyników uzyskanych na standardowych bazach relacyjnych nie należy jednak bezpośrednio traktować jako miary jakości generowania PostGIS SQL.

**Wnioski z artykułu:**

- Sposób zbudowania promptu (zapis schematu bazy, dobór przykładów i ich forma) ma istotny wpływ na poprawność generowanego SQL.
- Najlepsze wyniki uzyskano, gdy model otrzymywał strukturę bazy danych w postaci kodu SQL, uwzględniającego klucze główne i obce.
- Dodanie do promptu przykładów pytań wraz z odpowiadającymi im zapytaniami SQL poprawiało wyniki. Przykłady te były automatycznie dobierane na podstawie podobieństwa do aktualnego pytania, zarówno pod względem treści, jak i struktury zapytania SQL.
- Autorzy podkreślają, że oprócz poprawności liczy się też długość promptu, bo wpływa na koszt. Ich metoda osiągnęła lepsze wyniki niż wcześniejsze rozwiązania, mimo krótszego promptu.

## 10. Benchmarking and Improving Text-to-SQL Generation under Ambiguity (2023)

**Link:** https://aclanthology.org/2023.emnlp-main.436/

**Tematyka:** Generowanie SQL dla niejednoznacznych pytań w języku naturalnym.

Autorzy analizują sytuacje, w których jedno pytanie użytkownika może mieć kilka poprawnych interpretacji. Przedstawiają benchmark AmbiQT oraz metodę LogicalBeam, która ma wspierać generowanie odmiennych interpretacji logicznych. Praca pokazuje, że różne wygenerowane zapytania nie muszą reprezentować różnych znaczeń pytania - mogą być jedynie odmiennymi zapisami podobnej logiki.

**Znaczenie dla projektu:** To ważne źródło przy projektowaniu interfejsu, który powinien wykrywać niejednoznaczność, prezentować możliwe interpretacje i ewentualnie prosić użytkownika o doprecyzowanie pytania przed wykonaniem zapytania SQL.

**Wnioski z artykułu:**

- Jedno pytanie użytkownika można czasem zinterpretować na kilka poprawnych sposobów, co prowadzi do różnych zapytań SQL.
- Badane modele, w tym ChatGPT, zwykle podawały tylko jedną interpretację. Kolejne generowane warianty SQL różniły się zapisem, a nie znaczeniem.
- Według autorów idealny system powinien przedstawić wszystkie możliwe interpretacje, aby użytkownik mógł wybrać właściwą.

## 11. Foundation Models for Geospatial Reasoning: Assessing the Capabilities of Large Language Models in Understanding Geometries and Topological Spatial Relations (2025)

**Link:** https://www.tandfonline.com/doi/full/10.1080/13658816.2025.2511227

**Tematyka:** Ocena zdolności dużych modeli językowych do rozumienia geometrii i relacji topologicznych między obiektami geograficznymi.

Autorzy badają, czy modele językowe potrafią interpretować geometrie zapisane w formacie WKT (Well-Known Text) oraz rozpoznawać relacje przestrzenne między obiektami. Analizują m.in. wykorzystanie promptowania i reprezentacji geometrii do wnioskowania o relacjach topologicznych. Wyniki pokazują, że modele językowe mogą wspierać rozumowanie przestrzenne, ale nadal popełniają istotne błędy, co ogranicza możliwość bezwarunkowego polegania na ich interpretacji.

**Znaczenie dla projektu:** Artykuł pokazuje, że LLM popełniają istotne błędy, gdy samodzielnie określają relacje przestrzenne między obiektami. Uzasadnia to nasze podejście, w którym model jedynie tłumaczy pytanie na zapytanie SQL, a sprawdzenie relacji przestrzennych wykonuje baza danych. Wyniki wskazują też, że informacje dodane do promptu, np. przykłady czy typ geometrii, wpływają na poprawność odpowiedzi.

**Wnioski z artykułu:**

- Modele językowe mają trudność z samodzielnym określaniem relacji przestrzennych między geometriami zapisanymi w formacie WKT.
- Dodanie do promptu kilku przykładów (few-shot) oraz informacji o typie geometrii (punkt, linia, poligon) poprawiało wyniki.
- Prompt nakazujący rozumowanie krok po kroku (Chain-of-Thought) pogarszał wyniki modeli GPT-3.5 i GPT-4.
- Autorzy stwierdzają, że w obliczeniach geometrycznych bazy przestrzenne przewyższają LLM. Jako obiecujący kierunek wskazują podejście, w którym LLM tłumaczy pytanie użytkownika na formalne zapytanie, a obliczenia wykonuje baza danych.

## 12. A Survey on Employing Large Language Models for Text-to-SQL Tasks (2025)

**Link:** https://dl.acm.org/doi/full/10.1145/3737873

**Tematyka:** Przegląd zastosowań dużych modeli językowych do tłumaczenia pytań w języku naturalnym na zapytania SQL.

Publikacja porządkuje metody wykorzystywania LLM do generowania SQL. Omawia dwa główne podejścia: sterowanie gotowym modelem za pomocą odpowiednio przygotowanego promptu oraz douczanie modelu na własnych danych. Opisuje także sposoby oceny jakości oraz ograniczenia i otwarte problemy obecnych rozwiązań.

**Znaczenie dla projektu:** To źródło stabilnej wiedzy o tym, jak LLM generują zapytania SQL i jakie mają przy tym ograniczenia. Uzasadnia, dlaczego w projekcie warto badać, jakie informacje o bazie danych przekazuje się modelowi.

**Wnioski z artykułu:**

- Text-to-SQL to zadanie znane na długo przed LLM: najpierw rozwiązywano je regułami i szablonami, potem sieciami neuronowymi, a LLM są kolejnym etapem.
- Artykuł opisuje różne sposoby przekazywania modelowi informacji potrzebnych do zapytania, co może nam się przydać, ponieważ prawdopodobnie będziemy je badać.
- Sposób opisania bazy danych w prompcie wpływa na wynik: uporządkowany opis tabel działa lepiej niż luźny tekst, a przykładowe dane pomagają, o ile prompt nie robi się za długi.
- Modele najczęściej mylą się przy dopasowaniu pytania do właściwych tabel i kolumn, a w dalszej kolejności przy łączeniu tabel.
- Najlepsze wyniki dają podejścia, w których model sprawdza i poprawia swoje zapytanie, a w trudnych zadaniach agenci wykonujący pracę w kilku krokach wyraźnie wygrywają z pozostałymi metodami.
- Ocena poprawności zapytań nie jest prosta, bo to samo zapytanie można zapisać na różne sposoby, a błędne zapytanie może przypadkiem zwrócić poprawny wynik.

## 13. Autonomous GIS: The Next-Generation AI-Powered GIS (2023)

**Link:** https://www.tandfonline.com/doi/full/10.1080/17538947.2023.2278895

**Repozytorium:** https://github.com/gladcolor/LLM-Geo

**Tematyka:** System GIS, w którym duży model językowy sam wykonuje analizy przestrzenne.

Autorzy proponują GIS, w którym LLM na podstawie pytania użytkownika sam planuje analizę, pisze kod w Pythonie, uruchamia go i pokazuje wynik, np. w postaci liczby, wykresu lub mapy. Pomysł sprawdzili na prototypie LLM-Geo opartym na GPT-4, którego kod jest dostępny na GitHubie. W odróżnieniu od podejścia text-to-SQL model nie generuje zapytań do bazy danych, tylko kod wykonujący całą analizę, więc jest to rozwiązanie ogólne, niedopasowane do jednego typu problemu.

**Znaczenie dla projektu:** Przydatne we wstępie, do pokazania, w jakim kierunku rozwija się łączenie LLM z GIS oraz jako punkt odniesienia dla naszego węższego podejścia opartego na SQL, które łatwiej kontrolować i ocenić. LLM-Geo to przykład działającego, otwartego rozwiązania.

**Wnioski z artykułu:**

- LLM może pełnić rolę „mózgu” systemu GIS, który sam planuje analizę i generuje wykonujący ją kod w Pythonie.
- W przykładowych analizach prototyp zwrócił poprawne wyniki, co autorzy sprawdzili ręcznie.
- Większość błędów wynikała z niepoprawnie wygenerowanego kodu, a system nie ma mechanizmu jego sprawdzania i poprawiania.
- Autorzy uważają to podejście za wczesny etap i jako jeden z kierunków wskazują przekazywanie modelowi błędów, żeby sam poprawiał kod.
- Artykuł pokazuje ogólniejsze podejście, w którym model sam pisze kod całej analizy, co może nam się przydać we wstępie jako kontrast dla naszego węższego podejścia, w którym model generuje tylko zapytania SQL, a obliczenia przestrzenne wykonuje baza danych.

## Nieoficjalne źródła do przejrzenia

- (wystąpienie) https://www.youtube.com/watch?v=jv7O0a5YKgg
- (wystąpienie) https://www.youtube.com/watch?v=FxqFEx-JdJw
- (blog) https://dev.to/zeekrey/building-a-text-to-gis-engine-with-sveltekit-postgis-and-open-source-llms-57bo
- (blog Google Cloud, AlloyDB - gotowe rozwiązanie) https://cloud.google.com/blog/products/databases/techniques-for-improving-text-to-sql
- (claude-docs, kontekst podany w prompcie) https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
- (claude-docs, kontekst pobierany przez model za pomocą narzędzi) https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

## Wstępne obserwacje po analizie artykułów

- Tłumaczenie języka naturalnego na SQL rozwijano na długo przed LLM, a obecnie istnieje wiele rozwiązań o różnej architekturze: od gotowego modelu z odpowiednio przygotowanym kontekstem, przez douczanie modelu, po złożone systemy wieloagentowe. Historię i przegląd tych rozwiązań będzie można wykorzystać we wstępie artykułu.
- Wiele prac pokazuje, że informacje przekazane modelowi w prompcie, takie jak opis bazy danych, przykładowe zapytania czy dodatkowe wskazówki, wyraźnie wpływają na poprawność generowanych zapytań, ale więcej informacji nie zawsze oznacza lepszy wynik.
- Częstym źródłem błędów jest dopasowanie pytania do właściwych tabel i kolumn. U nas problem ten powinien być mniejszy, bo planujemy pracować na jednej bazie POI Warszawy, ale model nadal będzie musiał powiązać pojęcia z pytania z wartościami w danych.
- Modele językowe słabo radzą sobie z samodzielnym określaniem relacji przestrzennych, dlatego w naszym rozwiązaniu model będzie jedynie tłumaczył pytanie na zapytanie SQL, a obliczenia przestrzenne wykona baza danych.
- Model może zinterpretować niejednoznaczne lub nieprecyzyjne pytanie inaczej, niż zamierzał użytkownik, dlatego warto sprawdzić, jak modele radzą sobie z pytaniami o różnej precyzji.
- Większość badań korzysta z modeli GPT, w szczególności GPT-4, a modele Claude pojawiają się rzadko. Wynika to prawdopodobnie z tego, że Claude jest szeroko używany od niedawna, a przygotowanie i publikacja artykułów trwają długo. W związku z tym w projekcie planujemy wykorzystać Claude przez API.
- Ponieważ to samo zapytanie można zapisać na wiele sposobów, a poprawna składnia nie gwarantuje poprawnego wyniku, lepiej porównywać wyniki wykonania zapytań z oczekiwanymi niż sam kod SQL.
- Jest miejsce na wąskie badanie, które sprawdzi, jak dodatkowy kontekst i precyzja pytania wpływają na jakość zapytań przestrzennych przy prostej architekturze rozwiązania. Może ono pokazać, jak niewielkim nakładem pracy można poprawić odpowiedzi współczesnych LLM na pytania o dane przestrzenne.
