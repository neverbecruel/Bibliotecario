from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from sqlalchemy.sql.schema import UniqueConstraint
from validate_docbr import CPF


class Base(DeclarativeBase):
    pass


class Livro(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    gen = Column(String)
    autor = Column(String)
    ano = Column(Integer)
    disp = Column(Boolean)
    paginas = Column(Integer)
    nota = Column(Float)
    leitores = relationship('Pessoa', secondary='relacao_leitura', overlaps='livros')


class Pessoa(Base):
    __tablename__ = "Pessoas"
    id = Column(Integer, primary_key=True)
    cpf = Column(String(11), unique=True)
    livros = relationship('Livro', secondary='relacao_leitura', overlaps='leitores')
    nome = Column(String)


class RelacaoLeitura(Base):
    __tablename__ = 'relacao_leitura'
    livro_id = Column(Integer, ForeignKey('Livros.id'), primary_key=True)
    pessoa_id = Column(Integer, ForeignKey('Pessoas.id'), primary_key=True)
    __table_args__ = (UniqueConstraint('livro_id', 'pessoa_id'),)


db_url = 'sqlite:///livros_dataset.db'
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Sessao = sessionmaker(bind=engine)
sessao = Sessao()


def valida_cpf(cpf):
    # Crie uma instância da classe CPF
    cpf_validator = CPF()

    # Verifique se o CPF é válido
    if cpf_validator.validate(cpf):
        return True
    else:
        return False