import random

class SimulatedDetector:
    def __init__(self):
        self.noise_level = 0.1  # Simulated noise level

    def get_intensity_reading(self):
        """Simulates real-time intensity readings"""
        return round(100 + random.uniform(-self.noise_level, self.noise_level) * 100, 2)

# Example usage
if __name__ == "__main__":
    sensor = SimulatedDetector()
    print(f"Simulated Intensity: {sensor.get_intensity_reading()}")
