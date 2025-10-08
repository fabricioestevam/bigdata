import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import time
from dotenv import load_dotenv

# Importações absolutas
from core.sensors import SensorFactory
from data_cleaning.cleaners import DataCleaner
from core.storage import MongoDBStore
from core.pipeline_refactored import IoTPipeline, PipelineMonitor
from config import Config

# Load environment variables
load_dotenv()

def main():
    """
    IoT Big Data Pipeline - Main Application
    """
    
    print("🚀 Iniciando IoT Big Data Pipeline...")
    print("=" * 50)
    
    try:
        # 1. Factory Pattern for sensor creation
        sensor = SensorFactory.create_sensor("DHT22")
        
        # 2. Cleaning strategy
        cleaner = DataCleaner()
        
        # 3. Dependency Injection for storage
        storage = MongoDBStore()
        
        # 4. Create main pipeline
        pipeline = IoTPipeline(sensor, cleaner, storage)
        monitor = PipelineMonitor(pipeline)
        
        print("✅ Pipeline inicializado com sucesso!")
        print(f"📊 Configuração: Simulação={Config.SENSOR_SIMULATION}, Intervalo={Config.DATA_GENERATION_INTERVAL}s")
        print("=" * 50)
        
        # 5. Main execution loop
        iteration = 0
        while True:
            iteration += 1
            print(f"\n🔄 Iteração #{iteration}")
            
            success = pipeline.run_pipeline()
            
            # Show stats every 5 iterations
            if iteration % 5 == 0:
                stats = monitor.get_stats()
                print(f"📈 Estatísticas do Pipeline: {stats}")
            
            time.sleep(Config.DATA_GENERATION_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Pipeline interrompido pelo usuário")
        
        # Final statistics
        if 'monitor' in locals():   
            stats = monitor.get_stats()
            print(f"📊 Estatísticas Finais: {stats}")
        
    except Exception as e:
        print(f"❌ Erro crítico no pipeline: {e}")
        raise

if __name__ == "__main__":
    main()