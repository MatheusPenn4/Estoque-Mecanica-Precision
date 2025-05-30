# Sistema de Controle de Estoque

Sistema web desenvolvido em Django para gerenciamento completo de estoque de produtos.

## Funcionalidades

- Cadastro e gerenciamento de produtos
- Organização por categorias
- Registro de entradas e saídas de estoque
- Controle de estoque mínimo com alertas
- Histórico de movimentações
- Relatórios personalizados
- Interface responsiva e moderna

## Requisitos

- Python 3.8 ou superior
- Django 4.2.7
- Bibliotecas adicionais (listadas em `requirements.txt`)

## Instalação

1. Clone o repositório:
```
git clone https://github.com/MatheusPenn4/Estoque-Mecanica-Precision.git
```

2. Crie e ative um ambiente virtual:
```
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
- Crie um arquivo `.env` na raiz do projeto
- Adicione as variáveis necessárias (veja o arquivo `.env.example`)

5. Execute as migrações:
```
python manage.py migrate
```

6. Crie um superusuário:
```
python manage.py createsuperuser
```

7. Inicie o servidor:
```
python manage.py runserver
```

8. Acesse em seu navegador:
```
http://127.0.0.1:8000/
```
## Estrutura do Projeto

```
controle-estoque/
│
├── controlador_estoque/    # Configurações do projeto Django
│   ├── __init__.py
│   ├── settings.py         # Configurações gerais
│   ├── urls.py             # URLs do projeto
│   └── wsgi.py             # Configuração WSGI
│
├── estoque/                # Aplicação principal
│   ├── migrations/         # Migrações do banco de dados
│   ├── __init__.py
│   ├── admin.py            # Configuração do admin
│   ├── apps.py             # Configuração da aplicação
│   ├── forms.py            # Formulários
│   ├── models.py           # Modelos de dados
│   ├── urls.py             # URLs da aplicação
│   └── views.py            # Views da aplicação
│
├── templates/              # Templates HTML
│   ├── base.html           # Template base
│   └── estoque/            # Templates específicos da aplicação
│
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│
├── media/                  # Arquivos enviados pelos usuários
│
├── manage.py               # Script de gerenciamento Django
├── requirements.txt        # Dependências do projeto
└── .env                    # Variáveis de ambiente (não versionado)
```

## Screenshots

![Dashboard](screenshots/dashboard.png)
![Produtos](screenshots/produtos.png)
![Movimentações](screenshots/movimentacoes.png)

## Autor

Seu Nome - [matheusoliveirapenna@gmail.com]
