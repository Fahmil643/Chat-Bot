from .dialogflow_parser import DialogflowIntentParser
from .terminal_ui import ChatbotUI
import random

class SimpleChatbot:
    def __init__(self, intents_folder="intents", verbose=False, show_intents_on_startup=False):
        self.parser = DialogflowIntentParser(intents_folder, verbose)
        self.conversation_history = []
        self.verbose = verbose
        self.ui = ChatbotUI()
        self.show_intents_on_startup = show_intents_on_startup
        
        # Auto-show intents hanya jika diminta
        if self.show_intents_on_startup and self.parser.loaded_intents:
            self.show_loaded_intents()
    
    def get_response(self, user_input):
        """Dapatkan response berdasarkan input user"""
        if not user_input.strip():
            return "Silakan ketik pesan Anda...", "", 0
        
        # Cari intent yang cocok
        best_match, score = self.parser.find_best_match(user_input)
        
        if best_match:
            # Pilih random response
            if len(best_match['responses']) > 1:
                response = random.choice(best_match['responses'])
            else:
                response = best_match['responses'][0] if best_match['responses'] else "Maaf, tidak ada response yang tersedia."
            
            # Simpan ke history
            self.conversation_history.append({
                'user': user_input,
                'bot': response,
                'intent': best_match['name'],
                'confidence': score
            })
            
            return response, best_match['name'], score
        else:
            fallback = "Maaf, saya belum memahami pertanyaan Anda. Coba tanya dengan cara lain atau ketik 'help' untuk bantuan."
            self.conversation_history.append({
                'user': user_input,
                'bot': fallback,
                'intent': 'fallback',
                'confidence': 0
            })
            return fallback, 'fallback', 0
    
    def show_conversation_history(self):
        """Tampilkan history percakapan melalui UI"""
        self.ui.show_conversation_history(self.conversation_history)
    
    def show_loaded_intents(self):
        """Tampilkan intents melalui UI"""
        if self.parser.loaded_intents:
            self.ui.show_intents_summary(self.parser.loaded_intents)
        else:
            self.ui.show_error("Tidak ada intent yang tersedia")
    
    def show_help(self):
        """Tampilkan help commands"""
        self.ui.show_help_commands()
    
    def clear_screen(self):
        """Bersihkan layar"""
        self.ui.clear_screen()
    
    def get_loaded_intents_count(self):
        """Dapatkan jumlah intents yang loaded (untuk info saja)"""
        return len(self.parser.loaded_intents)