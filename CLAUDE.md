# CLAUDE.md

Plik kontekstowy dla Claude. Zawiera informacje o moim stacku technologicznym, projektach i preferencjach pracy.

---

## 👤 O mnie

**Poziom umiejętności:** Prawie średniozaawansowany (powyżej początkującego)

Znam i swobodnie używam:
- OOP (klasy, konstruktory, dziedziczenie, hermetyzacja)
- Funkcje, struktury kontrolne, składnia kilku języków
- Pracę w terminalu i z bibliotekami zewnętrznymi

Aktualnie się rozwijam w kierunku poznawania nowych bibliotek oraz łączenia hardware'u z softwarem.

---

## 💻 Środowisko pracy

| Element | Wartość |
|---------|---------|
| OS | Windows 11 |
| IDE | VS Code |
| Język komunikacji | PL + EN (terminy techniczne po angielsku) |

---

## 🛠️ Stack technologiczny

### C++ — mikrokontrolery
- **Arduino** (głównie)
- **ESP32**

Zastosowania: obsługa sensorów, komunikacja przez Serial, sterowanie I/O.

### Python — software, GUI, integracje
Aktywnie używane biblioteki:
- `pyserial` — komunikacja z mikrokontrolerami
- `tkinter` — GUI
- `pygame` — GUI z animacjami / grafiką
- `numpy` — analiza i przetwarzanie danych
- `requests` — komunikacja HTTP
- `anthropic` — integracja z LLM (Claude API)

Zastosowania: software desktop, GUI z animacjami, analiza danych z mikrokontrolerów, projekty z LLM.

### MicroPython
Używam okazjonalnie do projektów, gdzie Python działa bezpośrednio na mikrokontrolerze.

### Java — mój najmocniejszy język (obecnie nieaktywny)
- **Spigot/Bukkit API** — pluginy Minecraft
- Projekty terminalowe
- Proste aplikacje GUI z JFrame

> 💡 Java to mój pierwszy język i czuję się w niej najpewniej. Porównania konceptów Python/C++ ↔ Java są dla mnie pomocne i ułatwiają zapamiętywanie.

---

## 🚧 Aktualny projekt

**Stacja pomiarowa parametrów otoczenia**

**Hardware (Arduino + C++):**
- Pomiar: temperatura, ciśnienie, wilgotność
- Wysyłanie danych przez Serial do komputera

**Software (Python):**
- Odbiór danych z portu szeregowego (`pyserial`)
- Analiza odebranych parametrów
- GUI z animacjami wizualizującymi parametry środowiskowe

**Architektura ogólna:**
```
[Sensors] → [Arduino C++] → [Serial] → [Python software] → [GUI z animacjami]
```

---

## ⚙️ Preferencje pracy z Claude

### Język odpowiedzi
- Polski jako podstawa
- Terminy techniczne po angielsku (np. *loop*, *callback*, *thread*, *exception handling*)
- Nie tłumacz na siłę nazw bibliotek/funkcji

### Poziom wyjaśnień
- ✅ **Pomijaj** podstawy OOP, składnię, podstawowe konstrukcje
- ✅ **Wyjaśniaj** koncepty zaawansowane (np. dekoratory, metaclasses, asynchroniczność, wzorce projektowe, niskopoziomowe rzeczy w C++)
- Zakładaj że umiem czytać kod i znam dokumentację — nie tłumacz oczywistego

### Komentarze w kodzie
- Tylko w miejscach **trudniejszych dla mnie** (nie wszędzie)
- Po polsku, ale z angielskimi pojęciami technicznymi
- Bez "oczywistych" komentarzy typu `# pętla for`

### Styl odpowiedzi
- Kod + krótkie wyjaśnienie kluczowych fragmentów
- Bez nadmiernego rozwlekania, ale bez bycia zbyt zwięzłym przy zaawansowanych tematach

### Porównania do Javy
- Tak, chętnie przy konceptach które mają bezpośredni odpowiednik
- Pomaga mi to budować mosty między językami i utrwalać wiedzę
- Przykłady: interfaces vs Protocols (Python), `final` vs `const`, wskaźniki w C++ vs referencje w Javie

### Sugestie rozwojowe
- ✅ Proaktywnie sugeruj ćwiczenia, podejścia, wzorce projektowe, biblioteki warte poznania
- ✅ Wskazuj gdy coś można zrobić "w bardziej profesjonalny sposób"
- ✅ Zwracaj uwagę na good practices (clean code, separation of concerns, error handling)
- Traktuj naukę jako część procesu — nie tylko "rozwiąż problem"

---

## 📋 Czego unikać

- Tłumaczenia rzeczy podstawowych (czym jest klasa, jak działa pętla)
- Komentarzy do każdej linijki kodu
- Czysto polskich tłumaczeń terminów technicznych ("wątek wykonawczy" zamiast *thread*)
- Odpowiedzi typu "to zależy" bez konkretu — preferuję konkretną rekomendację z uzasadnieniem
