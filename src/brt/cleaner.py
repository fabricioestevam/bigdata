"""
Limpeza e Validação de Dados BRT - Segue padrão SOLID
"""
from datetime import datetime, timezone
from src.core.interfaces import IDataCleaner


class BRTDataCleaner(IDataCleaner):
    """
    Valida e enriquece dados de detecção BRT
    Implementa interface IDataCleaner (SOLID)
    """
    
    def __init__(self, linhas_conhecidas):
        """
        Args:
            linhas_conhecidas: dict com info das linhas
                {
                    "437": {"nome": "...", "tempo_medio_min": 5},
                    ...
                }
        """
        self.linhas_conhecidas = linhas_conhecidas
    
    def clean(self, data: dict) -> dict:
        """
        Valida e enriquece dados
        
        Args:
            data: dados brutos da detecção
            
        Returns:
            dict: dados limpos e validados
        """
        cleaned = data.copy()
        
        linha = cleaned.get('linha')
        
        # Validar linha
        if linha in self.linhas_conhecidas:
            cleaned['linha_valida'] = True
            cleaned['nome_linha'] = self.linhas_conhecidas[linha]['nome']
            cleaned['tempo_estimado_min'] = self.linhas_conhecidas[linha]['tempo_medio_min']
        else:
            cleaned['linha_valida'] = False
            cleaned['nome_linha'] = 'Desconhecida'
        
        # Metadados
        cleaned['cleaned'] = True
        cleaned['cleaned_at'] = datetime.now(timezone.utc).isoformat()
        
        return cleaned
```

---

### 6️⃣ `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Ambiente
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# Modelos
yolov8n.pt
*.pt

# Logs
*.log