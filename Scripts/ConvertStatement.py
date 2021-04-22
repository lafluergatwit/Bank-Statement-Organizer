import pdfplumber
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\vidrinen\\Downloads\\BankStatement.json", scope)

client = gspread.authorize(creds)

spreadsheet = client.open("Testtest")
sheet = spreadsheet.sheet1

Header = ["Effective Date", "Business Date", "Description", "Amount"]
currentRow = 1

sheet.insert_row(Header, currentRow)
currentRow+=1

rows = []

def insert(wordList):
        colOne = wordList[0] + " " + wordList[1]
        colTwo = wordList[2] + " " + wordList[3]
        colThree = ""
        for i in range(4, (len(wordList)-2)):
            colThree += wordList[i] + " "
        colFour = wordList[len(wordList)-1]
        sheet.insert_row([colOne, colTwo, colThree, colFour], currentRow)
        currentRow += 1

with pdfplumber.open(r'C:\Users\vidrinen\Downloads\test.pdf') as pdf:
    for i in range(0, len(pdf.pages)):
        current_page = pdf.pages[i].extract_text()
        page = current_page.split("\n")
        correctInfo = False
        for line in page:
            words = line.split(" ")
            if(correctInfo):
                if(words[0]=="Continued"): correctInfo = False
                elif(words[0]=="TOTAL"):
                    correctInfo = False
                    sheet.update_cell(currentRow, 3, "Total: ")
                    sheet.update_cell(currentRow, 4, words[len(words)-1])
                    currentRow += 2
                elif(words[0]=="Eff."): continue
                else: 
                    insert(words)
            else:
                if(line=='Deposits and Credits'): correctInfo = True
                elif(line=='ATM and Debit Card Withdrawals'): correctInfo = True
                elif(line=='Electronic Withdrawals'): correctInfo = True