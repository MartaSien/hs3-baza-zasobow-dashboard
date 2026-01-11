# HS3 Baza zasobów Dashboard

Skrypt, który generuje podsumowanie [Bazy Wiedzy zasobów Hackerspace Trójmiasto](https://kb.hs3.pl/docs) w formie statycznej strony internetowej.

## Sposób działania

1. Baza Wiedzy znajduje się na Discourse Hackerspace Trójmiasto i jest dostępna publicznie. Projekt wykorzystuje Discourse REST API do pobrania listy zasobów.
1. Lista zasobów zapisana jest w pliku csv `zasoby.csv`.
1. Skrypt tworzy statyczną stronę internetową na podstawie pliku `.csv`.
1. Strona jest hostowana przy pomocy GitHub Pages.

## Możliwości generatora bazy zasobów csv

- pobieranie listy wszystkich zasobów z wybranej kategorii
- pobieranie ID, tagów i treści posta każdego zasobu
- wyłuskanie z treści posta informacji:
  - nazwa przedmiotu
  - miejsce zamieszkania
  - ilość
  - opiekunowie
- oto jak powinien wyglądać ostateczny wpis:

```
ID, nazwa, miejsce, ilość, opiekunowie, tagi
```

## Możliwości dashboard'u

- filtrowanie bazy zasobów po tagach
- sortowanie alfabetyczne bazy zasobów po dowolnej kolumnie
- linki do zasobu na Discourse w ID zasobu
- łatwa zmiana ilości kolumn dashboardu

## Co chcę dodać w przyszłości

- wizualizacja statystyk z bazy zasobów
- generowanie drugiego pliku csv służącego do wygenerowania naklejek z kodem QR

## Dokumentacja

- [Discourse REST API](https://docs.discourse.org/)