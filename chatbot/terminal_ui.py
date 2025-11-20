from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box
import random

class ChatbotUI:
    def __init__(self):
        self.console = Console()
        self.colors = ["cyan", "magenta", "green", "yellow", "blue"]
    
    def show_welcome(self):
        """Tampilkan welcome message yang menarik"""
        welcome_text = Text()
        welcome_text.append("🤖 ", style="bold red")
        welcome_text.append("CHATBOT ASSISTANT", style="bold cyan")
        welcome_text.append("\nSelamat datang! Saya siap membantu Anda", style="green")
        
        self.console.print()
        self.console.print(
            Panel(
                welcome_text,
                box=box.DOUBLE,
                style="bright_blue",
                padding=(1, 2)
            )
        )
    
    def show_user_message(self, message):
        """Tampilkan pesan user di sebelah kanan"""
        user_panel = Panel(
            message,
            title="[bold yellow]YOU[/bold yellow]",
            title_align="right",
            box=box.ROUNDED,
            style="yellow",
            width=60
        )
        self.console.print(user_panel, justify="right")
    
    def show_bot_message(self, message, intent_name="", confidence=0):
        """Tampilkan pesan bot di sebelah kiri"""
        # Pilih color random untuk variasi
        color = random.choice(self.colors)
        
        # Buat content dengan info intent jika verbose
        content = message
        if intent_name and confidence > 0:
            content = f"{message}\n\n[dim][{intent_name} • {confidence}%][/dim]"
        
        bot_panel = Panel(
            content,
            title="[bold cyan]BOT[/bold cyan] 🤖",
            title_align="left",
            box=box.ROUNDED,
            style=color,
            width=60
        )
        self.console.print(bot_panel, justify="left")
    
    def show_typing_animation(self):
        """Tampilkan animasi typing"""
        with self.console.status("[bold green]Bot sedang mengetik...") as status:
            pass
    
    def show_intents_summary(self, intents_data):
        """Tampilkan summary intents dalam table yang rapi"""
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Intent", style="cyan", width=20)
        table.add_column("Patterns", style="green", width=10)
        table.add_column("Responses", style="yellow", width=10)
        table.add_column("Contoh Pattern", style="white", width=30)
        
        for intent_name, intent_data in intents_data.items():
            patterns = intent_data['patterns']
            responses = intent_data['responses']
            example = patterns[0] if patterns else "-"
            
            table.add_row(
                intent_name,
                str(len(patterns)),
                str(len(responses)),
                example
            )
        
        self.console.print()
        self.console.print(
            Panel(
                table,
                title="[bold green]📁 LOADED INTENTS[/bold green]",
                style="bright_blue"
            )
        )
    
    def show_conversation_history(self, history):
        """Tampilkan history percakapan"""
        if not history:
            self.console.print("[italic yellow]📝 Belum ada history percakapan[/italic yellow]")
            return
        
        table = Table(show_header=True, header_style="bold green", box=box.ROUNDED)
        table.add_column("No", style="cyan", width=5)
        table.add_column("User", style="yellow", width=30)
        table.add_column("Bot", style="blue", width=40)
        table.add_column("Intent", style="magenta", width=15)
        
        for i, conv in enumerate(history[-8:], 1):  # Tampilkan 8 terakhir
            table.add_row(
                str(i),
                conv['user'][:28] + "..." if len(conv['user']) > 28 else conv['user'],
                conv['bot'][:38] + "..." if len(conv['bot']) > 38 else conv['bot'],
                f"{conv['intent']} ({conv['confidence']}%)"
            )
        
        self.console.print()
        self.console.print(
            Panel(
                table,
                title=f"📝 CONVERSATION HISTORY ({len(history)} messages)",
                style="bright_blue"
            )
        )
    
    def show_help_commands(self):
        """Tampilkan help commands"""
        commands_table = Table(show_header=False, box=box.SIMPLE, style="dim")
        commands_table.add_column("Command", style="cyan")
        commands_table.add_column("Description", style="white")
        
        commands_table.add_row("quit", "Keluar dari chatbot")
        commands_table.add_row("history", "Lihat history percakapan")
        commands_table.add_row("intents", "Lihat loaded intents")
        commands_table.add_row("clear", "Bersihkan layar")
        commands_table.add_row("help", "Tampilkan bantuan ini")
        
        self.console.print()
        self.console.print(
            Panel(
                commands_table,
                title="[bold yellow]🛠️ AVAILABLE COMMANDS[/bold yellow]",
                style="bright_green"
            )
        )
    
    def show_error(self, message):
        """Tampilkan error message"""
        self.console.print(f"[bold red]❌ {message}[/bold red]")
    
    def clear_screen(self):
        """Bersihkan layar"""
        self.console.clear()
    
    def print_separator(self):
        """Print separator line"""
        self.console.print("\n[dim]" + "─" * 50 + "[/dim]\n")