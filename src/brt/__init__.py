"""
Módulo BRT - Detecção de Ônibus
"""

# Não importar automaticamente para evitar erro no Codespace
# from .detector import BusDetector
# from .cleaner import BRTDataCleaner

# __all__ = ['BusDetector', 'BRTDataCleaner']

# Imports lazy (só quando necessário)
def get_detector(linhas_validas):
    """Carrega detector sob demanda"""
    from .detector import BusDetector
    return BusDetector(linhas_validas)

def get_cleaner(linhas_conhecidas):
    """Carrega cleaner sob demanda"""
    from .cleaner import BRTDataCleaner
    return BRTDataCleaner(linhas_conhecidas)

__all__ = ['get_detector', 'get_cleaner']