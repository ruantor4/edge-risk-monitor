# Edge Risk Monitor – Monitoramento de Risco em Tempo Real

Aplicação desenvolvida em **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** para realizar **inferência em tempo real com Visão Computacional**, voltada ao **monitoramento de risco químico em ambientes industriais**, utilizando **computação de borda (edge computing)**.

O sistema monitora continuamente um fluxo de imagens provenientes de uma webcam, identifica automaticamente a presença de um **objeto de risco** e, ao confirmar a ocorrência por critérios temporais e estatísticos, gera evidências visuais e envia eventos estruturados para um backend desacoplado via **API HTTP**.

Neste contexto de desenvolvimento, o objeto de risco configurado é um **mouse de computador**, utilizado como elemento representativo de um item perigoso para validação do fluxo completo de monitoramento.

---

## Objetivos do Sistema

- Executar inferência local em tempo real (edge computing).
- Detectar objetos de risco utilizando modelos de detecção baseados em **YOLO**.
- Aplicar decisão temporal para redução de falsos positivos.
- Gerar evidências visuais rastreáveis das detecções confirmadas.
- Enviar eventos estruturados para um backend desacoplado.
- Garantir organização, legibilidade, rastreabilidade e manutenibilidade do código.

---

## Funcionalidades

| Categoria | Descrição |
|---------|-----------|
| **Captura de Vídeo** | Leitura contínua de frames via webcam utilizando **[OpenCV](https://docs.opencv.org/)**. |
| **Inferência em Tempo Real** | Detecção de objetos de risco com modelo **[Ultralytics YOLO](https://docs.ultralytics.com/)**. |
| **Decisão Temporal** | Confirmação do risco baseada em média de confiança entre múltiplos frames. |
| **Filtro de Classe** | Processamento exclusivo da classe de interesse definida em configuração. |
| **Geração de Evidências** | Salvamento local de imagens associadas à detecção confirmada. |
| **Envio de Eventos** | Envio de dados estruturados e evidência para API REST externa. |
| **Logs Estruturados** | Registro detalhado de eventos, falhas e estados do sistema. |
| **Execução em Edge** | Inferência local, sem dependência de serviços externos em tempo real. |

---

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|---------|------------|
| **Linguagem** | **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** |
| **Visão Computacional** | **[OpenCV](https://docs.opencv.org/)** |
| **Deep Learning** | **[Ultralytics YOLO](https://docs.ultralytics.com/)** |
| **Computação Numérica** | **[NumPy](https://numpy.org/doc/)** |
| **Cliente HTTP** | **[requests](https://requests.readthedocs.io/en/latest/)** |
| **Logging** | **[logging](https://docs.python.org/pt-br/3/library/logging.html)** |
| **Utilitários de Sistema** | **pathlib**, **uuid**, **datetime** |

---

## Estrutura de Diretórios

```bash
edge-risk-monitor/
├── config/
│   └── settings.py                    # Configurações centralizadas
│
├── detector/
│   └── detector.py                    # Inferência YOLO
│
├── webcam/
│   └── webcam.py                      # Captura de frames
│
├── evidence/
│   └── saver.py                       # Salvamento de evidências
│
├── sender/
│   └── sender.py                      # Envio de eventos via HTTP
│
├── utils/
│   ├── logging_global.py              # Logging global do sistema
│   └── system.py                      # Utilitários de sistema
│
├── outputs/
│   └── detection/                     # Evidências geradas
│
├── logs/
│   └── edge-risk-monitor.log          # Logs da aplicação
│
├── models/
│   └── yolo_mouse.pt                  # Modelo YOLO treinado
│
├── main.py                            # Orquestração do pipeline
│
├── requirements.txt                   # Dependências
│
└── README.md                          # Documentação
```

---

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

---

## Estrutura do Evento Enviado

Ao detectar um objeto de risco confirmado, o sistema envia um evento contendo:

- **MAC:** Endereço MAC do dispositivo de monitoramento
- **DATE:** Data e hora da ocorrência
- **CLASS:** Classe do objeto detectado
- **EVIDENCE:** Imagem da evidência capturada

O evento é enviado via **HTTP POST** no formato multipart/form-data, contendo payload textual e arquivo de evidência, para a **API** `risk-monitor-api`.

---

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

---

## Observações Técnicas

- O sistema executa inferência local, adequado para ambientes industriais.
- A decisão temporal baseada em média de confiança reduz falsos positivos.
- A arquitetura é desacoplada, permitindo integração com diferentes backends.
- O `main.py` atua exclusivamente como orquestrador do fluxo.
- O foco do sistema é a confiabilidade da decisão baseada em evidência temporal, não benchmark de FPS.
