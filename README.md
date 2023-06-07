# encode-decode-in-video

La rularea fișierului encode.py, se înregistrează un clip de 3 secunde cu ajutorul camerei web, apoi se extrage textul din imaginea din resurse image.png și este salvat în fișierul .txt. Ulterior, într-o secvență de 10 cadre aleasă aleator, se ascunde acel mesaj pe bucăți egale. Codecul corespunzător salvării fișierului este FFV1, deoarece prezintă o compresie fără pierderi.

La rularea fișierului decode.py, se decodează mesajul din clipul video și se afișează pe ecran.

Python-tesseract este un instrument open-source de recunoaștere a textului din diferite tipuri de imagini – JPEG, PNG, GIF, BMP, TIFF și nu numai. Acesta a fost dezvoltat pe baza motorului Tesseract OCR (Optical Character Recognition) de la Google și îl puteți instala cu ajutorul comenzii: pip install pytesseract.

Va trebui instalat înainte și Python Imaging Library (PIL), utilizând pip install Pillow, dar și executabilul tesseract-ocr-w64-setup-v4.0.0.20181030.exe de la adresa https://digi.bib.uni-mannheim.de/tesseract/ (pentru Windows). Pentru Linux sau MacOS, se poate instala Tesseract de la adresa: https://tesseract-ocr.github.io/tessdoc/Installation.html. 
