**Sistema de Controle de Estoque - Mecânica Precision**

Sistema web completo desenvolvido em Django para gerenciamento inteligente de estoque, especialmente projetado para oficinas mecânicas e pequenas empresas. Oferece controle total sobre produtos, movimentações e relatórios com interface moderna e intuitiva.

### 🚀 **Principais Funcionalidades**

**📦 Gestão de Produtos**
- Cadastro completo com código de referência, descrição, categoria e imagem
- Controle de localização na prateleira e informações do fornecedor
- Gestão de preços e cálculo automático de valores totais
- Upload de imagens para identificação visual

**📊 Dashboard Inteligente**
- Visão geral em tempo real do estoque
- Alertas visuais para produtos com estoque baixo
- Indicadores de performance e valor total em estoque
- Produtos mais valiosos e últimas movimentações

**⚠️ Sistema de Alertas**
- Monitoramento automático de estoque mínimo
- Notificações visuais para reposição
- Relatórios de produtos críticos

**🔄 Controle de Movimentações**
- Registro de entradas e saídas com histórico completo
- Atualização automática do estoque
- Rastreabilidade por responsável e data/hora
- Validação de quantidade disponívelanydesk

**📋 Relatórios Avançados**
- Relatórios por categoria, estoque baixo ou geral
- Exportação para CSV
- Função de impressão otimizada
- Filtros personalizáveis

**🏷️ Organização por Categorias**
- Sistema flexível de categorização
- Controle hierárquico de produtos
- Estatísticas por categoria

### 🛠️ **Tecnologias Utilizadas**

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Formulários**: Django Crispy Forms
- **Autenticação**: Sistema de usuários Django
- **Arquivos Estáticos**: WhiteNoise
- **Interface**: FontAwesome Icons, Design Responsivo

### 💼 **Ideal Para**

- Oficinas mecânicas e auto peças
- Pequenas e médias empresas
- Lojas de varejo
- Almoxarifados
- Controle de ferramentas e equipamentos

### ✨ **Diferenciais**

- Interface intuitiva e responsiva
- Sistema de alertas em tempo real
- Exportação de dados facilitada
- Controle de usuários e permissões
- Dashboard com métricas visuais
- Validações inteligentes de estoque

### 📱 **Compatibilidade**

- Totalmente responsivo (Desktop, Tablet, Mobile)
- Compatível com todos os navegadores modernos
- Interface otimizada para uso profissional

---

### 🔧 **Instalação Rápida**

```bash
git clone https://github.com/MatheusPenn4/Estoque-Mecanica-Precision.git
cd Estoque-Mecanica-Precision
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🚨 IMPORTANTE: Pasta venv NÃO deve ser enviada

A pasta `venv` (ambiente virtual) **NÃO** deve ser enviada para o GitHub porque:

- Contém arquivos específicos do seu sistema
- É muito pesada (centenas de MB)
- Pode causar conflitos em outros sistemas
- Será recriada automaticamente por quem baixar o projeto

### ✅ O que DEVE ser enviado:
- `requirements.txt` (lista de dependências)
- Código fonte do projeto
- Templates e arquivos estáticos
- Documentação

### ❌ O que NÃO deve ser enviado:
- `venv/` ou qualquer pasta de ambiente virtual
- `db.sqlite3` (banco de dados local)
- `__pycache__/` (cache do Python)
- `.env` (arquivos de configuração sensível)

### Como verificar se o .gitignore está funcionando:

1. No terminal, execute:
```bash
git status
```

2. Se a pasta `venv` aparecer na lista, adicione ao .gitignore:
```bash
echo "venv/" >> .gitignore
```

3. Se já foi adicionada por engano, remova do tracking:
```bash
git rm -r --cached venv/
git commit -m "Remove pasta venv do repositório"
```

### Para quem baixar o projeto:

Quem baixar seu projeto do GitHub deverá:

1. Criar um novo ambiente virtual:
```bash
python -m venv venv
```

2. Ativar o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instalar as dependências:
```bash
pip install -r requirements.txt
```

4. Executar migrações:
```bash
python manage.py migrate
```

5. Criar superusuário:
```bash
python manage.py createsuperuser
```

### Verificação final antes do upload:

Execute `git status` e certifique-se de que aparecem apenas estes tipos de arquivo:
- ✅ `.py` (arquivos Python)
- ✅ `.html` (templates)
- ✅ `.css`, `.js` (arquivos estáticos)
- ✅ `.md` (documentação)
- ✅ `requirements.txt`
- ✅ `manage.py`

Se aparecer `venv/` na lista, **NÃO** faça o commit até resolver.

### 📸 **Screenshots**

*Dashboard principal com métricas em tempo real*
*Gestão completa de produtos com alertas visuais*
*Sistema de relatórios com exportação*

### 🤝 **Contribuições**

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

### 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

### 👨‍💻 **Autor**

**Matheus Oliveira Penna**
- Email: matheusoliveirapenna@gmail.com
- GitHub: [@MatheusPenn4](https://github.com/MatheusPenn4)

---

*Sistema desenvolvido com foco na praticidade e eficiência para pequenas empresas que precisam de controle profissional do estoque sem complexidade desnecessária.*
