# UFC-2025.1-Persistencia-Trabalho-02 - Relatório de Divisão de Atividades

**Projeto:** Cinema API – Gerenciamento de Filmes, Diretores, Sessões, Salas, Ingressos e Pagamentos com FastAPI e SQLModel  
**Disciplina:** Desenvolvimento de Software para Persistência  
**Data de entrega:** 11.06.2025  
**Dupla:**

* **Aluno 1:** João Victor Amarante Diniz (510466)
* **Aluno 2:** Francisco Breno da Silveira (511429)

---

### 1. Introdução

Este projeto disponibiliza uma API REST construída com FastAPI para gerenciar o domínio **Cinema**, incluindo as entidades **Movies**, **Directors**, **Rooms**, **Sessions**, **Tickets** e **PaymentDetails**. A persistência é feita via SQLite e SQLModel, com migrações gerenciadas pelo Alembic. Foram implementados:

- Modelos de dados com SQLModel e validações de entrada com Pydantic
- Endpoints CRUD (F1–F3), contagem (F4), paginação (F5) e filtragem (F6)  
- Relatórios agregados e consultas avançadas  
- Sistema de migração de esquema com Alembic (F7)  
- Logging (F8)

---

### 2. Configuração do Projeto

1. **Ambiente virtual e dependências**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # ou .venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```

2. **Variáveis de ambiente**

   * `DATABASE_URL` (ex.: `sqlite:///./cinema_db.sqlite3`)
   * `LOG_LEVEL` (ex.: `DEBUG`, `INFO`)
   * `LOG_FILE` (ex.: `app.log`)

3. **Migrações Alembic**

   ```bash
   alembic upgrade head
   ```

4. **Executar a API**

   ```bash
   uvicorn main:app --reload
   ```

5. **Documentação interativa**
   Acesse `http://localhost:8000/docs`.

---

### 3. Atividades Executadas

1. **Modelagem de Entidades e Relacionamentos**

   * SQLModel: `Movie`, `Director`, `Room`, `Session`, `Ticket`, `PaymentDetails`
   * Relacionamentos 1\:N e N\:N implementados via `Relationship` e tabelas de link.
   * **Responsável: João Victor Amarante Diniz (510466)**

2. **DTOs e Validações (Pydantic)**

   * Criação e Update DTOs para todas as entidades
   * Validações de formato (datas, URLs), conflitos de ID, imutabilidade de IDs no PUT.
   * **Responsáveis:  Francisco Breno da Silveira (511429) e João Victor Amarante Diniz (510466)**

3. **Endpoints CRUD & Auxiliares**

   * **F1–F3**: CRUD completo em `/movies`, `/directors`, `/rooms`, `/sessions`, `/tickets`, `/payments`
   * **F4**: `/count` para cada entidade, com `CountResponse`
   * **F5**: paginação em rotas `/filter` e `PaginationMeta`
   * **F6**: filtros por atributos (e.g. `?genre=…`, `?after=…`, `?min_price=…`)
   * Divisão de responsabilidade:
      * **Francisco Breno da Silveira (511429)** - Responsável por implementar F1 - F6 para `Directors`.
      * **João Victor Amarante Diniz (510466)** - Responsável por implementar F1 - F6 para as demais entidades.

4. **Relatórios Avançados**

   * `GET /reports/movie-revenue`: receita e ingressos por filme
      * **Responsável: João Victor Amarante Diniz (510466)**
   * `GET /reports/movie/{movie_id}/sessions`: sessões de um filme com tickets vendidos e receita (com paginação)
      * **Responsável: Francisco Breno da Silveira (511429)**

5. **Migrações Alembic (F7)**

   * Migração inicial para criar todas as tabelas
   * Migração adicional (autogerada) para adicionar coluna `release_year` em `movie`
      * **Responsável: Francisco Breno da Silveira (511429)**

6. **Logging (F8)**

   * Módulo `core/logging.py` lendo `LOG_LEVEL` e `LOG_FILE` da env
   * `logger.info` e `logger.error` em todos os endpoints
      * **Responsável: Francisco Breno da Silveira (511429)**

7. **Relatório**
   * **Responsável: Francisco Breno da Silveira (511429)**

---

### 4. Estrutura modular do projeto

```
├── alembic/                 # Configuração e versões de migrações
│   ├── versions/
│   │   ├── 6eb2819f8a46_add_release_year_to_movie.py
│   │   └── 33f51347be1b_initial_schema.py
│   ├── env.py
│   ├── script.py.mako
│   └── README.md
├── core/                    # Configurações centrais (logging, settings)
│   └── logging.py
├── database/                # Engine e sessão do SQLModel
│   ├── database.py
│   └── db.env
├── models/                  # Definições das entidades com SQLModel
│   └── models.py
├── routers/                 # Rotas REST e relatórios
│   ├── common.py            # DTOs e respostas genéricas
│   ├── director_router.py
│   ├── movie_router.py
│   ├── room_router.py
│   ├── session_router.py
│   ├── ticket_router.py
│   ├── payment_router.py
│   └── complex_router.py    # Relatórios e consultas avançadas
├── main.py                  # Instanciação do FastAPI e inclusão de routers
├── README.md                # Este relatório e instruções de uso
├── requirements.txt         # Dependências do projeto
├── .gitignore
├── alembic.ini
└── cinema_db.sqlite3        # Banco de dados SQLite
```

--- 

### 5. Conclusão

Todas as funcionalidades solicitadas (F1–F8) foram implementadas, garantindo:

* **Robustez**: erros HTTP adequados (404, 409, 400)
* **Flexibilidade**: paginação, filtros dinâmicos e relatórios complexos
* **Manutenibilidade**: migrações controladas com Alembic e logging configurável

Este relatório serve de visão geral — detalhes de cada rota, modelo e migração estão no repositório.
