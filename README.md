<img width="1583" height="437" alt="Screenshot 2025-11-20 221901" src="https://github.com/user-attachments/assets/1419e848-e2ce-4c6f-8ef9-8967b4c67645" />
<img width="1596" height="415" alt="Screenshot 2025-11-20 221942" src="https://github.com/user-attachments/assets/8f341160-846d-4668-b2ef-76767e6d523d" />

Penjelasan:
pada chat-bot tersebut dibuat bertujuan agar mengetahui seberapa workit penggunaan python dan json dalam pengolahan data untuk chatot, namun untuk kerapihan metode python dan json tersebut sangat mudah diguanakn namun harus ada file json
untuk file json agar lebih cepat didalam penggunaannya direkoemndasi menggunakan Dialogflow agar pengujian chatbotnya diuji didalam jawabanya

cara penggunaanya:
1. install python di vscode
2. text editor/IDE
3. file json

Persiapan Environment:
1. install di terminal ( pip install fuzzywuzzy python-levenshtein )
2. Untuk struktur foldernya
   chatbot_project/
│
├── main.py
├── intents/
│   └── askname_intent.json
├── chatbot/
│   ├── __init__.py
│   └── dialogflow_parser.py
└── requirements.txt

Untuk mempercantik pada pemanggilan chatbotnya harus menginstall library:
1. pip install rich
2. pip install colorama
3. update file requirements.txt
   dengan isi file:
   fuzzywuzzy==0.18.0
   python-levenshtein==0.21.1
   rich==13.7.0
