#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <Stepper.h>
#include "time.h"

// Negócios do fuso horário
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = -3 * 3600;
const int daylightOffset_sec = 0;

// Variável do alarme
const int stepsPerRevolution = 2048;

// Variáveis do alarme
int buzzer = D0;

// Variáveis aleatórias
char codigo_user[9];
bool deuCertoConexao = false;
bool alarmeTocado = false;

const char* ssid = "esp";
const char* password = "12345678";  

WiFiServer server(80);

String ultimaHoraTocada = "";

void setup(){
  Serial.begin(9600);
  pinMode(buzzer, OUTPUT);

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

  http.begin(client, "http://192.168.0.240:5000/data");
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

void tocarAlarme(const char* nome, const int compartimento){
  Serial.print("Alarme do remédio: ");
  Serial.println(nome);

  int passos = stepsPerRevolution;

  switch(compartimento){
    case 1: {
      Stepper stepperName1 = Stepper(stepsPerRevolution, D0, D1, D2, D3);
      stepperName1.setSpeed(15);

      while (passos > 0){
        int passoAtual = (passos >= 10) ? 10 : passos;
        stepperName1.step(passoAtual);
        passos -= passoAtual;
      }

      break;
    }

    case 2: {
      Stepper stepperName2 = Stepper(stepsPerRevolution, D0, D1, D4, D5);
      stepperName2.setSpeed(15);
      
      while (passos > 0){
        int passoAtual = (passos >= 10) ? 10 : passos;
        stepperName2.step(passoAtual);
        passos -= passoAtual;
      }

      break;
    }

    case 3: {
      Stepper stepperName3 = Stepper(stepsPerRevolution, D0, D1, D6, D7);
      stepperName3.setSpeed(15);

      while (passos > 0){
        int passoAtual = (passos >= 10) ? 10 : passos;
        stepperName3.step(passoAtual);
        passos -= passoAtual;
      }

      break;
    }
  }

  for(int i = 0; i < 5; i++){
    tone(buzzer, 500);
    delay(1000);
    noTone(buzzer);
    delay(1000);
  }

  Serial.println("Alarme finalizado.");
}

void loop(){
  if(deuCertoConexao){
    HTTPClient http;
    WiFiClient client;

    http.begin(client,"http://192.168.0.240:5000/mandarTudo");
    http.addHeader("Content-Type","application/json");
    StaticJsonDocument<200> doc;
    doc["message"]="pleaseDaddy";
    String payload;
    serializeJson(doc,payload);
    int httpResponseCode=http.POST((uint8_t*)payload.c_str(),payload.length());

    if(httpResponseCode > 0){
      String response=http.getString();
      Serial.println("Resposta do servidor:");
      Serial.println(response);
      StaticJsonDocument<2048> resDoc;
      DeserializationError error=deserializeJson(resDoc,response);

      if(!error && String(resDoc["status"].as<const char*>()) == "success"){
        JsonArray remedios = resDoc["message"].as<JsonArray>();
        struct tm timeinfo;

        if(getLocalTime(&timeinfo)){
          char horaAtual[6];
          sprintf(horaAtual,"%02d:%02d",timeinfo.tm_hour,timeinfo.tm_min);
          bool alarmeDisparadoNoLoop=false;

          for(JsonObject rem:remedios){
            const char* nome=rem["nome"];
            const int compartimento=rem["compartimento"];
            JsonArray horas=rem["horas"].as<JsonArray>();

            for(JsonVariant h:horas){
              const char* horaDb=h.as<const char*>();

              if(strcmp(horaDb,horaAtual) == 0){
                if(ultimaHoraTocada != String(horaAtual)){
                  tocarAlarme(nome,compartimento);
                  ultimaHoraTocada=String(horaAtual);
                  alarmeDisparadoNoLoop=true;
                }
              }
            }
          }
        }
      }
      
      else{
        Serial.println("Erro ao interpretar JSON ou status inválido.");
      }
    }
    
    else{
      Serial.print("Erro no POST: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  }

  delay(5000);
}