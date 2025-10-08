import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import time
from dotenv import load_dotenv

# Importações
from core.sensors import SensorFactory
from data_cleaning.cleaners import DataCleaner
from core.storage import MongoDBStore
from core.pipeline_refactored import IoTPipeline, PipelineMonitor
from config import Config

# Load environment variables
load_dotenv()

def main():
    """
    IoT Big Data Pipeline - Garantido para funcionar!
    """
    
    print("🚀 Iniciando IoT Big Data Pipeline...")
    print("=" * 50)
    
    try:
        # 1. Sensor
        sensor = SensorFactory.create_sensor("DHT22")
        
        # 2. Cleaner
        cleaner = DataCleaner()
        
        # 3. Storage (agora com fallback garantido)
        storage = MongoDBStore()
        
        # 4. Pipeline
        pipeline = IoTPipeline(sensor, cleaner, storage)
        monitor = PipelineMonitor(pipeline)
        
        print("✅ Pipeline inicializado com sucesso!")
        print("=" * 50)
        
        # 5. Loop principal
        iteration = 0
        while True:
            iteration += 1
            print(f"\n🔄 Iteração #{iteration}")
            
            pipeline.run_pipeline()
            
            # Estatísticas a cada 5 iterações
            if iteration % 5 == 0:
                stats = monitor.get_stats()
                print(f"📈 Estatísticas: {stats}")
            
            time.sleep(Config.DATA_GENERATION_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Pipeline interrompido pelo usuário")
        if 'monitor' in locals():
            stats = monitor.get_stats()
            print(f"📊 Estatísticas Finais: {stats}")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")

if __name__ == "__main__":
    main()