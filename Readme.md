## Descrição

O edge-risk-monitor é uma aplicação Python de computação de borda (edge computing) desenvolvida para realizar detecção automática de objetos de risco em tempo real a partir de um fluxo contínuo de vídeo proveniente de uma webcam.

O projeto integra uma Prova de Conceito (PoC) voltada ao monitoramento de risco químico em ambientes industriais, na qual o objeto de risco definido é um mouse de computador (com ou sem fio), utilizado como substituto conceitual de um item perigoso.

A aplicação executa inferência local utilizando técnicas de Visão Computacional e Deep Learning, reduzindo latência e dependência de servidores centrais. Quando uma detecção positiva ocorre, eventos estruturados são enviados para o backend risk-monitor-api, uma API REST desenvolvida em Django, por meio de requisições HTTP, permitindo o registro, a gestão e a análise centralizada das ocorrências.


## Responsabilidades:

* Captura de frames de uma webcam em tempo real
* Execução de inferência com modelo de detecção de objetos
* Identificação automática do objeto de risco
* Geração de evidências visuais das detecções
* Envio de eventos estruturados ao risk-monitor-api (Django REST API) via HTTP

## Tecnologias Utilizadas

* Python 3.x
* OpenCV (captura de vídeo)
* YOLO (detecção de objetos)
* Ultralytics
* Requests / HTTPX
* Logging padrão Python

## Integração com o Backend

O edge-risk-monitor atua como um cliente da API risk-monitor-api, desenvolvida com Django, responsável por:

* Receber os eventos de detecção
* Persistir os dados em banco de dados
* Gerenciar evidências associadas às ocorrências
* Disponibilizar informações para visualização e análise
* Toda a comunicação entre os sistemas ocorre de forma desacoplada via API REST, garantindo escalabilidade e facilidade de manutenção.

## Estrutura do Projeto

~~~sh

edge-risk-monitor/
├── main.py                 # Ponto de entrada da aplicação (orquestração)
├── README.md               # Documentação do projeto
├──                
│
├── logs/                   # Logs do sistema
│       └── edge-risk-monitor.log
│
├── utils/
│       ├── __init__.py
│       └── logging_global.py   # Logging global do sistema
│       └── system.py
│
├── webcam/
│       ├── __init__.py
│       └── webcam.py           # Captura de frames da webcam
│
├── detector/               # (futuro) Inferência YOLO
│       ├── __init__.py
│       └── detector.py
│
├── evidence/               # (futuro) Evidências visuais
│       ├── __init__.py
│       └── saver.py
│
├── sender/                 # Envio de eventos à API Django
│       ├── __init__.py
│       └── sender.py
│
└── config/                 # (Configurações do sistema
│        ├── __init__.py
│        └── settings.pys
~~~

#### Embora o backend utilize Django, o edge-risk-monitor não depende de frameworks web, mantendo-se leve, desacoplado e adequado para execução contínua em dispositivos de borda.