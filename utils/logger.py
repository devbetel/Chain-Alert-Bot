import logging
from pathlib import Path

def start_logger(name: str = "bot") -> logging.Logger:
    
    logger= logging.getLogger(name)
    logger.setLevel(logging.DEBUG)   # Captura tudo (DEBUG, INFO, WARNING, ERROR)

    logs_dir= Path( "logs")
    logs_dir.mkdir(parents=True, exist_ok=True)  # Cria o diretório se não existir


    # Formato das mensagens de log

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configurando arquivo de log
    file_handler = logging.FileHandler(logs_dir / "botAlertaTelegram.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(log_format))

    # Configurando console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    # Configura o log para console 
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    return logger