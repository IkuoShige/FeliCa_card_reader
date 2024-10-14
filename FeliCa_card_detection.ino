#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>

#include <SPI.h>
#include <PN532_SPI.h>
#include <PN532.h>

PN532_SPI pn532spi(SPI, 10);
PN532 nfc(pn532spi);

//PN532_I2C pn532i2c(Wire);
//PN532 nfc(pn532i2c);

uint8_t _prevIDm[8] = {0};
unsigned long _prevTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("FeliCaカードリーダーの初期化を開始します...");
  nfc.begin(); 
  
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.println("PN53xモジュールが見つかりません。接続を確認してください。");
    while (1);
  }
  
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX); 
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC); 
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);
  
  nfc.SAMConfig();
  Serial.println("PN532の初期化が完了しました。");
}

void loop() {
  uint8_t ret;
  uint16_t systemCode = 0x81E1;
  uint8_t requestCode = 0x01;
  uint8_t idm[8];
  uint8_t pmm[8];
  uint16_t systemCodeResponse;

  Serial.println("FeliCaカードを待っています...");
  ret = nfc.felica_Polling(systemCode, requestCode, idm, pmm, &systemCodeResponse, 5000);

  if (ret != 1) {
    Serial.println("カードが見つかりません。カードを近づけてください。");
    delay(1000);
    return;
  }

  if (memcmp(idm, _prevIDm, 8) == 0 && (millis() - _prevTime) < 3000) {
    Serial.println("同じカードが検出されました。3秒後に再試行します。");
    delay(1000);
    return;
  }

  Serial.println("カードが検出されました！");
  Serial.print("  IDm: ");
  nfc.PrintHex(idm, 8);
  Serial.print("  PMm: ");
  nfc.PrintHex(pmm, 8);
  Serial.print("  システムコード: ");
  Serial.println(systemCodeResponse, HEX);

  memcpy(_prevIDm, idm, 8);
  _prevTime = millis();

  // 学生証のサービスコードとブロックリストに変更
  uint16_t serviceCodeList[1];  // 学生証のサービスコード
  serviceCodeList[0] = 0x300B;
  uint16_t blockList[1];  // 読み出すブロック番号
  blockList[0] = 0x8000;
  Serial.println("version: 1.1.1");
  // 例： 0x2000番地から16バイト（ブロック）読み出す場合

  uint8_t blockData[1][16];  // 変更: 二次元配列として宣言

  ret = nfc.felica_ReadWithoutEncryption(1, serviceCodeList, 1, blockList, blockData);

  if (ret != 1) {
    Serial.println("データの読み取りに失敗しました。エラーコード: " + String(ret));
    Serial.println("カードがサポートしているサービスコードを確認してください。");
  } else {
    Serial.println("データの読み取りに成功しました！");
    Serial.print("読み取りデータ: ");
    nfc.PrintHex(blockData[0], 7);  // 変更: blockData[0]を使用
  }

  delay(1000);
}
