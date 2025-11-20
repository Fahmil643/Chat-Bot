from chatbot import SimpleChatbot
from chatbot.terminal_ui import ChatbotUI
import argparse
import time

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Beautiful Chatbot')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode dengan detail debugging')
    parser.add_argument('--show-intents', '-s', action='store_true', help='Tampilkan intents pada startup')
    args = parser.parse_args()
    
    # Inisialisasi UI dan chatbot
    ui = ChatbotUI()
    chatbot = SimpleChatbot("intents", verbose=args.verbose)
    
    # Clear screen dan tampilkan welcome
    ui.clear_screen()
    ui.show_welcome()
    
    # Check jika ada intent yang loaded
    if not chatbot.parser.loaded_intents:
        ui.show_error("Tidak ada intent yang berhasil di-load! Pastikan folder 'intents' berisi file JSON")
        return
    
    # Hanya tampilkan intents jika diminta secara explicit
    if args.show_intents:
        ui.show_intents_summary(chatbot.parser.loaded_intents)
    
    # Tampilkan help commands
    ui.show_help_commands()
    ui.print_separator()
    
    # Main chat loop
    while True:
        try:
            user_input = input("💬 You: ").strip()
            
            if user_input.lower() == 'quit':
                ui.show_bot_message("Sampai jumpa! Terima kasih telah chatting dengan saya 😊")
                break
            elif user_input.lower() == 'history':
                chatbot.show_conversation_history()
                ui.print_separator()
                continue
            elif user_input.lower() == 'intents':
                chatbot.show_loaded_intents()
                ui.print_separator()
                continue
            elif user_input.lower() == 'clear':
                chatbot.clear_screen()
                ui.show_welcome()
                if args.show_intents:
                    ui.show_intents_summary(chatbot.parser.loaded_intents)
                ui.show_help_commands()
                ui.print_separator()
                continue
            elif user_input.lower() == 'help':
                chatbot.show_help()
                ui.print_separator()
                continue
            elif user_input.lower() == '':
                continue
            
            # Tampilkan pesan user
            ui.show_user_message(user_input)
            
            # Tampilkan typing animation
            ui.show_typing_animation()
            
            # Dapatkan response
            response, intent_name, confidence = chatbot.get_response(user_input)
            
            # Tampilkan response bot
            if chatbot.verbose:
                ui.show_bot_message(response, intent_name, confidence)
            else:
                ui.show_bot_message(response)
            
            ui.print_separator()
            
        except KeyboardInterrupt:
            ui.show_bot_message("Chat dihentikan. Sampai jumpa! 👋")
            break
        except Exception as e:
            ui.show_error(f"Error: {e}")
            ui.print_separator()

if __name__ == "__main__":
    main()