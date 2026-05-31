import os
import sys
import re
import threading
import customtkinter as ctk
import yt_dlp
from tkinter import messagebox, filedialog


def pasta_do_executavel():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def limpar_codigo_terminal(texto):
    if texto is None:
        return ""
    texto = str(texto)
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


class DownloadCancelado(Exception):
    pass


class YoutubeVideoDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Youtube Vídeo Downloader")
        self.geometry("760x520")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.pasta_destino = pasta_do_executavel()
        self.cancelar_download = False
        self.download_em_andamento = False

        self.criar_interface()

    def criar_interface(self):
        self.configure(fg_color="#070A12")

        self.container = ctk.CTkFrame(
            self,
            width=700,
            height=455,
            corner_radius=28,
            fg_color="#111827",
            border_width=1,
            border_color="#26344D"
        )
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.titulo = ctk.CTkLabel(
            self.container,
            text="YOUTUBE VÍDEO DOWNLOADER",
            font=("Segoe UI", 28, "bold"),
            text_color="#F8FAFC"
        )
        self.titulo.place(x=45, y=35)

        self.subtitulo = ctk.CTkLabel(
            self.container,
            text="Baixe vídeos autorizados em alta qualidade e escolha onde salvar.",
            font=("Segoe UI", 14),
            text_color="#9DB2D6"
        )
        self.subtitulo.place(x=48, y=78)

        self.label_link = ctk.CTkLabel(
            self.container,
            text="Link do vídeo",
            font=("Segoe UI", 14, "bold"),
            text_color="#E5F0FF"
        )
        self.label_link.place(x=50, y=122)

        self.entrada_link = ctk.CTkEntry(
            self.container,
            width=600,
            height=46,
            corner_radius=14,
            placeholder_text="Cole aqui o link do vídeo...",
            font=("Segoe UI", 14),
            fg_color="#0B1220",
            border_color="#2F80ED",
            border_width=1,
            text_color="#FFFFFF",
            placeholder_text_color="#667799"
        )
        self.entrada_link.place(x=50, y=150)

        self.label_destino = ctk.CTkLabel(
            self.container,
            text="Pasta de destino",
            font=("Segoe UI", 14, "bold"),
            text_color="#E5F0FF"
        )
        self.label_destino.place(x=50, y=210)

        self.campo_destino = ctk.CTkEntry(
            self.container,
            width=430,
            height=42,
            corner_radius=14,
            font=("Segoe UI", 12),
            fg_color="#0B1220",
            border_color="#26344D",
            border_width=1,
            text_color="#CBD5E1"
        )
        self.campo_destino.place(x=50, y=238)
        self.campo_destino.insert(0, self.pasta_destino)
        self.campo_destino.configure(state="disabled")

        self.botao_escolher = ctk.CTkButton(
            self.container,
            text="ESCOLHER",
            width=150,
            height=42,
            corner_radius=14,
            font=("Segoe UI", 13, "bold"),
            fg_color="#1F2937",
            hover_color="#374151",
            command=self.escolher_pasta
        )
        self.botao_escolher.place(x=500, y=238)

        self.botao_baixar = ctk.CTkButton(
            self.container,
            text="BAIXAR VÍDEO",
            width=190,
            height=48,
            corner_radius=16,
            font=("Segoe UI", 15, "bold"),
            fg_color="#2F80ED",
            hover_color="#1C64D1",
            command=self.iniciar_download
        )
        self.botao_baixar.place(x=50, y=305)

        self.botao_parar = ctk.CTkButton(
            self.container,
            text="PARAR",
            width=130,
            height=48,
            corner_radius=16,
            font=("Segoe UI", 14, "bold"),
            fg_color="#7F1D1D",
            hover_color="#991B1B",
            command=self.parar_download,
            state="disabled"
        )
        self.botao_parar.place(x=255, y=305)

        self.botao_limpar = ctk.CTkButton(
            self.container,
            text="LIMPAR",
            width=130,
            height=48,
            corner_radius=16,
            font=("Segoe UI", 14, "bold"),
            fg_color="#1F2937",
            hover_color="#374151",
            command=self.limpar
        )
        self.botao_limpar.place(x=400, y=305)

        self.progress_bar = ctk.CTkProgressBar(
            self.container,
            width=600,
            height=16,
            corner_radius=10,
            progress_color="#2F80ED",
            fg_color="#1F2937"
        )
        self.progress_bar.place(x=50, y=385)
        self.progress_bar.set(0)

        self.status = ctk.CTkLabel(
            self.container,
            text="Aguardando link...",
            font=("Segoe UI", 13),
            text_color="#9CA3AF"
        )
        self.status.place(x=50, y=413)

    def atualizar_status(self, texto, cor="#DCE7FF"):
        texto = limpar_codigo_terminal(texto)
        self.after(0, lambda: self.status.configure(text=texto, text_color=cor))

    def atualizar_progresso(self, valor):
        self.after(0, lambda: self.progress_bar.set(valor))

    def escolher_pasta(self):
        if self.download_em_andamento:
            return

        pasta = filedialog.askdirectory(title="Escolha onde salvar o vídeo")

        if pasta:
            self.pasta_destino = pasta

            self.campo_destino.configure(state="normal")
            self.campo_destino.delete(0, "end")
            self.campo_destino.insert(0, self.pasta_destino)
            self.campo_destino.configure(state="disabled")

            self.atualizar_status("Pasta de destino atualizada.", "#22C55E")

    def limpar(self):
        if self.download_em_andamento:
            messagebox.showwarning(
                "Download em andamento",
                "Pare o download antes de limpar os campos."
            )
            return

        self.entrada_link.delete(0, "end")
        self.progress_bar.set(0)
        self.atualizar_status("Aguardando link...", "#9CA3AF")

    def iniciar_download(self):
        url = self.entrada_link.get().strip()

        if not url:
            messagebox.showwarning("Atenção", "Cole um link antes de baixar.")
            return

        self.cancelar_download = False
        self.download_em_andamento = True

        self.botao_baixar.configure(state="disabled", text="BAIXANDO...")
        self.botao_parar.configure(state="normal")
        self.botao_escolher.configure(state="disabled")
        self.botao_limpar.configure(state="disabled")

        self.progress_bar.set(0)
        self.atualizar_status("Preparando download...", "#DCE7FF")

        thread = threading.Thread(target=self.baixar_video, args=(url,), daemon=True)
        thread.start()

    def parar_download(self):
        if self.download_em_andamento:
            self.cancelar_download = True
            self.botao_parar.configure(state="disabled", text="PARANDO...")
            self.atualizar_status("Cancelando download...", "#FBBF24")

    def hook_progresso(self, d):
        if self.cancelar_download:
            raise DownloadCancelado("Download cancelado pelo usuário.")

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            baixado = d.get("downloaded_bytes", 0)

            velocidade = limpar_codigo_terminal(d.get("_speed_str", "")).strip()
            eta = limpar_codigo_terminal(d.get("_eta_str", "")).strip()

            if total:
                progresso = baixado / total
                porcentagem = int(progresso * 100)

                self.atualizar_progresso(progresso)
                self.atualizar_status(
                    f"Baixando... {porcentagem}% | {velocidade} | Restante: {eta}",
                    "#DCE7FF"
                )
            else:
                self.atualizar_status(
                    "Baixando... calculando progresso...",
                    "#DCE7FF"
                )

        elif d["status"] == "finished":
            self.atualizar_progresso(1)
            self.atualizar_status(
                "Download concluído. Processando arquivo final...",
                "#22C55E"
            )

    def apagar_arquivos_parciais(self):
        """
        Remove arquivos temporários deixados pelo download cancelado.
        Normalmente o yt-dlp cria arquivos .part durante o processo.
        """
        try:
            for arquivo in os.listdir(self.pasta_destino):
                caminho = os.path.join(self.pasta_destino, arquivo)

                if arquivo.endswith(".part") or arquivo.endswith(".ytdl"):
                    os.remove(caminho)
        except Exception:
            pass

    def baixar_video(self, url):
        try:
            opcoes = {
                "format": "bv*[vcodec^=avc1]+ba[ext=m4a]/b[ext=mp4]/best",
                "outtmpl": os.path.join(self.pasta_destino, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",

                "socket_timeout": 60,
                "retries": 10,
                "fragment_retries": 10,
                "continuedl": True,
                "noplaylist": True,

                "no_color": True,
                "quiet": True,
                "no_warnings": True,

                "progress_hooks": [self.hook_progresso],
            }

            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([url])

            if not self.cancelar_download:
                self.atualizar_status(
                    "Pronto! Vídeo salvo na pasta escolhida.",
                    "#22C55E"
                )

                self.after(0, lambda: messagebox.showinfo(
                    "Concluído",
                    "Vídeo baixado com sucesso!"
                ))

        except DownloadCancelado:
            self.apagar_arquivos_parciais()
            self.atualizar_progresso(0)
            self.atualizar_status(
                "Download cancelado pelo usuário.",
                "#FBBF24"
            )

        except Exception as erro:
            if self.cancelar_download:
                self.apagar_arquivos_parciais()
                self.atualizar_progresso(0)
                self.atualizar_status(
                    "Download cancelado pelo usuário.",
                    "#FBBF24"
                )
            else:
                erro_limpo = limpar_codigo_terminal(str(erro))

                self.atualizar_status(
                    "Erro ao baixar o vídeo.",
                    "#EF4444"
                )

                self.after(0, lambda: messagebox.showerror(
                    "Erro",
                    f"Não foi possível baixar o vídeo:\n\n{erro_limpo}"
                ))

        finally:
            self.download_em_andamento = False
            self.cancelar_download = False

            self.after(0, lambda: self.botao_baixar.configure(
                state="normal",
                text="BAIXAR VÍDEO"
            ))

            self.after(0, lambda: self.botao_parar.configure(
                state="disabled",
                text="PARAR"
            ))

            self.after(0, lambda: self.botao_escolher.configure(
                state="normal"
            ))

            self.after(0, lambda: self.botao_limpar.configure(
                state="normal"
            ))


if __name__ == "__main__":
    app = YoutubeVideoDownloader()
    app.mainloop()