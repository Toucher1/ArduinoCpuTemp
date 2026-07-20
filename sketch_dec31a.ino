#define LED1 3  // Зелёный: нормальная температура
#define LED2 4  // Жёлтый: повышенная температура
#define LED3 5  // Красный: высокая температура

// Пороги переключения индикации (°C)
#define TEMP_WARN 56  // < этого значения — зелёный
#define TEMP_HOT  70  // >= этого значения — красный, между порогами — жёлтый

int lastTemp = -1; // Последняя обработанная температура (-1 = ещё не получена)

void setLeds(bool green, bool yellow, bool red) {
  digitalWrite(LED1, green ? HIGH : LOW);
  digitalWrite(LED2, yellow ? HIGH : LOW);
  digitalWrite(LED3, red ? HIGH : LOW);
}

void setup() {
  Serial.begin(9600); // Настройка последовательного порта
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  setLeds(false, false, false); // Изначально все светодиоды выключены
}

void loop() {
  if (Serial.available() > 0) {
    int temp = Serial.parseInt(); // Считываем температуру из порта

    // parseInt возвращает 0 при таймауте/мусоре — игнорируем такие значения
    if (temp <= 0) {
      return;
    }

    // Обновляем индикацию только при изменении температуры
    if (temp != lastTemp) {
      lastTemp = temp;

      if (temp < TEMP_WARN) {
        setLeds(true, false, false);   // Зелёный
      } else if (temp < TEMP_HOT) {
        setLeds(false, true, false);   // Жёлтый
      } else {
        setLeds(false, false, true);   // Красный
      }
    }
  }
}