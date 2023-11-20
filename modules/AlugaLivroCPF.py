from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from metadatas import sessao, Pessoa, valida_cpf
from modules.BuscaOlivro import BuscaOlivro
from modules.JanelaCadastroPessoa import JanelaCadastroPessoa
from modules import open_window


class AlugaLivroCPF(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aluguel')
        self.setGeometry(100, 100, 230, 170)

        self.ATitulo = QLabel("Aluguel dos livros", self)
        self.ATitulo.setGeometry(65, 5, 150, 20)

        self.LCPF = QLabel("Qual o seu cpf?", self)
        self.LCPF.setGeometry(8, 65, 95, 20)

        self.CaixaCPF = QLineEdit(self)
        self.CaixaCPF.setGeometry(95, 65, 95, 20)
        self.CaixaCPF.setPlaceholderText('Digite o seu CPF...')

        self.Busca = QPushButton("Buscar livro", self)
        self.Busca.setGeometry(60, 120, 100, 25)
        self.Busca.clicked.connect(self.buscar_cpf)

    def buscar_cpf(self):
        cpf = self.CaixaCPF.text()
        if valida_cpf(cpf):
            pessoa_existente = sessao.query(Pessoa).filter_by(cpf=cpf).first()
            if not pessoa_existente:
                QMessageBox.warning(self, "Aviso", "Pessoa não cadastrada. Cadastre-se e tente novamente.")
                self.fechar_abrir_janela_cadastro_pessoa()
            else:
                self.chamar_busca_livro(cpf)
        else:
            QMessageBox.warning(self, "Aviso", "CPF INVÁLIDO")
            self.CaixaCPF.clear()

    @open_window(JanelaCadastroPessoa)
    def fechar_abrir_janela_cadastro_pessoa(self):
        self.close()

    def chamar_busca_livro(self, cpf):
        self.close()
        self.janela_busca_livro = BuscaOlivro(cpf)
        self.janela_busca_livro.show()