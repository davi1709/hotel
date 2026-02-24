import flet as ft
import datetime

class Pessoa:
    def __init__(self, nome, telefone, email):
        self.__nome = nome
        self.__telefone = telefone
        self.__email = email
    @property
    def nome(self):
        return self.__nome
    @property
    def telefone(self):
        return self.__telefone
    @property
    def email(self):
        return self.__email
    def exibir_informacoes(self):
        return f"Nome: {self.__nome}, Telefone: {self.__telefone}, Email: {self.__email}"

class Cliente(Pessoa):
    _id_contador = 1
    def __init__(self, nome, telefone, email):
        super().__init__(nome, telefone, email)
        self.__id = Cliente._id_contador
        Cliente._id_contador += 1
    @property
    def id(self):
        return self.__id
    def exibir_informacoes(self):
        return f"ID: {self.__id}, {super().exibir_informacoes()}"

class Quarto:
    def __init__(self, numero, tipo, preco):
        self.__numero = numero
        self.__tipo = tipo
        self.__preco = preco
        self.__disponivel = True
    @property
    def numero(self):
        return self.__numero
    @property
    def tipo(self):
        return self.__tipo
    @property
    def preco(self):
        return self.__preco
    @property
    def disponivel(self):
        return self.__disponivel
    @disponivel.setter
    def disponivel(self, valor: bool):
        self.__disponivel = valor

class Reserva:
    def __init__(self, cliente: Cliente, quarto: Quarto, checkin: datetime.date, checkout: datetime.date):
        self.cliente = cliente
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.status = "Ativa"
        self.quarto.disponivel = False
    def cancelar(self):
        self.status = "Cancelada"
        self.quarto.disponivel = True

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []
    def adicionar_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)
    def adicionar_quarto(self, quarto: Quarto):
        self.quartos.append(quarto)
    def criar_reserva(self, cliente: Cliente, quarto: Quarto, checkin: datetime.date, checkout: datetime.date):
        if quarto.disponivel:
            reserva = Reserva(cliente, quarto, checkin, checkout)
            self.reservas.append(reserva)
            return reserva
    def listar_reservas(self):
        return self.reservas

ger = GerenciadorDeReservas()
ger.adicionar_quarto(Quarto(101,"Single",150))
ger.adicionar_quarto(Quarto(102,"Double",200))
ger.adicionar_quarto(Quarto(103,"Suite",400))
ger.adicionar_cliente(Cliente("Davi","1111-1111","davi@email.com"))
ger.adicionar_cliente(Cliente("Jair","2222-2222","jair@email.com"))

def main(page: ft.Page):
    page.title = "Hotel"
    lst = ft.ListView(expand=True, spacing=5, padding=5)
    def atualizar_lista():
        lst.controls.clear()
        for r in ger.listar_reservas():
            lst.controls.append(ft.Text(f"{r.cliente.nome} - Quarto {r.quarto.numero} - Status: {r.status}"))
        page.update()
    def criar_reserva_click(e):
        ger.criar_reserva(ger.clientes[0], ger.quartos[0], datetime.date.today(), datetime.date.today()+datetime.timedelta(days=2))
        atualizar_lista()
    page.add(
        ft.Column([
            ft.Row([
                ft.Text("Reservas:", size=20),
                ft.ElevatedButton("Criar reserva", on_click=criar_reserva_click)
            ]),
            lst
        ])
    )
    atualizar_lista()

ft.app(target=main)
