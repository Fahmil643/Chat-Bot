import json
import os
from fuzzywuzzy import fuzz, process

class DialogflowIntentParser:
    def __init__(self, intents_folder="intents", verbose=False):
        self.intents_folder = intents_folder
        self.loaded_intents = {}
        self.verbose = verbose  # Tambahkan mode verbose
        self.load_intents()
    
    def load_intents(self):
        """Load semua file JSON intent dari folder"""
        if not os.path.exists(self.intents_folder):
            print(f"❌ Folder '{self.intents_folder}' tidak ditemukan!")
            return
        
        loaded_count = 0
        for filename in os.listdir(self.intents_folder):
            if filename.endswith('.json'):
                intent_name = filename.replace('.json', '')
                file_path = os.path.join(self.intents_folder, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        intent_data = json.load(file)
                        self.loaded_intents[intent_name] = self.parse_intent(intent_data)
                        loaded_count += 1
                        if self.verbose:
                            print(f"✅ Loaded intent: {intent_name}")
                            print(f"   Patterns: {self.loaded_intents[intent_name]['patterns']}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
        
        if not self.verbose:
            print(f"✅ Loaded {loaded_count} intents")
    
    def parse_intent(self, intent_data):
        """Parse data intent dari format Dialogflow"""
        patterns = []
        
        # Extract user questions/patterns
        for user_say in intent_data.get('userSays', []):
            full_text = ''.join([item.get('text', '') for item in user_say.get('data', [])])
            if full_text.strip():
                patterns.append(full_text.lower())
        
        # Extract bot response
        responses = ["Maaf, saya belum bisa menjawab itu."]
        if intent_data.get('responses'):
            messages = intent_data['responses'][0].get('messages', [])
            for msg in messages:
                if msg.get('type') == 'message' and msg.get('speech'):
                    responses = msg['speech']
                    break
        
        return {
            'name': intent_data.get('name', 'unknown'),
            'patterns': patterns,
            'responses': responses,
            'original_data': intent_data
        }
    
    def find_best_match(self, user_input, threshold=50):
        """Cari intent terbaik yang match dengan input user"""
        user_input = user_input.lower().strip()
        best_match = None
        best_score = 0
        best_pattern = ""
        
        if self.verbose:
            print(f"🔍 Searching for: '{user_input}'")
        
        for intent_name, intent_data in self.loaded_intents.items():
            for pattern in intent_data['patterns']:
                # Multiple matching strategies
                exact_match = user_input == pattern
                contains_match = pattern in user_input or user_input in pattern
                fuzzy_score = fuzz.partial_ratio(user_input, pattern)
                
                if self.verbose:
                    print(f"   Comparing with '{pattern}': exact={exact_match}, contains={contains_match}, fuzzy={fuzzy_score}%")
                
                # Priority: exact match > contains match > fuzzy match
                if exact_match:
                    best_score = 100
                    best_match = intent_data
                    best_pattern = pattern
                    break
                elif contains_match and best_score < 90:
                    best_score = 90
                    best_match = intent_data
                    best_pattern = pattern
                elif fuzzy_score > best_score and fuzzy_score >= threshold:
                    best_score = fuzzy_score
                    best_match = intent_data
                    best_pattern = pattern
            
            if best_score == 100:
                break
        
        if self.verbose and best_match:
            print(f"🎯 BEST MATCH: '{best_pattern}' (score: {best_score}%)")
        elif self.verbose:
            print(f"❌ NO MATCH FOUND (threshold: {threshold}%)")
        
        return best_match, best_score