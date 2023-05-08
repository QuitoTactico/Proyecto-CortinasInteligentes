'''
 [PARCIAL - CORTINAS INTELIGENTES]
  
hecho por:    Esteban Vergara Giraldo
              Jonathan Betancur Espinosa
             
manual de
fabricación:  https://docs.google.com/document/d/1S8KZpc69cQ6S1qoQciOljn6loe1zCqPxLhJy1a0WGjw/

'''
import anvil.pico
import uasyncio as a
from machine import Pin, ADC    # uso de pines digitales y análogos
from random import randint      # simulación de luz nocturna

UPLINK_KEY = "server_V6XYAKDSY2BV6XTRE7MOXHGF-M33JCTKEAWVOBO7S"

# Sólo se usa para mostrar que se usó un botón desde anvilworks.
led = Pin("LED", Pin.OUT, value=1)

#salidas digitales
dia   = Pin(17, Pin.OUT, value=1)
noche = Pin(16, Pin.OUT, value=0)

#entradas digitales (entran desde anvilworks
modo      = True # True = Dia       | False = Noche
powermode = True # True = Encendido | False = Apagado

#entrada análoga
luz_pin = ADC(28)

#salida análoga (también mostrada en anvil)
cortina_pin = ADC(27)
cortina = 50    #inicializamos la variable en un valor intermedio

#------------[FUNCIONES]---------------------

#Sólo para ver al led integrado titilar cuando se presione un botón
@anvil.pico.callable(is_async=True)
async def titilar():
    for _ in range(10):
        led.toggle()
        sleep(0.1)


# alterna entre noche y día
@anvil.pico.callable(is_async=True)
async def dia_noche():
    global modo
    modo = not modo
    
    # dependiendo de si es de día o de noche, se enciende un led o el otro
    # Día (17) | Noche (16)
    if modo:
        dia.value(1)
        noche.value(0)
    else:
        dia.value(0)
        noche.value(1)
    
    # retorna el cambio que se ha hecho, para ser impreso en la consola de anvilworks
    return "Modo día" if modo else "Modo noche"


# enciende y apaga el sistema de cortinas automáticas, aunque los datos se siguen tomando.
@anvil.pico.callable(is_async=True)
async def encendido_apagado():
    global powermode
    powermode = not powermode
    
    # cuando el sistema de automatización se apaga, el led integrado deja de brillar
    if powermode:
        led.value(1)
    else:
        led.value(0)
    
    # retorna el cambio que se ha hecho, para ser impreso en la consola de anvilworks
    return "La cortina automática ha sido encendida" if powermode else "La cortina automática ha sido apagada"


# para obtener el valor actual del modo(Día/Noche)
@anvil.pico.callable(is_async=True)
async def get_modo():
    return "Día" if modo else "Noche"  # es mostrado por modo_label

# para obtener el valor actual del powermode(Encendido/Apagado)
@anvil.pico.callable(is_async=True)
async def get_powermode():
    return "Encendida" if powermode else "Apagada"  # es mostrado por powermode_label
    

# para obtener la medición análoga actual. Puede ser simulada con un potenciómetro
@anvil.pico.callable(is_async=True)
async def get_luz():
    