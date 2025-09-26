#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <Keypad.h>

// Variables for Keypad
const byte LINHAS = 4;
const byte COLUNAS = 4;

// Usuário definidos
char codigo_user[9];

//Teclado
const char TECLAS_MATRIZ[LINHAS][COLUNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte PINOS_LINHAS[LINHAS] = {D1, D2, D3, D4};
byte PINOS_COLUNAS[COLUNAS] = {D5, D6, D7, D8};

// Objeto do teclado  
Keypad teclado_personalizado = Keypad(makeKeymap(TECLAS_MATRIZ), PINOS_LINHAS, PINOS_COLUNAS, LINHAS, COLUNAS);

// Internet
const char* ssid = "Amigo Luci";
const char* password = "30081967";  

WiFiServer server(80);

void setup(){
  Serial.begin(9600);

  for (int i = 0; i < 8; i++) {
    int tipo = random(2); // 0 = número, 1 = letra
    if(tipo == 0){
      codigo_user[i] = '0' + random(10);
    }
    
    else{
      codigo_user[i] = 'A' + random(26);
    }
  }

  codigo_user[8] = '\0';

  Serial.print("Connecting");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi Conectada");

  HTTPClient http;
  WiFiClient client;

  Serial.print("IP do ESP: ");
  Serial.println(WiFi.localIP());

  http.begin(client, "http://192.168.3.14:5000/data");
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;

  doc["code"] = codigo_user;

  String payload;
  serializeJson(doc, payload);

  Serial.println(payload);
  int httpResponseCode = http.POST(payload);

  if(httpResponseCode > 0){
    Serial.print("Resposta HTTP: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println("Resposta do servidor:");
    Serial.println(response);
  }
  
  else{
    Serial.println(httpResponseCode);
    Serial.print("Erro no POST: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  delay(5000);
}

void loop(){
  
}