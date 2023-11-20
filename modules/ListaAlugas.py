from PyQt6.QtWidgets import QMainWindow, QListWidget, QPushButton, QLabel, QListWidgetItem
from metadatas import sessao, Livro, RelacaoLeitura, Pessoa


class ListaAlugas(QMainWindow):
    def __init__(self, nome, cpf):
        super().__init__()
        self.setWindowTitle('Devolução')
        self.setGeometry(100, 100, 500, 300)

        self.nome = nome
        self.cpf = cpf

        self.lista_livros = QListWidget(self)
        self.lista_livros.setGeometry(50, 50, 400, 200)

        livros = sessao.query(RelacaoLeitura).filter(RelacaoLeitura.pessoa_id == self.get_id()).all()
        self.livros_dict = {}  # Dicionário para mapear os índices dos livros aos livros
        self.preencher_lista_de_livros(livros)

        self.texto = QLabel("", self)
        self.texto.setGeometry(70, 20, 200, 20)
        self.get_name()

        self.devolver = QPushButton("Devolver", self)
        self.devolver.setGeometry(200, 260, 100, 30)
        self.devolver.clicked.connect(self.deletar_livro)

    def get_name(self):
        self.texto.setText(f"Livros alugados por: {self.nome}")

    def get_id(self):
        pessoa = sessao.query(Pessoa).filter(Pessoa.cpf == self.cpf).first()
        pessoa_id = pessoa.id
        return pessoa_id

    def deletar_livro(self):
        item_selecionado = self.lista_livros.currentItem()
        if item_selecionado:
            indice = self.lista_livros.row(item_selecionado)
            livro = self.livros_dict.get(indice)
            if livro:
                # Remova a relação da tabela RelacaoLeitura
                sessao.query(RelacaoLeitura).filter(
                    RelacaoLeitura.pessoa_id == self.get_id(),
                    RelacaoLeitura.livro_id == livro.id
                ).delete()

                # Defina o atributo disp do livro como True
                livro.disp = True
                sessao.commit()

                # Atualize a lista de livros na interface gráfica
                self.lista_livros.takeItem(indice)
                del self.livros_dict[indice]



    def preencher_lista_de_livros(self, livros):
        for i, livro_relacao in enumerate(livros):
            livro = sessao.query(Livro).filter(Livro.id == livro_relacao.livro_id).first()
            if livro:
                self.livros_dict[i] = livro
                item = QListWidgetItem(f'Título: {livro.titulo} - Autor: {livro.autor}')
                self.lista_livros.addItem(item)