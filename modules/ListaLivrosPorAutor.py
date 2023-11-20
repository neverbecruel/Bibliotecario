from PyQt6.QtWidgets import QMainWindow, QLabel, QListWidget, QPushButton, QListWidgetItem, QMessageBox
from metadatas import sessao, Livro, RelacaoLeitura, Pessoa


class ListaLivrosPorAutor(QMainWindow):
    def __init__(self, autor, cpf):
        super().__init__()
        self.setWindowTitle('Livros por Autor')
        self.setGeometry(200, 100, 400, 300)

        self.autor = autor
        self.cpf = cpf

        self.LAutor = QLabel(f"Livros de {autor}:", self)
        self.LAutor.setGeometry(50, 15, 300, 20)

        self.lista_livros = QListWidget(self)
        self.lista_livros.setGeometry(50, 50, 300, 200)
        livros = sessao.query(Livro).filter(Livro.autor == autor).all()
        self.livros_dict = {}  # Dicionário para mapear os índices dos livros aos livros
        self.preencher_lista_de_livros(livros)

        self.alugar = QPushButton("OK", self)
        self.alugar.setGeometry(175, 260, 50, 30)
        self.alugar.clicked.connect(self.alugar_livro)

    def preencher_lista_de_livros(self, livros):
        for i, livro in enumerate(livros):
            item = QListWidgetItem(f"Livro: {livro.titulo}  |  Nota: {livro.nota}")
            self.lista_livros.addItem(item)
            self.livros_dict[i] = livro  # Mapeia o índice do livro ao livro

    def alugar_livro(self):
        item_selecionado = self.lista_livros.currentItem()

        if item_selecionado is not None:
            item_index = self.lista_livros.row(item_selecionado)
            livro = self.livros_dict.get(item_index)

            if livro and livro.disp:
                cpf = self.cpf
                pessoa = sessao.query(Pessoa).filter(Pessoa.cpf == cpf).first()

                if pessoa:
                    # Verifique se a pessoa já alugou dois livros
                    alugueis = sessao.query(RelacaoLeitura).filter(RelacaoLeitura.pessoa_id == pessoa.id).all()

                    if len(alugueis) >= 2:
                        QMessageBox.warning(self, "Aviso",
                                            "Esta pessoa já alugou dois livros. Não é possível alugar mais.")
                    else:
                        id_pessoa = pessoa.id
                        id_livro = livro.id
                        relacao = RelacaoLeitura(livro_id=id_livro, pessoa_id=id_pessoa)
                        sessao.add(relacao)
                        livro.disp = False
                        sessao.commit()
                        QMessageBox.warning(self, "Aviso", "Livro alugado com sucesso.")
                        self.close()
                else:
                    QMessageBox.warning(self, "Aviso", "Pessoa não encontrada.")
                    self.close()
            elif livro and not livro.disp:
                QMessageBox.warning(self, "Aviso", "Livro indisponível.")
        else:
            QMessageBox.warning(self, "Aviso", "Selecione um livro primeiro.")
