from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit
import nvs

vochtigheidslevel = 0
# vochtigheidslevel = nvs.read_str('geheugen')


setScreenColor(0x111111)

Watering0 = unit.get(unit.WATERING, unit.PORTA)

#functie die de vochtigheid opslaat
# def opslaan()
  # lcd.clear(lcd.BLACK)
  # scherm_print('kaas')
    # vochtigheidslevel = Watering0.get_adc_value()
    # lcd.clear(lcd.BLACK)
    # M5.Lcd.drawString(vochtigheidslevel, 160, 120, 2)

def pomp_seconden(n):
  pomp_aan()
  wait(n)
  pomp_uit()

# functie die de pomp Watering0 aan zet
def pomp_aan():
  Watering0.set_pump_status(1)

# functie die de pomp Watering0 uit zet
def pomp_uit():
  Watering0.set_pump_status(0)

# functie die <text> in het midden van het scherm displayt.
def scherm_print(text): 
  lcd.text(lcd.CENTER, lcd.CENTER, text)








label0 = M5TextBox(50, 50, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
pauze = False

pomp_uit()

while True:
  watermeting = Watering0.get_adc_value()
  label0.setText(str(watermeting))

  if pauze:
    # HIER DINGEN DIE ALLEEN IN DE PAUZE GEBEUREN
    wait(0.5) # drie seconden wachten dan weer checken
    if btnB.wasPressed(): 
      pauze = False # stop met pauze houden
      lcd.clear(lcd.BLACK)
      scherm_print("en doorr")
  else:
    # HIER DINGEN DIE ALLEEN TIJDENS *NIET* PAUZE GEBEUREN
    if (watermeting > vochtigheidslevel):
      pomp_seconden(0.5)
    else:
      pomp_uit()

    if (btnB.wasPressed()):
      pomp_uit()
      lcd.clear(lcd.BLACK)
      scherm_print('pauze')
      pauze = True

    if btnA.wasPressed():
      vochtigheidslevel = Watering0.get_adc_value()
      nvs.write_str(str('geheugen'), vochtigheidslevel)
      lcd.clear(lcd.BLACK)
      scherm_print(str(vochtigheidslevel))
      
      


  wait(0.3)
  wait_ms(2)

  # , voor het einde van het programma:    




# NOTITIES
  # OBSERVATIES SENSOR IN PUUR WATER:
  # als de sensor DROOG is is de meting HOOG, rond ~2000
  # als de sensor NAT is   is de meting LAAG, rond ~1850
  # UPDATE:
  # als de sensor langere tijd NAT is (~5 min) dan gaat ie nog lager tot ~1750
  # als er een groter deel van de sensor nat is wordt de waarde NOG LAGER. ~1650
  # OBSERVATIES SENSOR IN NATTE AARDE:
  # aarde erg droog 2000
  # kleine hoeveelheid water veranderd naar 1700
  # optimale waarden 2000-1900
  #scherm groote 135 x 240
