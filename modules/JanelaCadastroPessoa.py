from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QMessageBox
from metadatas import sessao, Pessoa, valida_cpf


class JanelaCadastroPessoa(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tela de Cadastro')
        self.setGeometry(100, 100, 400, 200)
        # Caixa para digitar o CPF
        self.CaixaCPF = QLineEdit(self)
        self.CaixaCPF.setGeometry(155, 60, 95, 20)
        self.CaixaCPF.setPlaceholderText('Digite o seu CPF')
        # Caixa para Digitar o nome
        self.CaixaNome = QLineEdit(self)
        self.CaixaNome.setGeometry(155, 85, 95, 20)
        self.CaixaNome.setPlaceholderText('Digite o seu Nome...')
        # Botão para salvar os dados
        self.criar_leitor = QPushButton("Cadastrar Leitor", self)
        self.criar_leitor.setGeometry(155, 110, 95, 20)
        self.criar_leitor.clicked.connect(self.cadastrar_leitor)

    def cadastrar_leitor(self):
        cpf = self.CaixaCPF.text()
        nome = self.CaixaNome.text()

        # Checa se a pessoa ja existe no db
        if valida_cpf(cpf):
            pessoa_existente = sessao.query(Pessoa).filter_by(cpf=cpf).first()
            if not pessoa_existente:
                pessoa = Pessoa(nome=nome, cpf=cpf)
                sessao.add(pessoa)
                sessao.commit()
                QMessageBox.warning(self, 'Aviso', 'Pessoa cadastrada com sucesso.')
                self.close()
            else:
                QMessageBox.warning(self, "Aviso", "Pessoa já cadastrada")
        else:
            QMessageBox.warning(self, "Aviso", "CPF INVÁLIDO")
            self.CaixaCPF.clear()