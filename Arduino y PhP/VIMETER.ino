#include <WiFi.h>
#include <dht11.h>

// Configuración del DHT11
// Pin donde está conectado el DHT11
#define DHT11PIN 23
dht11 DHT11;
int buzzer = 14; // Pin al que está conectado el buzzer

// Configuración de red Wi-Fi
const char* ssid = ""; // Reemplaza con el nombre de tu red WiFi
const char* password = ""; // Reemplaza con el password de tu red WiFi

// Dirección IP del servidor
const char* server = ""; // Reemplaza con la IP de tu servidor

// ID del dispositivo
const char* id_dispositivo = "VMT_001"; // Cada VI-METER tiene su propio ID

// Crear el cliente WiFi
WiFiClient client;

void wifiConnect() {
    Serial.print("Conectando a la red WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("Conectado a Wi-Fi!");
    Serial.print("Dirección IP: ");
    Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
   delay(2000);
   Serial.println('\n');
   wifiConnect();
   Serial.println("Conectando con la base de datos...");
}

void loop() {
    // Leer temperatura y humedad del sensor
    Serial.println();
    int chk = DHT11.read(DHT11PIN);
    float temperature = DHT11.temperature;
    float humidity = DHT11.humidity;

    // Validar las lecturas
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Error al leer el sensor DHT11.");
        delay(2000);
        return;
    }

    // Imprimir los valores para depuración
    Serial.print("Temperatura: ");
    Serial.print((float)DHT11.temperature, 2);
    Serial.println(" °C");
    Serial.print("Humedad: ");
    Serial.print((float)DHT11.humidity, 2);
    Serial.println(" %");

    if (DHT11.humidity > 80.00 || DHT11.temperature > 30.0){
      tone(buzzer, 450);
      delay(500);
      noTone(buzzer); 
      delay(5000);
    }

    // Conectar al servidor y enviar los datos
    if (client.connect(server, 80)) {
        Serial.println("Conectado al servidor");

        // Crear la solicitud HTTP con los valores del sensor
        String url = "/testcode/dht11.php?temperature=" + String(temperature) + 
                     "&humidity=" + String(humidity) + 
                     "&id_dispositivo=" + String(id_dispositivo);

        client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                     "Host: " + server + "\r\n" +
                     "Connection: close\r\n\r\n");

        delay(100);

        // Leer la respuesta del servidor
        while (client.available()) {
            String line = client.readStringUntil('\r');
            Serial.print(line);
        }
        // Cerrar la conexión
        client.stop();
        Serial.println("Desconectado del servidor");
    } else {
        Serial.println("Conexión fallida al servidor");
    }
    // Esperar un tiempo antes de enviar de nuevo
    delay(20000);
}
