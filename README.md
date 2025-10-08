# bigdata# IoT Big Data Pipeline

## 📋 Descrição
Pipeline completa para coleta, limpeza e armazenamento de dados de sensores IoT em MongoDB Atlas, aplicando princípios SOLID e conceitos de Big Data.

## 🏗 Arquitetura SOLID
- **S** - Single Responsibility: Cada classe tem uma única responsabilidade
- **O** - Open/Closed: Extensível para novos sensores e cleaners
- **L** - Liskov Substitution: Interfaces garantem substituibilidade
- **I** - Interface Segregation: Interfaces específicas para cada papel
- **D** - Dependency Inversion: Dependências de abstrações, não implementações

## 🚀 Como Executar

1. **Configurar Environment**
```bash
cp .env.example .env
# Edite .env com suas configurações do MongoDB Atlas