from loguru import logger
import sys
import os

LOG_PATH = "logs"
os.makedirs(LOG_PATH, exist_ok=True)

logger.remove()  # Quita el handler por defecto

# Log en consola
logger.add(sys.stderr, level="INFO")

# Log en archivo rotativo
logger.add(
	f"{LOG_PATH}/app.log",
	level="INFO",
	rotation="1 week",  	# Nueva versión semanal
	retention="1 month",	# Guarda logs por 1 mes
	compression="zip",  	# Comprime automáticamente
	backtrace=True,
	diagnose=True
)
