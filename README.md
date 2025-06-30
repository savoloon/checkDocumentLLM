Перед запуском установить все зависимости. Для того, чтобы скачать все зависимости нужно прописать в корне проекта: 
pip install -r requirements.txt


Важный момент, что для запуска Qwen лучше в проекте прописать cuda ядра, чтобы torch мог их использовать, чтобы узнать какая нужна версия, нужно открыть cmd консоль от админа и прописать: 
nvidia-smi

Возле версии драйвера будет надпись: 
CUDA Version: 12.6

В зависимости от версии переходишь на сайт: 
https://pytorch.org/get-started/locally/

Выставляешь нужные параметры Stable/Windows/pip/Python/CUDA...  и прям снизу будет запрос в виде: 
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
Этот запрос в корне проекта запускаешь!


Чтобы запустить проект для LLM Qwen нужно находясь в корне проекта в консоли прописать: 
uvicorn newApp:app --reload --host 0.0.0.0 --port 8000


Для того, чтобы запустить llama нужно находясь в корне проекта прописать: 
uvicorn app:app --reload --host 0.0.0.0 --port 8000
