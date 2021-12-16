import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from time import perf_counter

from RutinaVicsek import ActualizarFlocking

N_particulas = 500 #Numero de particulas
lx, ly =  20.0, 20.0 #Dimensiones de la caja
r = min(lx,ly)/max(lx,ly) #Radio de vecindad
dt = 0.1 #Intervalo de tiempo
v0 = 1.0 #Magnitud de velocidad
Ruido = 1.5 #factor de Ruido

Dtype = np.float64

x, y = np.random.uniform(2.0*lx/4.0, 4.0*lx/6.0, (N_particulas,1)), np.random.uniform(2.0*ly/6.0, 4.0*ly/6.0, (N_particulas,1))
Pos = np.concatenate([x,y], axis=1)
theta = np.random.uniform(-np.pi, np.pi, (N_particulas,1))
vx, vy = v0*np.cos(theta), v0*np.sin(theta)
Velocidad = np.concatenate([vx,vy], axis=1)

FPS = 0
#Creating the main figure within its subplots
pg.setConfigOption("background", "k")
pg.setConfigOption("foreground", "w")
ventana = pg.GraphicsLayoutWidget(show=True, title=f"Simulación de modelo de Ising, {FPS=}",size=(1200,700))

string_constant_data = "N={0}, <font>&eta;<font>={1:.3f}, v<sub>0</sub>={2:.3f}, dt={3:.3f}".format(N_particulas, Ruido, v0, dt)

PlotParticulas = ventana.addPlot(col=0 ,rowspan=2,
labels={"bottom":"Posición X", "left":"Posición Y"}, title=string_constant_data)
PlotParticulas.setXRange(0,lx)
PlotParticulas.setYRange(0,ly)
PlotParticulas.setAspectLocked(True, ratio=1)
PlotParticulas.setMouseEnabled(x=False, y=False)
PlotParticulas.hideButtons()

PuntosParticulas = PlotParticulas.plot(Pos[:,0], Pos[:,1], pen=None, symbol="o", symbolPen=None, 
pxMode=False, symbolSize = min(lx,ly)/100, symbolBrush=pg.mkBrush(color="w"))

timer = QtCore.QTimer()
timer.setSingleShot(True)
TiempoActualizar = perf_counter()
transcurrido = 0.0

#Inicia utilizando el parametro de ruido para simular las particulas y su dinamica   
def ActualizarEstadoParitculas():
   global Pos, Velocidad, theta, TiempoActualizar, transcurrido

   thetaCopia = np.copy(theta)
   ActualizarFlocking( Ruido,  dt,  v0,  lx,  ly,  r, Pos, Velocidad, theta, thetaCopia)

   PuntosParticulas.setData(Pos[:,0], Pos[:,1])
   string_constant_data = "N={0}, <font>&eta;<font>={1:.3f}, v<sub>0</sub>={2:.3f}, dt={3:.3f}".format(N_particulas, Ruido, v0, dt)
   PlotParticulas.setTitle(string_constant_data)

   TiempoAct = perf_counter()
   TiempoTrans = TiempoAct - TiempoActualizar
   TiempoActualizar = TiempoAct
   transcurrido = transcurrido*0.9 + TiempoTrans*0.1
   FPS = int(1.0/transcurrido)
   ventana.setWindowTitle(f"Simulación de modelo de Ising, {FPS=}")

   timer.start()

timer.timeout.connect(ActualizarEstadoParitculas)
ActualizarEstadoParitculas()

if __name__=="__main__":
   pg.exec()