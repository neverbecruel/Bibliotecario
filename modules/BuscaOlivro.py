from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QLineEdit
from PyQt6.QtWidgets import QCompleter, QMessageBox
from PyQt6.QtCore import Qt
from metadatas import sessao, Livro, RelacaoLeitura, Pessoa
from modules.ListaLivrosPorAutor import ListaLivrosPorAutor


class BuscaOlivro(QMainWindow):
    def __init__(self, cpf):
        super().__init__()
        self.setWindowTitle('Aluguel')
        self.setGeometry(200, 100, 350, 200)

        self.cpf = cpf

        self.Llivro = QLabel("", self)
        self.Llivro.setGeometry(50, 15, 160, 20)
        self.get_name()
        # Caixa para busca
        self.caixatxt = QLineEdit(self)
        self.caixatxt.setGeometry(90, 60, 200, 25)

        # caixa de opções de busca
        self.opcao = QComboBox(self)
        self.opcao.setGeometry(10, 60, 80, 25)
        self.opcao.addItem("Selecione...")
        self.opcao.addItem("Título...")
        self.opcao.addItem("Autor...")

        self.escolher = QPushButton("OK", self)
        self.escolher.setGeometry(175, 160, 50, 30)
        self.escolher.clicked.connect(self.teste)

        self.opcao.currentTextChanged.connect(self.atualizar_texto)
        self.opcao.currentTextChanged.connect(self.busca_busca)

        self.sugestoes_titulos = self.obter_sugestoes_titulos()
        self.sugestoes_autores = self.obter_sugestoes_autores()

        self.sugestoes_label = QLabel("", self)  # Adicione um rótulo para exibir as sugestões
        self.sugestoes_label.setGeometry(10, 100, 250, 35)  # Posicione o rótulo na interface

    def obter_sugestoes_titulos(self):
        # Consulta o banco de dados para obter títulos de livros
        livros = sessao.query(Livro.titulo).all()
        titulos = [livro.titulo for livro in livros]
        return titulos

    def obter_sugestoes_autores(self):
        livros = sessao.query(Livro.autor).all()
        autores = [livro.autor for livro in livros]
        return autores

    def teste(self):
        if self.opcao.currentText() == "Título..." and self.caixatxt.text():
            titulo = self.caixatxt.text()
            livro = sessao.query(Livro).filter(Livro.titulo == titulo).first()

            if self.cpf and livro:
                if livro.disp:
                    pessoa = sessao.query(Pessoa).filter(Pessoa.cpf == self.cpf).first()

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
                else:
                    QMessageBox.warning(self, "Aviso", "Livro indisponível.")
                    self.caixatxt.clear()
            else:
                QMessageBox.warning(self, "Aviso", "Livro não encontrado.")

        elif self.opcao.currentText() == "Autor..." and self.caixatxt.text():
            autor = self.caixatxt.text()
            self.abrir_lista_livros_por_autor(autor)
        else:
            QMessageBox.warning(self, "Aviso", "ERRO")
            self.close()

    def atualizar_texto(self, texto):
        self.caixatxt.setPlaceholderText(texto)

    def busca_busca(self, texto):
        if texto == "Título...":
            titulo = self.caixatxt.text()
            resultados = sessao.query(Livro).filter(Livro.titulo == titulo).all()
            sugestoes = [livro.titulo for livro in resultados]
            self.caixatxt.textChanged.connect(self.mostrar_sugestoes_titulos)
            self.sugestoes_label.setText("\n".join(sugestoes))
            completer = QCompleter(self.sugestoes_titulos, self.caixatxt)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.caixatxt.setCompleter(completer)
        elif texto == 'Autor...':
            autor = self.caixatxt.text()
            resultados = sessao.query(Livro).filter(Livro.autor == autor).all()
            sugestoes = [livro.autor for livro in resultados]
            self.caixatxt.textChanged.connect(self.mostrar_sugestoes_autores)
            self.sugestoes_label.setText("\n".join(sugestoes))
            completer = QCompleter(self.sugestoes_autores, self.caixatxt)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.caixatxt.setCompleter(completer)


    def abrir_lista_livros_por_autor(self, autor):
        self.close()
        self.janela_lista_livros = ListaLivrosPorAutor(autor, self.cpf)
        self.janela_lista_livros.show()

    def mostrar_sugestoes_autores(self):
        # O texto digitado será exibido no rótulo de sugestões
        texto_digitado = self.caixatxt.text()
        self.sugestoes_label.setText(f"Autor selecionado: '{texto_digitado}':")

    def mostrar_sugestoes_titulos(self):
        # O texto digitado será exibido no rótulo de sugestões
        texto_digitado = self.caixatxt.text()
        self.sugestoes_label.setText(f"Titulo selecionado: '{texto_digitado}':")


    def get_name(self):
        pessoa = sessao.query(Pessoa).filter(Pessoa.cpf == self.cpf).first()
        nome = pessoa.nome
        self.Llivro.setText(f"Olá, {nome}. Escolha um livro...")

