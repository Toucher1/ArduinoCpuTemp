#define LED1 3  // Пин для первого светодиода
#define LED2 4  // Пин для второго светодиода
#define LED3 5  // Пин для третьего светодиода

int lastTemp = -1; // Переменная для хранения последней температуры

void setup() {
  Serial.begin(9600); // Настройка последовательного порта
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  // Изначально выключаем все светодиоды
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    int temp = Serial.parseInt(); // Считываем температуру из последовательного порта

    // Если температура изменилась, обновляем светодиоды
    if (temp != lastTemp) {
      lastTemp = temp;

      // Управляем светодиодами в зависимости от температуры
      if (temp >= 40 && temp <= 55) {
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
      } else if (temp >= 56 && temp <= 69) {
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED3, LOW);
      } else if (temp >= 70) {
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, HIGH);
      }
    }
  }
}