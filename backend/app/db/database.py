from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./app.db"  # futuramente trocamos por PostgreSQL

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Cria as tabelas no banco."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Cria uma sessão de banco."""
    with Session(engine) as session:
        yield session
