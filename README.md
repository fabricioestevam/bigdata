🚀 IoT Big Data Pipeline
📋 Descrição do Projeto
Pipeline completa de Big Data para coleta, processamento e armazenamento de dados de sensores IoT em MongoDB Atlas, aplicando princípios SOLID e boas práticas de engenharia de software.
🏗 Arquitetura SOLID Aplicada
S - Single Responsibility Principle

DHT22Sensor: Apenas coleta dados do sensor
DataCleaner: Apenas limpa e valida dados
MongoDBStore: Apenas gerencia armazenamento
IoTPipeline: Orquestra o fluxo completo

O - Open/Closed Principle

Interfaces ISensor, IDataCleaner, IDataStore permitem extensão
Novos sensores/cleaners/storages podem ser adicionados sem modificar código existente

L - Liskov Substitution Principle

Todas as implementações podem substituir suas interfaces
DHT22Sensor pode ser substituído por qualquer ISensor

I - Interface Segregation Principle

Interfaces específicas e focadas
ISensor ≠ IDataCleaner ≠ IDataStore

D - Dependency Inversion Principle

Módulos de alto nível dependem de abstrações
IoTPipeline depende de interfaces, não de implementações concretas

📁 Estrutura do Projeto
iot-bigdata-pipeline/
├── src/
│   ├── core/
│   │   ├── interfaces.py          # Interfaces SOLID
│   │   ├── sensors.py             # Implementação do sensor
│   │   ├── storage.py             # Conexão MongoDB Atlas
│   │   └── pipeline_refactored.py # Pipeline principal
│   ├── data_cleaning/
│   │   └── cleaners.py            # Limpeza e validação
│   └── config.py                  # Configurações
├── tests/                         # Testes unitários
├── app.py                         # Aplicação principal
└── requirements.txt               # Dependências
🛠 Tecnologias Utilizadas

Python 3.12+
MongoDB Atlas (Cloud)
PyMongo - Driver MongoDB
python-dotenv - Variáveis de ambiente
pytest - Testes unitários

🚀 Como Executar
1. Configuração do Ambiente
bash# Clone o repositório
git clone <seu-repositorio>
cd iot-bigdata-pipeline

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais do MongoDB Atlas
2. Configuração do MongoDB Atlas

Crie uma conta em MongoDB Atlas
Crie um cluster gratuito (M0)
Configure usuário de banco com permissões de leitura/escrita
Adicione 0.0.0.0/0 na whitelist de IPs
Obtenha a string de conexão

3. Execução
bash# Executar pipeline completa
python app.py

# Executar testes
python -m pytest tests/ -v
📊 Fluxo de Dados

Coleta → Sensor DHT22 (simulado) coleta temperatura e umidade
Limpeza → Validação de ranges e detecção de anomalias
Armazenamento → Persistência em MongoDB Atlas
Monitoramento → Estatísticas em tempo real

🔧 Funcionalidades
Sensor Simulation

Gera dados realistas de temperatura (20-30°C) e umidade (40-70%)
Simula erros de sensor ocasionais (5% de chance)
Timestamp automático com timezone UTC

Data Cleaning

Validação de ranges de temperatura (-50°C a 60°C)
Validação de ranges de umidade (0% a 100%)
Detecção de anomalias e dados inválidos
Metadados de limpeza

MongoDB Storage

Conexão segura com MongoDB Atlas
Inserção de documentos com IDs únicos
Fallback automático para modo simulação
Tratamento de erros robusto

📈 Exemplo de Saída
🚀 Iniciando IoT Big Data Pipeline...
🔗 Conectando ao MongoDB Atlas...
🎉 CONEXÃO REAL COM MONGODB ATLAS ESTABELECIDA!
✅ DADOS SALVOS NO MONGODB! ID: 68e6942299465e5aca6fbec2
📈 Estatísticas: 15 processados, 0 erros, 100% sucesso
🧪 Testes
bash# Executar todos os testes
python -m pytest tests/ -v

# Testes específicos
python -m pytest tests/test_sensors.py
python -m pytest tests/test_cleaners.py
python -m pytest tests/test_storage.py
🔄 Modos de Operação
Modo Real (MongoDB Atlas)

Conexão com MongoDB na nuvem
Persistência real dos dados
IDs únicos do MongoDB
Escalabilidade cloud

Modo Simulação (Fallback)

Operação offline
Dados exibidos no console
Mesma funcionalidade sem dependência externa

📝 Configuração
Variáveis de Ambiente (.env)
envMONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
DB_NAME=iot_database
COLLECTION_NAME=sensor_data
SENSOR_SIMULATION=True
DATA_GENERATION_INTERVAL=5
👨‍💻 Desenvolvimento
Adicionar Novo Sensor
pythonfrom core.interfaces import ISensor

class NovoSensor(ISensor):
    def read_data(self) -> Dict[str, Any]:
        # Implementação específica
        return {...}
Adicionar Novo Data Cleaner
pythonfrom core.interfaces import IDataCleaner

class NovoCleaner(IDataCleaner):
    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Nova estratégia de limpeza
        return cleaned_data
🐛 Solução de Problemas
Erro de Conexão MongoDB

Verifique a string de conexão no .env
Confirme se o IP está na whitelist
Verifique se o cluster está ativo

Dados Inválidos

O sistema detecta automaticamente dados fora do range
Anomalias são marcadas no campo *_status

📄 Licença
Este projeto é para fins educacionais como parte da disciplina de Big Data.

Desenvolvido com 💻 para demonstração de conceitos de IoT e Big Data