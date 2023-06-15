from tkinter import *
import sqlite3     #También importamos sqlite para trabajar con la base de datos. En este caso no empleamos el ORM.
from models import Producto


if __name__ == "__main__":
    ventana_grafica = Tk()       #Istanciamos la ventana de lla aplicación. En el ejemplo la llamamos "root".
    app = Producto(ventana_grafica)     #Creamos un objeto de esa clase para que se ejecuten los métodos de tKinter usados en ella.
    ventana_grafica.mainloop()      #Con este método logramos que la ventana permanezca abierta.