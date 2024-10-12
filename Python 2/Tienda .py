import csv
from colorama import Fore, Style, init
from datetime import datetime

# Inicializar colorama
init(autoreset=True)

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad


class Producto:
    def __init__(self, nombre, precio, cantidad):
        self._nombre = nombre
        self._precio = precio
        self._cantidad = cantidad

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if not value:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, value):
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = value

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("La cantidad debe ser un entero no negativo")
        self._cantidad = value
        
class Cliente:
    def __init__(self, nombre, compras=None):
        self.nombre = nombre
        self.compras = compras or []

class Tienda:
    def __init__(self):
        self.productos = []
        self.clientes = []
        self.cargar_datos()

    def agregar_producto(self, nombre, precio, cantidad):
        # Merging similar products
        existing_product = next((p for p in self.productos if p.nombre.lower() == nombre.lower()), None)
        if existing_product:
            existing_product.cantidad += cantidad
            existing_product.precio = (existing_product.precio + precio) / 2  # Average price
            print(f"{Fore.GREEN}Producto '{nombre}' actualizado en la tienda.")
        else:
            producto = Producto(nombre, precio, cantidad)
            self.productos.append(producto)
            print(f"{Fore.GREEN}Producto '{nombre}' agregado a la tienda.")

    def actualizar_producto(self, nombre, nuevo_precio, nueva_cantidad):
        producto = next((p for p in self.productos if p.nombre.lower() == nombre.lower()), None)
        if producto:
            producto.precio = nuevo_precio
            producto.cantidad = nueva_cantidad
            print(f"{Fore.BLUE}Producto '{nombre}' actualizado.")
        else:
            print(f"{Fore.RED}Producto '{nombre}' no encontrado en la tienda.")

    def eliminar_producto(self, nombre):
        self.productos = [p for p in self.productos if p.nombre.lower() != nombre.lower() or p.cantidad > 0]
        print(f"{Fore.BLUE}Producto '{nombre}' eliminado de la tienda.")

    def vender_producto(self, nombre_producto, cantidad, nombre_cliente):
        producto = next((p for p in self.productos if p.nombre.lower() == nombre_producto.lower()), None)
        if not producto:
            print(f"{Fore.RED}Producto '{nombre_producto}' no encontrado en la tienda.")
            return

        if producto.cantidad < cantidad:
            print(f"{Fore.RED}Cantidad insuficiente de '{nombre_producto}' en stock.")
            return

        cliente = next((c for c in self.clientes if c.nombre == nombre_cliente), None)
        if not cliente:
            cliente = Cliente(nombre_cliente)
            self.clientes.append(cliente)

        producto.cantidad -= cantidad
        fecha_compra = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cliente.compras.append((nombre_producto, cantidad, fecha_compra))
        print(f"{Fore.BLUE}Vendido {cantidad} {nombre_producto}(s) a {nombre_cliente}")

    def mostrar_inventario(self):
        print(f"\n{Fore.YELLOW}Inventario Actual:")
        for producto in self.productos:
            print(f"{Fore.CYAN}{producto.nombre}: Precio: ${producto.precio:.2f}, Cantidad: {producto.cantidad}")

    def mostrar_clientes(self):
        print(f"\n{Fore.YELLOW}Historial de Compras de Clientes:")
        for cliente in self.clientes:
            print(f"{Fore.MAGENTA}{cliente.nombre}:")
            for compra in cliente.compras:
                print(f"  {Fore.CYAN}{compra[0]}: Cantidad: {compra[1]}, Fecha: {compra[2]}")

    def guardar_datos(self):
        with open('productos.csv', 'w', newline='') as archivo:
            escritor = csv.writer(archivo)
            for producto in self.productos:
                escritor.writerow([producto.nombre, producto.precio, producto.cantidad])

        with open('clientes.csv', 'w', newline='') as archivo:
            escritor = csv.writer(archivo)
            for cliente in self.clientes:
                escritor.writerow([cliente.nombre] + [f"{c[0]},{c[1]},{c[2]}" for c in cliente.compras])

    def cargar_datos(self):
        try:
            with open('productos.csv', 'r') as archivo:
                lector = csv.reader(archivo)
                self.productos = [Producto(fila[0], float(fila[1]), int(fila[2])) for fila in lector]
        except FileNotFoundError:
            print(f"{Fore.YELLOW}No se encontraron datos de productos existentes. Iniciando con un inventario vacío.")

        try:
            with open('clientes.csv', 'r') as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    cliente = Cliente(fila[0])
                    cliente.compras = [(c.split(',')[0], int(c.split(',')[1]), c.split(',')[2]) for c in fila[1:]]
                    self.clientes.append(cliente)
        except FileNotFoundError:
            print(f"{Fore.YELLOW}No se encontraron datos de clientes existentes. Iniciando con una lista de clientes vacía.")

def main():
    tienda = Tienda()

    while True:
        print(f"\n{Fore.GREEN}1. Agregar Producto")
        print(f"{Fore.BLUE}2. Actualizar Producto")
        print(f"{Fore.CYAN}3. Eliminar Producto")
        print(f"{Fore.MAGENTA}4. Vender Producto")
        print(f"{Fore.YELLOW}5. Mostrar Inventario")
        print(f"{Fore.RED}6. Mostrar Clientes")
        print(f"{Fore.WHITE}7. Guardar y Salir")

        opcion = input(f"{Style.RESET_ALL}Ingrese su opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del producto: ")
            try:
                precio = float(input("Ingrese el precio del producto: "))
                cantidad = int(input("Ingrese la cantidad del producto: "))
                tienda.agregar_producto(nombre, precio, cantidad)
            except ValueError:
                print(f"{Fore.RED}Entrada inválida. Asegúrese de ingresar números para precio y cantidad.")
        elif opcion == '2':
            nombre = input("Ingrese el nombre del producto a actualizar: ")
            try:
                nuevo_precio = float(input("Ingrese el nuevo precio del producto: "))
                nueva_cantidad = int(input("Ingrese la nueva cantidad del producto: "))
                tienda.actualizar_producto(nombre, nuevo_precio, nueva_cantidad)
            except ValueError:
                print(f"{Fore.RED}Entrada inválida. Asegúrese de ingresar números.")
        elif opcion == '3':
            nombre = input("Ingrese el nombre del producto a eliminar: ")
            tienda.eliminar_producto(nombre)
        elif opcion == '4':
            nombre = input("Ingrese el nombre del producto: ")
            try:
                cantidad = int(input("Ingrese la cantidad a vender: "))
                cliente = input("Ingrese el nombre del cliente: ")
                tienda.vender_producto(nombre, cantidad, cliente)
            except ValueError:
                print(f"{Fore.RED}Entrada inválida. Asegúrese de ingresar un número para la cantidad.")
        elif opcion == '5':
            tienda.mostrar_inventario()
        elif opcion == '6':
            tienda.mostrar_clientes()
        elif opcion == '7':
            tienda.guardar_datos()
            print(f"{Fore.YELLOW}Datos guardados. Saliendo...")
            break
        else:
            print(f"{Fore.RED}Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()