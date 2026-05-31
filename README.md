# 🎬 YouTube Vídeo Downloader

Aplicativo desktop para baixar vídeos do YouTube com interface gráfica moderna, desenvolvido em Python com CustomTkinter e yt-dlp.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-informational?style=flat-square)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

---

## 📸 Visão Geral

Uma aplicação desktop completa que permite baixar vídeos do YouTube de forma simples e direta. O app conta com uma interface escura e elegante, barra de progresso em tempo real, controle de cancelamento e escolha da pasta de destino.

---

## ✨ Funcionalidades

- **Download de vídeos** em alta qualidade (formato MP4, codec H.264)
- **Barra de progresso em tempo real** com porcentagem, velocidade e tempo restante
- **Cancelamento de download** com limpeza automática de arquivos parciais (`.part`, `.ytdl`)
- **Escolha da pasta de destino** via seletor de diretório nativo do sistema
- **Interface dark mode** limpa e responsiva
- **Tratamento de erros** com mensagens amigáveis ao usuário
- **Thread separada** para o download, mantendo a UI sempre responsiva

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| [Python 3.8+](https://www.python.org/) | Linguagem base do projeto |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Interface gráfica moderna com tema escuro |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Engine de download de vídeos |
| `threading` | Download assíncrono sem travar a UI |
| `tkinter` | Diálogos nativos (messagebox, filedialog) |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip

### Instalação

1. **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/youtube-downloader.git
cd youtube-downloader
```

2. **Instale as dependências:**

```bash
pip install customtkinter yt-dlp
```

3. **Execute o aplicativo:**

```bash
python baixador_premium.py
```

---

## 📖 Como Usar

1. Cole o link do vídeo do YouTube no campo indicado
2. Opcionalmente, clique em **ESCOLHER** para selecionar a pasta de destino
3. Clique em **BAIXAR VÍDEO** para iniciar
4. Acompanhe o progresso pela barra e pelo status na parte inferior
5. Para interromper, clique em **PARAR** — os arquivos parciais são removidos automaticamente

---

## 🗂️ Estrutura do Projeto

```
youtube-downloader/
│
├── baixador_premium.py   # Código principal — UI e lógica de download
└── README.md
```

### Principais componentes do código

- **`YoutubeVideoDownloader`** — classe principal que herda de `ctk.CTk` e centraliza toda a lógica
- **`hook_progresso()`** — callback chamado pelo yt-dlp a cada chunk baixado para atualizar a UI
- **`baixar_video()`** — executado em thread separada para não bloquear a interface
- **`apagar_arquivos_parciais()`** — limpa resíduos de download cancelado na pasta de destino
- **`limpar_codigo_terminal()`** — remove escape codes ANSI das strings retornadas pelo yt-dlp

---

## ⚙️ Configuração de Download

O formato escolhido prioriza a melhor qualidade compatível com MP4:

```python
"format": "bv*[vcodec^=avc1]+ba[ext=m4a]/b[ext=mp4]/best"
```

Isso garante:
- Vídeo com codec **H.264 (avc1)** — máxima compatibilidade
- Áudio em **M4A** mesclado no container final
- Fallback automático para o melhor formato disponível

---

## 🔒 Aviso Legal

Este projeto foi desenvolvido para fins educacionais e de portfólio. Utilize apenas para baixar conteúdos que você tem autorização para baixar, respeitando os [Termos de Serviço do YouTube](https://www.youtube.com/t/terms) e os direitos autorais dos criadores.

---

## 👨‍💻 Autor

Feito com 💙 por **[Eduardo Moura Sekeff](https://github.com/eduardosekeffadv-eng)**

---

*Sinta-se à vontade para abrir uma issue ou enviar um pull request com sugestões de melhoria!*
