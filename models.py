from tkinter import *        #Impotamos la librería del Framework a utilizar. Con el asterisco seleccionamos todo.
from tkinter import ttk
import sqlite3       #También importamos sqlite para trabajar con la base de datos. En este caso no empleamos el ORM.


class Producto():

    db = "database/productos.db"

    def __init__(self, ventana_grafica):
        self.ventana_grafica = ventana_grafica
        self.ventana_grafica.title("App Gestor de Productos")  # Con esta instrucción ponemos el nombre a la ventana.
        self.ventana_grafica.resizable(1,1)  # Aqui habilitamos el que podamos cambiar el tamaño de la ventana y agrandarla.
        self.ventana_grafica.wm_iconbitmap("recursos/icon.ico")   #Cambiamos el icono de la ventana. Usamos una "imagen.ico"

        #Creamos el primer "Frame" con el método "LabelFrame()" y le pasamos por parámetro (1) donde se va a ejecutar. El segundo
        #parámetro es el título.
        frame = LabelFrame(self.ventana_grafica, text="Registrar un Producto")

        #Con el método ".grid()" le indicamos la posisión por parámetro (1ª y 2ª). El tamaño del Frame (3ª).
        #Y la separación entre las columnas en pixeles (4ª).
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Creamos la "Label" de Nombre (una "Label" es un texto impreso por pantalla) y el "Entry" o cajon de texto (input).
        # Usamos el método "Label()" para crearla y le pasamos por parámetro donde queremos que se cree (1ª frame), el texto que
        #uqeremos que imprima (2ª text)
        self.nombre_label = Label(frame, text="Nombre: ")   #"Label" nos imprime un texto (como un print).
        self.nombre_label.grid(row=1, column=0)   #Invocamos el método ".grid()" en nuestro Label para indicarle su posición.
        self.nombre_entry = Entry(frame)  #Para crear la entrada por pantalla (input) creamos un objeto de la clase "Entry".
        self.nombre_entry.focus()    #Con ".focus()" logramos que al entrar a la aplicación el foco se centre en este "entry".
        self.nombre_entry.grid(row=1, column=1)   #Por último para el "entry", le damos una ubicación en el "frame".

        self.precio_label = Label(frame, text="Precio: ")
        self.precio_label.grid(row=2, column=0)
        self.precio_entry = Entry(frame)
        self.precio_entry.grid(row=2, column=1)

        #Aqui aproveche para añadir las mejoras del pdf de incluir la "categoría" y el "stock".
        self.categoria_label = Label(frame, text="Categoría: ")
        self.categoria_label.grid(row=3, column=0)
        self.categoria_entry = Entry(frame)
        self.categoria_entry.grid(row=3, column=1)

        self.stock_label = Label(frame, text="Stock: ")
        self.stock_label.grid(row=4, column=0)
        self.stock_entry = Entry(frame)
        self.stock_entry.grid(row=4, column=1)


        #A continuación añadimos el botón. Antes hemos usado "Label" y "Entry" directamente porque usabamos la libreria "tk".
        #Sin embargo, el botón que vamos a añadir acontinuación es de la librería "ttk" que es la más moderna. Por eso es diferente.
        self.aniadir_boton = ttk.Button(frame, text="Guardar Producto", command = self.add_producto)
        #¡¡->Importante<-!! El parámetro (command) se le pasa la función creada de añadir producto pero ¡¡sin paréntesis()!!

        #Con el parámetro "columnspan" del ".grid()" le indicamos cuantas columnas debe ocupar.
        #Con "sticky" conseguimos que rellene las columnas. Se le indican como tiene que rellenarla como una brújula.
        self.aniadir_boton.grid(row=5, columnspan= 2, sticky= W + E)  #Le hemos dicho que rellene del oeste al este.


        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky= W + E)

        #Tabla de Producto.
        #Creamos un objeto de la clase "Style()" para poder usar sus atributos y asi cambiar el estilo del texto. "estilo_nuevo" es una variable propia.
        style = ttk.Style()
        style.configure("estilo_nuevo.Treeview", highlightthickness=0, bd=0, font=('Calibri',11))  #Se modifica la fuente de la tabla
        style.configure("estilo_nuevo.Treeview.Heading", font=('Calibri', 13, 'bold'))  #Se modifica la fuente de las cabeceras
        style.layout("estilo_nuevo.Treeview", [('estilo_nuevo.Treeview.treearea', {'sticky':'nswe'})])  #Eliminamos los bordes

        #Estructura de Tabla.
        # Con el método "Treeview" creamos la tabla. Le indicamos por parámetro la altura (1ª height) y el  número de columnas (2ª).
        #¡¡-->Fallo<--!!: Aqui tuve el problema de que al cambiar en el parámetro "colums=2" por "colums=4" aun así no me dejaba añadir
        #las dos columnas nuevas a la tabla. Buscando por internet encontre que le tengo que introducir a ese parámetro una lista de
        #elementos "str", tantos como columnas necesite, pero tengo el problema de que me cambia el tamaño del botón "guardar".
        self.tabla = ttk.Treeview(frame, height=20, columns=[f"#{n}" for n in range(1, 4)], style="estilo_nuevo.Treeview")

        #Siempre indicamos con el método ".grid()" la ubicación de la esquina superior izquierda. Y le indicamos las columnas a ocupar.
        self.tabla.grid(row=6, column=0, columnspan=4)

        #Ahora creamos las cabeceras de cada columna de la tabla donde se almacenan los productos.
        #Usaremos el método ".heading()" y le pasaremos por parámetro: (1ª) la posisión, El parámetro "anchor" es para alinear el texto.
        self.tabla.heading("#0", text="Nombre:", anchor=CENTER)
        self.tabla.heading("#1", text="Precio:", anchor=CENTER)
        self.tabla.heading("#2", text="Categoría", anchor=CENTER)
        self.tabla.heading("#3", text="Stock:", anchor=CENTER)

        #Botón de Eliminar y el de Editar.
        s = ttk.Style()
        s.configure('my.TButton', font= ('Calibri', 14, 'bold'))

        # Los situamos debajo de la tabla (row=7). Y les pasamos a cada uno los comandos que queramos que se ejecuten cuando se pulsen.
        self.eliminar_boton = ttk.Button(text="Eliminar", style= 'my.TButton', command=self.del_producto)
        self.eliminar_boton.grid(row=7, column=0, sticky=W + E)

        self.editar_boton = ttk.Button(text="Editar", style='my.TButton', command=self.edit_producto)
        self.editar_boton.grid(row=7, column=1, sticky=W + E)  #Este lo situamos a la derecha del otro  (column=1).

        #Invocamos al método creado ".get_productos()".
        self.get_productos()


    def db_consulta(self, consulta, parametros=()):   #Los parámetros son un "str" y una tupla. Por el método execute.
        with sqlite3.connect(self.db) as conexion:  #Con "with" esto logramos una conexión con la base al igual que con los ficheros.
            cursor = conexion.cursor()   #Este método "cursor" nos permite interactuar con la base.
            resultado = cursor.execute(consulta, parametros)   #Con el método "execute()" ejecutamos la consulta a db.
            conexion.commit()   #Y como siempre terminamos la interacción con la db con el método ".commit()" para que se ejecute.
        return resultado

    def get_productos(self):   #Con esta función vamos a enviar una consulta que me entregue lso productos de la db.

        registros_actuales = self.tabla.get_children()   #Con este método creamos un registro de lso valores actuales.
        for row in registros_actuales:
            self.tabla.delete(row)    #Con esto procedemos a recorrer el registro y a borrar los valores actuales.
        #Esto es necesario, ya que si ejecutamos el método ".get_productos()" habiendo registros en la tabla, se creara un error
        #al intentar sobreescribir posisiones de filas en las que ya existen valores.

        query = "SELECT * FROM producto ORDER BY nombre DESC"   #Guardamos la consulta en una variable.
        registros = self.db_consulta(query)   #Usamos el método creado antes y le pasamos por parámetro la consulta (query).
        for i in registros:
            print(i)
            # Parámetros: 1ª.En este caso lo asignamos vacío, lo que significa que no hereda de nadie. 2ª.Es el índice por el que
            #queremos que empiece. 3ª.Le enviamos en la variable "text" la posision en la tupla del "nombre" del producto.
            #4.En esta variable (value) le indicamos la posisión en la tupla del "precio", seguido de dicho índice usamos ":"
            #para indicarle que muestre el valor del resto de columnas, en este caso serian "categoría" y "stock".
            self.tabla.insert("", 0, text=i[1], values=i[2:])
        #Cuando llegue al método ".execute()" es cuando realmente se va a ejecutar la consulta.

    def validacion_nombre(self):   #Leera su cajon de texto (nombre) y realizara sus comprovaciones.
        #Con el método "get()" recogemos el valor introducido en el cajon de texto. Usamos la variable con la que creamos dicho cajón.
        nombre_introducido = self.nombre_entry.get()

        return len(nombre_introducido) != 0   #Si el tamaño del valor introducido es igual que 0 esta función no retornara nada.
        #Esta comprovación se asegura de que el cajón no se quede vacío, ya que programamos los valores de las filas para que
        #no aceptaran valores vacios, y provocaría un error.

    def validacion_precio(self):
        precio_introducido = self.precio_entry.get()
        return len(precio_introducido) != 0

    def validacion_categoria(self):
        categoria_introducida = self.categoria_entry.get()
        return len(categoria_introducida) != 0

    def validacion_stock(self):
        stock_introducido = self.stock_entry.get()
        return len(stock_introducido) != 0

    def add_producto(self):
        #Con la siguiente condición nos aseguramos de que ningún valor introducido sea nulo, ya que si una sola validación
        #devuelve "False", no se ejecutara el código del condicional.
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_categoria() and self.validacion_stock():
            #-->¡¡Importante!!<-- En el "INSERT" nombramos como "NULL" a la posisión de "ID", ya que como es autoincremental,
            #si no lo nombramos de esta manera nos dara error. Al resto de columnas les hacemos referencia con "?", que después
            #se sustituirán por variables.
            instruccion_insert = "INSERT INTO producto VALUES(NULL, ?, ?, ?, ?)"

            #En la variable "parametros", introduciremos los ".get()" de cada valor en el orden que queramos que se introduzca en el "INSERT".
            parametros = (self.nombre_entry.get(), self.precio_entry.get(), self.categoria_entry.get(), self.stock_entry.get())
            self.db_consulta(instruccion_insert, parametros)
            print("Datos guardados.")
            self.mensaje["text"] = "Datos guardados."

            #print(self.nombre_entry.get())
            #print(self.precio_entry.get())->Estas impresiones de pantalla es solo para confirmar que se llega al interior de if.
            #print(self.categoria_entry.get())
            #print(self.stock_entry.get())

        else:   #En caso de que falte por introducir una valor a alguno de los campos, se mostraran los siguientes mensajes.
            print("Uno de los valores introducidos no es correcto, por favor intentelo de nuevo. Le recordamos que debe introducir algun valor, ya que todos los campos son obligatorios.")
            self.mensaje["text"] = "Uno de los valores introducidos no es correcto, por favor intentelo de nuevo. Le recordamos que debe introducir algun valor, ya que todos los campos son obligatorios."

        #Con el método ".get_productos()" borraremos los datos actuales y sobreescribimos la tabla para que nos aparezcan las
        #filas nuevas introducidas alfinal de este método ".add_producto()".
        self.get_productos()

    def del_producto(self):
        #El método ".item()" nos devuelve el registro entero.Y ".selection()" nos devuelve la fila seleccionada en diccionario.
        #Como nos devuelve un diccionario, accedemos por la clave a un elemento para usarlo en filtrar (en este caso el nombre)
        nombre = self.tabla.item(self.tabla.selection())["text"]
        filto_eliminacion = "DELETE FROM producto WHERE nombre = ?"
        #Usamos el método creado "db_consulta" y le pasamos la consulta de eliminación y la variable "nombre" que hace referencia
        #al nombre de la fila. Asi en la consulta sustituye la "?" por la variable que la usa para filtrar.
        self.db_consulta(filto_eliminacion, (nombre,))   #Le pasamos "nombre" como una tupla ya que es los parámetros se le pasan asi.
        self.get_productos()  #Lo volvemos a invocar para que me actualice de nuevo la tabla.


    def edit_producto(self):
        self.mensaje['text'] = ''  # Mensaje inicialmente vacio
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return
        nombre = self.tabla.item(self.tabla.selection())['text']  #Igual que en "delete" aqui accedemos al nombre de la fila de esa manera.
        old_precio = self.tabla.item(self.tabla.selection())['values'][0] # El precio se encuentra dentro de una lista.
        old_categoria = self.tabla.item(self.tabla.selection())['values'][1]
        old_stock = self.tabla.item(self.tabla.selection())['values'][2]

        self.ventana_editar = Toplevel()  # Crear una ventana por delante de la principal con "Toplevel()"
        self.ventana_editar.title = "Editar Producto"  # Titulo de la ventana nueva
        self.ventana_editar.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0, 0)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico') # Icono de la ventana

        titulo = Label(self.ventana_editar, text='Edición de Productos', font=('Calibri', 50, 'bold'))
        titulo.grid(column=0, row=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto")  #frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_anituguo = Label(frame_ep, text="Nombre antiguo: ")  #Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre_anituguo.grid(row=2, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly')
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep)
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio


        # Label Precio antiguo
        self.etiqueta_precio_anituguo = Label(frame_ep, text="Precio antiguo: ")  #Etiqueta de texto ubicada en el frame
        self.etiqueta_precio_anituguo.grid(row=4, column=0)  # Posicionamiento a traves de grid

        #Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo= Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio), state='readonly')
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=5, column=0)

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep)
        self.input_precio_nuevo.grid(row=5, column=1)


        # Label Categoría antigua
        self.etiqueta_categoria_anitugua = Label(frame_ep, text="Categoría antigua: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria_anitugua.grid(row=6, column=0)  # Posicionamiento a traves de grid

        # Entry Categoría antiguo (texto que no se podra modificar)
        self.input_categoria_antigua = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),state='readonly')
        self.input_categoria_antigua.grid(row=6, column=1)

        # Label Categoría nuevo
        self.etiqueta_categoria_nueva = Label(frame_ep, text="Categoria nueva: ")
        self.etiqueta_categoria_nueva.grid(row=7, column=0)

        # Entry Categoría nuevo (texto que si se podra modificar)
        self.input_categoria_nueva = Entry(frame_ep)
        self.input_categoria_nueva.grid(row=7, column=1)


        # Label Stock antigua
        self.etiqueta_stock_anituguo = Label(frame_ep, text="Stock antiguo: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_stock_anituguo.grid(row=8, column=0)  # Posicionamiento a traves de grid

        # Entry Stock antiguo (texto que no se podra modificar)
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock), state='readonly')
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nueva: ")
        self.etiqueta_stock_nuevo.grid(row=9, column=0)

        # Entry Stock nuevo (texto que si se podra modificar)
        self.input_stock_nuevo = Entry(frame_ep)
        self.input_stock_nuevo.grid(row=9, column=1)


        # Boton Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", command=lambda:
        self.actualizar_productos(self.input_nombre_nuevo.get(), self.input_nombre_antiguo.get(),
        self.input_precio_nuevo.get(), self.input_precio_antiguo.get(), self.input_categoria_nueva.get(),
        self.input_categoria_antigua.get(), self.input_stock_nuevo.get(), self.input_stock_antiguo.get()))

        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W + E)

    def actualizar_productos(self, nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio, nueva_categoria,
                             antigua_categoria, nuevo_stock, antiguo_stock):
        producto_modificado = False
        query = 'UPDATE producto SET nombre = ?, precio = ?, categoría = ?, stock = ? WHERE nombre = ? AND precio = ? AND categoría = ? AND stock = ?'
        """if nuevo_nombre != '' and nuevo_precio != '':
            # Si el usuario escribe nuevo nombre y nuevo precio, se cambian ambos
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '':
            # Si el usuario deja vacio el nuevo precio, se mantiene el pecio anterior
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '':
            # Si el usuario deja vacio el nuevo nombre, se mantiene el nombre anterior
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock)
            producto_modificado = True"""

        if nuevo_nombre != '' and nuevo_precio != '' and nueva_categoria != '' and nuevo_stock != '':
            parametros = (nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock, antiguo_nombre, antiguo_precio,
                          antigua_categoria, antiguo_stock)
            producto_modificado = True


        if (producto_modificado):
            self.db_consulta(query, parametros)  # Ejecutar la consulta
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} ha sido actualizado conéxito'.format(antiguo_nombre) # Mostrar mensaje para el usuario
            self.get_productos()  # Actualizar la tabla de productos
        else:
            self.ventana_editar.destroy()  # Cerrar la ventana de edicion de productos
            self.mensaje['text'] = 'El producto {} NO ha sido actualizado; se debe rellenar todos los campos para que se actualice'.format(antiguo_nombre)
            # Mostrar mensaje para el usuario