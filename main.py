'''
 [PARCIAL - CORTINAS INTELIGENTES v2.0]
  
hecho por:    Esteban Vergara Giraldo
              Jonathan Betancur Espinosa
             
manual de
fabricación:  https://docs.google.com/document/d/1S8KZpc69cQ6S1qoQciOljn6loe1zCqPxLhJy1a0WGjw/

link anvil:   https://cortinas-inteligentes.anvil.app/

'''
import anvil.pico
import uasyncio as a
from machine import Pin, ADC    # uso de pines digitales y análogos
from random import randint      # simulación de luz nocturna

UPLINK_KEY = "server_V6XYAKDSY2BV6XTRE7MOXHGF-M33JCTKEAWVOBO7S"

# Sólo se usa para mostrar que se usó un botón desde anvilworks.
led = Pin("LED", Pin.OUT, value=1)

#salidas digitales
dia      = Pin(17, Pin.OUT, value=1)
noche	 = Pin(16, Pin.OUT, value=0)
toma_led = Pin(18, Pin.OUT, value=1)

#entradas digitales (entran desde anvilworks
modo      = True # True = Dia       | False = Noche
powermode = True # True = Encendido | False = Apagado
toma_datos= True # True = Toma datos de luz | False = No toma datos de luz

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


# enciende y apaga el sistema de cortinas automáticas, aunque los datos se siguen tomando.
@anvil.pico.callable(is_async=True)
async def toma_notoma():
    global toma_datos
    toma_datos = not toma_datos
    
    if toma_datos:
        toma_led.value(1)
    else:
        toma_led.value(0)
    
    # retorna el cambio que se ha hecho, para ser impreso en la consola de anvilworks
    return "Ahora la cortina tomará datos de luz" if toma_datos else "Ahora la cortina NO tomará datos de luz"

# para obtener el valor actual del modo(Día/Noche)
@anvil.pico.callable(is_async=True)
async def get_modo():
    return "Día" if modo else "Noche"  # es mostrado por modo_label

# para obtener el valor actual del powermode(Encendido/Apagado)
@anvil.pico.callable(is_async=True)
async def get_powermode():
    return "Encendida" if powermode else "Apagada"  # es mostrado por powermode_label
    
# para obtener el valor actual del powermode(Encendido/Apagado)
@anvil.pico.callable(is_async=True)
async def get_toma():
    return "Toma datos" if toma_datos else "No toma datos"  # es mostrado por powermode_label    

# para obtener la medición análoga actual. Puede ser simulada con un potenciómetro
@anvil.pico.callable(is_async=True)
async def get_luz():
    if toma_datos:
        if modo:
            luz = luz_pin.read_u16()  # da valores entre 0 y 65025
        else:
            luz = randint(3000,5000)  # simula los bajos valores de luz que hay en la noche
            
        # retornamos el valor para ser graficado en plot_luz
        return luz
    else:
        return None


# dependiendo de la luz, dice qué tan abierta estará la cortina (porcentaje). 5 modos
@anvil.pico.callable(is_async=True)
async def get_cortina(luz):
    global cortina
    
    # si el sistema está apagado, no hay cambios en la cortina.
    # lo mismo si se dejaron de tomar datos de luz
    if powermode and toma_datos:
        
        # lo dividimos en 5 rangos de luz, a cada uno le corresponde un nivel de apertura para la cortina
        # a mayor luz, menor apertura
        if modo:  #es de día
            if 50000 < luz:
                cortina = 0
            elif 40000 <= luz and luz < 50000:
                cortina = 20
            elif 30000 <= luz and luz < 40000:
                cortina = 40
            elif 20000 <= luz and luz < 30000:
                cortina = 60
            elif 10000 <= luz and luz < 20000:
                cortina = 80
            elif 0 <= luz and luz < 10000:
                cortina = 100
                
        # pero en la noche, la cortina se cierra por privacidad        
        else:
            cortina = 0    
    
    # retornamos el valor para ser graficado en plot_cortina
    return cortina     

    
# una versión simplificada de get_cortina. Debían ser dos funciones diferentes, o el return se confundiría
@anvil.pico.callable(is_async=True)
async def conversor(luz_conversor):
    cortina_conversor = 0   # una variable diferente a la global
    
    if 50000 < luz_conversor:
        cortina_conversor = 0
    elif 40000 <= luz_conversor and luz_conversor < 50000:
        cortina_conversor = 20
    elif 30000 <= luz_conversor and luz_conversor < 40000:
        cortina_conversor = 40
    elif 20000 <= luz_conversor and luz_conversor < 30000:
        cortina_conversor = 60
    elif 10000 <= luz_conversor and luz_conversor < 20000:
        cortina_conversor = 80
    elif 0 <= luz_conversor and luz_conversor < 10000:
        cortina_conversor = 100
        
    return cortina_conversor



# se conecta a nuestro proyecto en anvilworks
anvil.pico.connect(UPLINK_KEY)


'''
    _                ___       _.--.    ----------- REQUERIMIENTOS: --------------
    \`.|\..----...-'`   `-._.-'_.-'`             Proyecto en AnvilWorks
    /  ' `         ,       _.-'                  Raspberry Pi Pico W
    )/' _/     \   `-_,   /                      Potenciómetro
    `-'" `"\_  ,_.-;_.-\_ ',                     2 LEDs
        _.-'_./   {_.'   ; /             
       {_.-``-'         {_/       
                                 
'''

