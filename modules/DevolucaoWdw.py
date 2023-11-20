from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from metadatas import sessao, Pessoa, valida_cpf
from modules.ListaAlugas import ListaAlugas


class DevolucaoWdw(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Devolução')
        self.setGeometry(100, 100, 230, 170)
        self.ATitulo = QLabel("Devolva o livro.", self)
        self.ATitulo.setGeometry(65, 5, 150, 20)

        self.LCPF = QLabel("CPF do Retornador:", self)
        self.LCPF.setGeometry(8, 65, 100, 20)

        self.CaixaCPF = QLineEdit(self)
        self.CaixaCPF.setGeometry(115, 65, 95, 20)
        self.CaixaCPF.setPlaceholderText('Digite o CPF...')

        self.Busca = QPushButton("Buscar livros", self)
        self.Busca.setGeometry(60, 120, 100, 25)
        self.Busca.clicked.connect(self.lista_alugados)

    def lista_alugados(self):
        cpf = self.CaixaCPF.text()

        if valida_cpf(cpf):
            pessoa = sessao.query(Pessoa).filter_by(cpf=cpf).first()
            if pessoa:
                nome = pessoa.nome
                self.lista_aluguel = ListaAlugas(nome, cpf)
                self.lista_aluguel.show()
                self.close()
            else:
                QMessageBox.warning(self, "Aviso", "CPF não encontrado.")
        else:
            QMessageBox.warning(self, "Aviso", "CPF inválido.")
