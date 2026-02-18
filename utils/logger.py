import logging
import os

def setup_logger():
    # Log dosyasının kaydedileceği dizini kontrol et
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Logger yapılandırması
    logging.basicConfig(
        filename='logs/iris_system.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger("IRIS")

# Proje genelinde kullanabileceğimiz bir nesne oluşturuyoruz
iris_logger = setup_logger()