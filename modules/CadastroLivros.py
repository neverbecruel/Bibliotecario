from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QMessageBox
from metadatas import sessao, Livro


class CadastroLivros(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tela de livro')
        self.setGeometry(100, 100, 340, 300)

        self.LTitulo = QLabel("Cadastro de livros", self)
        self.LTitulo.setGeometry(115, 15, 150, 20)

        self.LLivro = QLabel("Titulo", self)
        self.LLivro.setGeometry(25, 65, 95, 20)

        self.LGenero = QLabel("Genero", self)
        self.LGenero.setGeometry(25, 100, 95, 20)

        self.LAutor = QLabel("Autor", self)
        self.LAutor.setGeometry(25, 135, 95, 20)

        self.LAno = QLabel("Ano", self)
        self.LAno.setGeometry(25, 165, 95, 20)

        self.LNota = QLabel("Nota", self)
        self.LNota.setGeometry(25, 200, 95, 20)

        self.CLivro = QLineEdit(self)
        self.CLivro.setGeometry(65, 65, 205, 20)
        self.CLivro.setPlaceholderText('Digite o Titulo do livro...')

        self.CGenero = QLineEdit(self)
        self.CGenero.setGeometry(65, 100, 205, 20)
        self.CGenero.setPlaceholderText('Digite o Gênero...')

        self.CAutor = QLineEdit(self)
        self.CAutor.setGeometry(65, 135, 205, 20)
        self.CAutor.setPlaceholderText('Digite o nome do autor...')

        self.CAno = QLineEdit(self)
        self.CAno.setGeometry(65, 165, 205, 20)
        self.CAno.setPlaceholderText('Digite o Ano Lançado...')

        self.CNota = QLineEdit(self)
        self.CNota.setGeometry(65, 200, 205, 20)
        self.CNota.setPlaceholderText('Digite a nota do livro...')

        self.CadastroL = QPushButton("Cadastrar o Livro", self)
        self.CadastroL.setGeometry(114, 245, 105, 30)
        self.CadastroL.clicked.connect(self.cadastrar_livro)

    def cadastrar_livro(self):
        titulo = self.CLivro.text()
        if len(titulo) <= 0:
            QMessageBox.warning(self, "Aviso", "Titulo não preenchido")
            self.CLivro.clear()
        genero = self.CGenero.text()
        if len(genero) <= 0:
            QMessageBox.warning(self, "Aviso", "Gênero não preenchido")
        autor = self.CAutor.text()
        if len(autor) <= 0:
            QMessageBox.warning(self, "Aviso", "Autor não preenchido")
        ano = self.CAno.text()
        try:
            str(ano)
        except:
            QMessageBox.warning(self, "Aviso", "Ano de publicação inválido")
        paginas = self.CAno.text()
        if len(paginas) <= 0:
            QMessageBox.warning(self, "Aviso", "Paginas não preenchido")
        try:
            nota = float(self.CNota.text())
            if nota >= 0 and nota <= 5:
                livro = Livro(titulo=titulo, gen=genero, autor=autor, ano=ano, disp=True, paginas=paginas, nota=nota)
                sessao.add(livro)
                sessao.commit()
                QMessageBox.warning(self, "Aviso", "Livro cadastrado com sucesso.")

            else:
                QMessageBox.warning(self, "Aviso", "Nota tem que ser de 0 a 5.")
                self.CNota.clear()
        except:
            QMessageBox.warning(self, "Aviso", "Nota tem que ser um valor numérico.")
            self.CNota.clear()