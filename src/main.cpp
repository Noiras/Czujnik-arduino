#include <Arduino.h>

// TODO: dodaj biblioteki sensorów, np.:
// #include <DHT.h>          // temperatura + wilgotność (DHT11/DHT22)
// #include <Adafruit_BMP280.h>  // ciśnienie + temperatura

// TODO: zdefiniuj stałe konfiguracyjne zamiast magic numbers w kodzie
// #define DHT_PIN 2
// #define DHT_TYPE DHT22
// #define BAUD_RATE 9600

// TODO: zadeklaruj obiekty sensorów tutaj (scope globalny, ale inicjalizuj w setup())
// DHT dht(DHT_PIN, DHT_TYPE);
// Adafruit_BMP280 bmp;

void setup()
{
  // TODO: Serial.begin(9600) — niezbędne do komunikacji z Pythonem
  // TODO: dht.begin(), bmp.begin() — inicjalizacja sensorów
  // TODO: sprawdź czy sensory odpowiadają (bmp.begin() zwraca false jeśli nie wykryto)
}

void loop()
{
  // TODO: odczytaj dane z sensorów i wyślij przez Serial w ustalonym formacie
  // Rekomendowany format: CSV "temp,humidity,pressure\n" — łatwy do parsowania w Pythonie
  // Przykład: Serial.print(temp); Serial.print(","); Serial.println(pressure);
  //
  // Alternatywa: JSON {"t":23.5,"h":45,"p":1013} — bardziej rozszerzalny, ale cięższy
  //
  // TODO: dodaj delay lub użyj millis() do kontrolowania częstotliwości wysyłania
  // millis() jest lepsze niż delay() — nie blokuje pętli (odpowiednik Timer w Javie)
}
