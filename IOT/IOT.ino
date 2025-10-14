#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include "time.h"

// Negócios do fuso horário
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -3 * 3600;
const int daylightOffset_sec = 0;

char codigo_user[9];
bool deuCertoConexao = false;
bool alarmeTocado = false;

const char* ssid = "Amigo Luci";
const char* password = "30081967";  

WiFiServer server(80);

void setup(){
  Serial.begin(9600);

  for(int i = 0; i < 8; i++){
    int tipo = random(2);
    codigo_user[i] = (tipo == 0) ? '0' + random(10) : 'A' + random(26);
  }

  codigo_user[8] = '\0';

  Serial.print("Connecting");
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi Conectada");
  Serial.print("IP do ESP: ");
  Serial.println(WiFi.localIP());

  HTTPClient http;
  WiFiClient client;

  http.begin(client, "http://192.168.3.14:5000/data");
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;
  doc["code"] = codigo_user;

  String payload;
  serializeJson(doc, payload);

  int httpResponseCode = http.POST(payload);

  if(httpResponseCode > 0){
    Serial.print("Resposta HTTP: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println("Resposta do servidor:");
    Serial.println(response);
    deuCertoConexao = true;
  }
  
  else{
    Serial.println(httpResponseCode);
    Serial.print("Erro no POST: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  delay(5000);
}

void tocarAlarme(const char* nome){
  Serial.print("Alarme do remédio: ");
  Serial.println(nome);

  //Funcao dos negocio girar
}

void loop() {
  if(deuCertoConexao) {
    HTTPClient http;
    WiFiClient client;

    http.begin(client, "http://192.168.3.14:5000/mandarTudo");
    http.addHeader("Content-Type", "application/json");

    // Cria JSON para enviar
    StaticJsonDocument<200> doc;
    doc["message"] = "pleaseDaddy";

    String payload;
    serializeJson(doc, payload);

    int httpResponseCode = http.POST((uint8_t*)payload.c_str(), payload.length());
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Resposta do servidor:");
      Serial.println(response);

      StaticJsonDocument<2048> resDoc;
      DeserializationError error = deserializeJson(resDoc, response);

      if (!error && String(resDoc["status"].as<const char*>()) == "success") {
        JsonArray remedios = resDoc["message"].as<JsonArray>();

        struct tm timeinfo;
        if (getLocalTime(&timeinfo)) {
          char horaAtual[6];
          sprintf(horaAtual, "%02d:%02d", timeinfo.tm_hour, timeinfo.tm_min);

          bool alarmeDisparadoNoLoop = false;

          for (JsonObject rem : remedios) {
            const char* nome = rem["nome"];
            JsonArray horas = rem["horas"].as<JsonArray>();

            for (JsonVariant h : horas) {
              const char* horaDb = h.as<const char*>();
              if (strcmp(horaDb, horaAtual) == 0) {
                if (!alarmeTocado) {
                  tocarAlarme(nome);
                  alarmeDisparadoNoLoop = true;
                }
              }
            }
          }

          // Atualiza flag para não repetir o alarme no mesmo minuto
          alarmeTocado = alarmeDisparadoNoLoop;
          if (!alarmeDisparadoNoLoop) alarmeTocado = false;
        }
      } else {
        Serial.println("Erro ao interpretar JSON ou status inválido.");
      }
    } else {
      Serial.print("Erro no POST: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  }

  delay(5000); // Verifica a cada 5 segundos
}