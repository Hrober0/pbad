"""Eksperyment 2 (PB2): interpretacja niejasnych określeń i nazw potocznych.

Moduły:
    questions  wczytanie wariantów z eksperyment/selected/H2/pytania.md
    generate   wywołania modelu (kontekst K2, odpowiedź {"sql", "uwagi"})
    execute    wykonanie SQL na bazie (rola tylko do odczytu)
    extract    odczytanie z SQL przyjętej wartości i rodzaju interpretacji
    references kandydaci i wartości wzorcowe dla części 2e i 2g
    identify   identyfikacja obiektu wybranego przez model (po osm_id) w 2e i 2g
    analyze    opisowe porównania wariantów według ocena.md (bez testów statystycznych)
    report     tabele markdown do wyniki/tabele.md
    replicate  seria kontrolna w osobnym pliku (poza analizą)
"""
