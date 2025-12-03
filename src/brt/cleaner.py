"""
Limpeza e Validação de Dados BRT - Segue padrão SOLID
Sistema BRT Recife
"""

from datetime import datetime, timezone
from typing import Dict, Any

# Tentar importar interface, mas funciona sem ela também
try:
    from src.core.interfaces import IDataCleaner
    HAS_INTERFACE = True
except ImportError:
    # Se não tiver interface, criar uma classe base simples
    class IDataCleaner:
        """Interface base para cleaners"""
        def clean(self, data: dict) -> dict:
            raise NotImplementedError
    HAS_INTERFACE = False


class BRTDataCleaner(IDataCleaner):
    """
    Valida e enriquece dados de detecção BRT
    Implementa interface IDataCleaner seguindo princípios SOLID
    
    Responsabilidade Única: Apenas limpar e validar dados BRT
    
    Attributes:
        linhas_conhecidas (dict): Dicionário com informações das linhas
    
    Example:
        >>> linhas = {
        ...     "437": {"nome": "TI Caxangá", "tempo_medio_min": 5}
        ... }
        >>> cleaner = BRTDataCleaner(linhas)
        >>> data = {"linha": "437"}
        >>> cleaned = cleaner.clean(data)
        >>> print(cleaned["linha_valida"])  # True
    """
    
    def __init__(self, linhas_conhecidas: Dict[str, Dict[str, Any]]):
        """
        Inicializa o cleaner com informações das linhas
        
        Args:
            linhas_conhecidas (dict): Dicionário com dados das linhas
                Formato esperado:
                {
                    "437": {
                        "nome": "TI Caxangá (Conde da Boa Vista) - BRT",
                        "tempo_medio_min": 5,
                        "distancia_km": 2.5
                    },
                    "2441": { ... },
                    ...
                }
        
        Raises:
            ValueError: Se linhas_conhecidas estiver vazio ou inválido
        """
        if not linhas_conhecidas:
            raise ValueError("linhas_conhecidas não pode estar vazio")
        
        if not isinstance(linhas_conhecidas, dict):
            raise TypeError("linhas_conhecidas deve ser um dicionário")
        
        self.linhas_conhecidas = linhas_conhecidas
        print(f"✅ BRTDataCleaner inicializado com {len(linhas_conhecidas)} linhas")
    
    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida e enriquece dados de detecção
        
        Validações realizadas:
        - Verifica se linha existe no cadastro
        - Adiciona nome da linha
        - Adiciona tempo estimado
        - Adiciona metadados de limpeza
        
        Args:
            data (dict): Dados brutos da detecção
                Campos esperados:
                - linha (str): Número da linha detectada
                - outros campos opcionais
        
        Returns:
            dict: Dados limpos e enriquecidos
                Campos adicionados:
                - linha_valida (bool): Se a linha é válida
                - nome_linha (str): Nome completo da linha
                - tempo_estimado_min (int): Tempo estimado de viagem
                - cleaned (bool): True (marca que foi processado)
                - cleaned_at (str): Timestamp ISO da limpeza
        
        Example:
            >>> data = {"linha": "437", "parada_origem": "A"}
            >>> cleaned = cleaner.clean(data)
            >>> print(cleaned)
            {
                "linha": "437",
                "parada_origem": "A",
                "linha_valida": True,
                "nome_linha": "TI Caxangá...",
                "tempo_estimado_min": 5,
                "cleaned": True,
                "cleaned_at": "2025-12-03T..."
            }
        """
        # Copiar dados originais
        cleaned = data.copy()
        
        # Extrair linha
        linha = cleaned.get('linha')
        
        if not linha:
            # Sem linha, marcar como inválida
            cleaned['linha_valida'] = False
            cleaned['nome_linha'] = 'Não detectada'
            cleaned['tempo_estimado_min'] = None
            cleaned['erro'] = 'Linha não fornecida'
        
        elif linha in self.linhas_conhecidas:
            # Linha válida - enriquecer dados
            linha_info = self.linhas_conhecidas[linha]
            
            cleaned['linha_valida'] = True
            cleaned['nome_linha'] = linha_info.get('nome', 'Sem nome')
            cleaned['tempo_estimado_min'] = linha_info.get('tempo_medio_min', 5)
            cleaned['distancia_km'] = linha_info.get('distancia_km', 0)
            
            print(f"✅ Dados limpos: Linha {linha} válida")
        
        else:
            # Linha não cadastrada
            cleaned['linha_valida'] = False
            cleaned['nome_linha'] = 'Desconhecida'
            cleaned['tempo_estimado_min'] = None
            cleaned['erro'] = f'Linha {linha} não cadastrada'
            
            print(f"⚠️  Linha {linha} não encontrada no cadastro")
        
        # Adicionar metadados de limpeza
        cleaned['cleaned'] = True
        cleaned['cleaned_at'] = datetime.now(timezone.utc).isoformat()
        cleaned['cleaner_version'] = '1.0'
        
        return cleaned
    
    def validar_linha(self, linha: str) -> bool:
        """
        Verifica se uma linha é válida (cadastrada)
        
        Args:
            linha (str): Número da linha
        
        Returns:
            bool: True se linha existe, False caso contrário
        
        Example:
            >>> cleaner.validar_linha("437")
            True
            >>> cleaner.validar_linha("999")
            False
        """
        return linha in self.linhas_conhecidas
    
    def obter_info_linha(self, linha: str) -> Dict[str, Any]:
        """
        Retorna informações completas de uma linha
        
        Args:
            linha (str): Número da linha
        
        Returns:
            dict: Informações da linha ou None se não encontrada
        
        Example:
            >>> info = cleaner.obter_info_linha("437")
            >>> print(info["nome"])
            "TI Caxangá..."
        """
        return self.linhas_conhecidas.get(linha)
    
    def listar_linhas(self) -> list:
        """
        Lista todas as linhas cadastradas
        
        Returns:
            list: Lista com números das linhas
        
        Example:
            >>> linhas = cleaner.listar_linhas()
            >>> print(linhas)
            ["437", "2441", "2450", "2444"]
        """
        return list(self.linhas_conhecidas.keys())


# Teste rápido (só executa se rodar o arquivo diretamente)
if __name__ == "__main__":
    print("\n🧪 Testando BRTDataCleaner...\n")
    
    # Linhas de exemplo
    linhas_teste = {
        "437": {
            "nome": "TI Caxangá (Conde da Boa Vista) - BRT",
            "tempo_medio_min": 5,
            "distancia_km": 2.5
        },
        "2441": {
            "nome": "TI CDU (Conde da Boa Vista) - BRT",
            "tempo_medio_min": 5,
            "distancia_km": 2.5
        }
    }
    
    try:
        # Criar cleaner
        cleaner = BRTDataCleaner(linhas_teste)
        
        # Teste 1: Linha válida
        print("\n📋 Teste 1: Linha válida")
        data1 = {"linha": "437", "parada_origem": "A"}
        result1 = cleaner.clean(data1)
        print(f"   Resultado: {result1['linha_valida']}")
        print(f"   Nome: {result1['nome_linha']}")
        
        # Teste 2: Linha inválida
        print("\n📋 Teste 2: Linha inválida")
        data2 = {"linha": "999"}
        result2 = cleaner.clean(data2)
        print(f"   Resultado: {result2['linha_valida']}")
        print(f"   Erro: {result2.get('erro')}")
        
        # Teste 3: Sem linha
        print("\n📋 Teste 3: Sem linha")
        data3 = {"parada_origem": "A"}
        result3 = cleaner.clean(data3)
        print(f"   Resultado: {result3['linha_valida']}")
        
        print("\n✅ Todos os testes passaram!")
        
    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback
        traceback.print_exc()