# Edge Risk Monitor – Monitoramento de Risco em Tempo Real

Aplicação desenvolvida em **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** para realizar **inferência em tempo real** com **Visão Computacional** como parte de uma **Prova de Conceito (PoC)** de um sistema de **monitoramento de risco químico em ambientes industriais**, utilizando **computação de borda (edge computing)**.

O sistema monitora um fluxo contínuo de imagens provenientes de uma webcam, identifica automaticamente a presença de um **objeto de risco** e, ao confirmar a ocorrência, gera evidências visuais e envia eventos estruturados para um backend desacoplado via API HTTP.

Nesta PoC, o objeto de risco definido é um **mouse de computador**, utilizado como substituto conceitual de um item perigoso.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Objetivos do Projeto

- Desenvolver um sistema de inferência local em tempo real (edge).
- Avaliar técnicas de detecção de objetos com foco em YOLO.
- Implementar debounce temporal para evitar falsos positivos.
- Gerar evidências visuais das detecções.
- Enviar eventos estruturados para um backend desacoplado (API).
- Garantir organização, legibilidade e rastreabilidade do código.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Funcionalidades

| Categoria | Descrição |
|----------|-----------|
| **Captura de Vídeo** | Leitura contínua de frames via webcam utilizando OpenCV. |
| **Inferência em Tempo Real** | Detecção de objetos de risco com modelo YOLO treinado. |
| **Debounce Temporal** | Confirma o risco apenas após múltiplos frames consecutivos. |
| **Filtro de Classe** | Considera apenas a classe de interesse definida em configuração. |
| **Geração de Evidências** | Salva imagens da detecção confirmada localmente. |
| **Envio de Eventos** | Envia dados e evidência para API REST (Django). |
| **Logs Estruturados** | Registro detalhado de eventos, falhas e estado do sistema. |
| **Execução em Edge** | Inferência local, sem dependência de serviços externos. |

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|----------|------------|
| **Linguagem** | **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** |
| **Visão Computacional** | **[OpenCV](https://docs.opencv.org/)** |
| **Deep Learning** | **[Ultralytics YOLO](https://docs.ultralytics.com/)** |
| **NumPy** | **[numpy](https://numpy.org/doc/)** |
| **HTTP Client** | **[requests](https://requests.readthedocs.io/en/latest/)** |
| **Logging** | **[logging](https://docs.python.org/pt-br/3/library/logging.html)** |
| **Sistema** | **uuid**, **pathlib**, **datetime** |

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Estrutura de Diretórios
```bash
edge-risk-monitor/
├── config/
│ ├── init.py
│ └── settings.py                              # Configurações centralizadas
│
├── detector/
│ ├── init.py
│ └── detector.py                              # Inferência YOLO
│
├── webcam/
│ ├── init.py
│ └── webcam.py                                # Captura de frames
│
├── evidence/
│ ├── init.py
│ └── saver.py                                 # Salvamento de evidências
│
├── sender/
│ ├── init.py
│ └── sender.py                                # Envio de eventos via HTTP
│
├── utils/
│ ├── init.py
│ ├── logging_global.py                        # Logging global do sistema
│ └── system.py                                # Funções auxiliares de sistema
│
├── outputs/
│ └── detection/                               # Evidências geradas
│
├── logs/
│ └── edge-risk-monitor.log                    # Logs da aplicação
│
├── models/
│ └── yolo_mouse.pt                            # Modelo YOLO treinado
│
├── main.py                                    # Orquestração da aplicação
│
├── requirements.txt                           # Dependências
│
├── documentação_técnica_edge-risk-monitor.pdf # Documentação Técnica
│
└── README.md                                  # Documentação
```

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Instalação e Execução

### Passo 1 – Criar ambiente virtual
```bash
$ python -m venv .venv
$ source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
```

### Passo 2 – Instalar dependências
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```
### Passo 3 – Executar o sistema
```bash
$ python main.py
```
A aplicação inicia a captura da webcam, executa inferência em tempo real e envia eventos ao backend configurado.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Estrutura do Evento Enviado

Ao detectar um objeto de risco confirmado, o sistema envia um evento contendo:

- **MAC:** Endereço MAC do dispositivo de monitoramento

- **DATE:** Data e hora da ocorrência

- **CLASS:** Classe do objeto detectado

- **EVIDENCE:** Imagem da evidência capturada

Os dados são enviados via **HTTP POST** para a **API** `risk-monitor-api`.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Observações Técnicas

- O sistema executa inferência local, adequado para ambientes industriais.

- O debounce temporal evita múltiplos envios para o mesmo evento.

- A arquitetura é desacoplada, permitindo integração com diferentes backends.

- O `main.py` atua exclusivamente como orquestrador do fluxo.

**━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━**

## Execução com API Mock

Para fins de desenvolvimento e testes locais, o projeto disponibiliza um **servidor mock** que simula o comportamento da API `risk-monitor-api`.

O uso do mock permite validar o envio de eventos sem a necessidade de executar o backend real em Django.

### Execução do mock
```bash
$ python mock/mock_server.py
```
Após iniciar o mock, o sistema pode ser executado normalmente:

```bash
$ python mock/main.py
```