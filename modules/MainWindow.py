from PyQt6.QtWidgets import (QApplication, QComboBox, QMainWindow, QPushButton, QCompleter, QLabel, QLineEdit,
                             QMessageBox, QListWidgetItem, QListWidget, QWidget)
from PyQt6.QtCore import Qt
import sys
from metadatas import sessao, Livro, RelacaoLeitura, Pessoa, valida_cpf
from modules.ListaAlugas import ListaAlugas
from modules.DevolucaoWdw import DevolucaoWdw
from modules.BuscaOlivro import BuscaOlivro
from modules.ListaLivrosPorAutor import ListaLivrosPorAutor
from modules.JanelaCadastroPessoa import JanelaCadastroPessoa
from modules.CadastroLivros import CadastroLivros
from modules.AlugaLivroCPF import AlugaLivroCPF
from modules.BuscaOlivro import BuscaOlivro

def open_window(window_class):
    def decorator(func):
        def wrapper(self):
            self.new_window = window_class()
            self.new_window.show()
            func(self)
        return wrapper
    return decorator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tela Principal')
        self.setGeometry(100, 150, 400, 350)

        # Cria um Label
        self.hello = QLabel("Livros com maiores notas abaixo:", self)
        self.hello.setGeometry(50, 10, 300, 30)

        # Cria uma lista
        self.lista_livros = QListWidget(self)
        self.lista_livros.setGeometry(50, 50, 300, 200)
        livros = sessao.query(Livro).filter(Livro.nota > 4).all()
        self.preencher_lista_de_livros(livros)

        # Cria Botão de cadastro de usuário
        self.criar_leitor = QPushButton("Cadastrar Leitor", self)
        self.criar_leitor.setGeometry(280, 260, 100, 30)
        self.criar_leitor.clicked.connect(self.cadastrar_leitor)

        # Cria Botão para cadastro de novo Livro
        self.cria_livro = QPushButton("Cadastrar Livro", self)
        self.cria_livro.setGeometry(20, 260, 100, 30)
        self.cria_livro.clicked.connect(self.cadastrar_livro)

        # Cria botão para alugar um livro
        self.aluga = QPushButton("Alugar livro", self)
        self.aluga.setGeometry(40, 300, 100, 30)
        self.aluga.clicked.connect(self.alugar)

        #Cria botão para devolução
        self.devolve = QPushButton("Devolução", self)
        self.devolve.setGeometry(260, 300, 100, 30)
        self.devolve.clicked.connect(self.devolves)

    @open_window(DevolucaoWdw)
    def devolves(self):
        pass


    def preencher_lista_de_livros(self, livros):
        for livro in livros:
            item = QListWidgetItem(f"{livro.titulo} - Nota: {livro.nota}")
            self.lista_livros.addItem(item)

    def cadastrar_leitor(self):
        self.pessoacadastro = JanelaCadastroPessoa()
        self.pessoacadastro.show()

    def cadastrar_livro(self):
        self.janelacadlivro = CadastroLivros()
        self.janelacadlivro.show()

    def alugar(self):
        self.chama = AlugaLivroCPF()
        self.chama.show()