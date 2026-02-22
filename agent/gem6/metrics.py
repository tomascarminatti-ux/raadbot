from typing import Dict, List, Any
import statistics
from datetime import datetime, timezone
from collections import defaultdict

class MetricsCollector:
    """
    Recolección y exportación de métricas de performance y calidad en tiempo real.
    """
    
    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
        self.histograms: Dict[str, List[float]] = defaultdict(list)
        self.gauges: Dict[str, float] = defaultdict(float)
        self.start_time = datetime.now(timezone.utc)
        
    def increment(self, metric_name: str, value: int = 1):
        """Incrementa un contador."""
        current = self.counters[metric_name]
        self.counters[metric_name] = current + value
        
    def record_histogram(self, metric_name: str, value: float):
        """Registra un valor en un histograma (ej: duración)."""
        current_list = self.histograms[metric_name]
        current_list.append(value)
        self.histograms[metric_name] = current_list
        
    def set_gauge(self, metric_name: str, value: float):
        """Establece un valor instantáneo."""
        self.gauges[metric_name] = value
        
    def export(self) -> Dict[str, Any]:
        """Exporta todas las métricas en un formato estructurado."""
        results: Dict[str, Any] = {
            'counters': dict(self.counters),
            'histograms': {},
            'gauges': dict(self.gauges),
            'uptime_seconds': (datetime.now(timezone.utc) - self.start_time).total_seconds()
        }

        for name, values in self.histograms.items():
            if not values:
                continue
            results['histograms'][name] = {
                'count': len(values),
                'sum': sum(values),
                'avg': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'p95': self._percentile(values, 95)
            }
            
        return results
    
    def _percentile(self, values: List[float], p: int) -> float:
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * p / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
