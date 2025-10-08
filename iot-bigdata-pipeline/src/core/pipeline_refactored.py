from typing import List
from src.core.interfaces import ISensor, IDataCleaner, IDataStore

class IoTPipeline:
    """Main IoT Pipeline following Single Responsibility and Open/Closed Principles"""
    
    def __init__(self, sensor: ISensor, cleaner: IDataCleaner, storage: IDataStore):
        self.sensor = sensor
        self.cleaner = cleaner
        self.storage = storage
        self.processed_count = 0
        self.error_count = 0
    
    def run_pipeline(self) -> bool:
        """Execute complete data pipeline"""
        try:
            # 1. Data Acquisition
            raw_data = self.sensor.read_data()
            print(f"📊 Dados brutos: {raw_data}")
            
            # 2. Data Cleaning
            cleaned_data = self.cleaner.clean(raw_data)
            
            if cleaned_data is None:
                print("⚠️  Dados descartados após limpeza")
                self.error_count += 1
                return False
            
            print(f"✨ Dados limpos: {cleaned_data}")
            
            # 3. Data Storage
            success = self.storage.save(cleaned_data)
            
            if success:
                self.processed_count += 1
                print(f"📈 Estatísticas: {self.processed_count} processados, {self.error_count} erros")
            else:
                self.error_count += 1
                
            return success
            
        except Exception as e:
            print(f"❌ Erro no pipeline: {e}")
            self.error_count += 1
            return False

class PipelineMonitor:
    """Monitor pipeline performance and health"""
    
    def __init__(self, pipeline: IoTPipeline):
        self.pipeline = pipeline
    
    def get_stats(self) -> dict:
        """Get pipeline statistics"""
        total = self.pipeline.processed_count + self.pipeline.error_count
        success_rate = (self.pipeline.processed_count / total * 100) if total > 0 else 0
        
        return {
            "processed": self.pipeline.processed_count,
            "errors": self.pipeline.error_count,
            "success_rate": round(success_rate, 2),
            "total_operations": total
        }