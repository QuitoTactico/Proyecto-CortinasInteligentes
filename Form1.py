from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import plotly.graph_objects as go
import anvil.server

from datetime import datetime
from collections import deque

#colecciones para almacenar los datos de las gráficas
luz_values     = deque()
cortina_values = deque()
timestamps     = deque()

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

  #Se ejecuta cuando se presiona el botón [Modo]
  def dia_noche(self, **event_args):
    anvil.server.call("titilar")
    modo = anvil.server.call("dia_noche")
    print(modo)

  #Se ejecuta cuando se presiona el botón [Cortina]
  def encendido_apagado(self, **event_args):
    anvil.server.call("titilar")
    powermode = anvil.server.call("encendido_apagado")
    print(powermode)

  #Se ejecuta cuando se presiona el botón [Sensor]
  def toma_notoma(self, **event_args):
    anvil.server.call("titilar")
    toma = anvil.server.call("toma_notoma")
    print(toma)
     
  #Esta función es llamada cada segundo
  def timer_1_tick(self, **event_args):
    #Es necesario llamar a las conexiones globales para poder modificarlas
    global luz_values
    global cortina_values
    global timestamps

    #consultamos el valor lumínico del sol, cada que se ejecute la función
    luz       = anvil.server.call("get_luz")
    
    #consultamos el porcentaje de apertura de la cortina
    cortina   = anvil.server.call("get_cortina",luz)
    
    #consultamos la hora actual, para cada valor registrado
    timestamp = datetime.now().strftime("%H:%M:%S")

    #los metemos a todos en sus colecciones
    luz_values.append( luz )
    cortina_values.append( cortina )
    timestamps.append( timestamp )

    #filtramos para que sólo se almacenen los 20 valores más recientes
    if len(luz_values) >= 20:
      luz_values.popleft()
    if len(cortina_values) >= 20:
      cortina_values.popleft()
    if len(timestamps) >= 20:
      timestamps.popleft()

    #son para ver información de las variables del raspberry, en los labels
    self.mode_label.text = anvil.server.call('get_modo')
    self.powermode_label.text = anvil.server.call('get_powermode')
    self.toma_label.text = anvil.server.call('get_toma')

    #los valores de la última medición de luz, y el último output de cortina
    self.luz_label.text = f"{luz} lux" if luz != None else 'Sin datos'
    self.cortina_label.text = f"{cortina}%"

    #podemos graficar
    self.plot_luz.data = go.Scatter(x=list(timestamps) , y=list(luz_values))
    self.plot_luz.layout.title = "Luz ambiental (lux)" 

    self.plot_cortina.data = go.Scatter( x=list(timestamps) , y=list(cortina_values))
    self.plot_cortina.layout.title = "Apertura de cortina (%)" 

    
  # se ejecuta automáticamente cada que cambia el contenido del input en el conversor,
  # o si se presiona enter
  def conversor(self, **event_args):
    luz = self.conversor_input.text
    if luz != None:
      cortina   = anvil.server.call("conversor",luz)
      self.conversor_output.text = f"{cortina}%"
    else:
      self.conversor_output.text = None
     
    
