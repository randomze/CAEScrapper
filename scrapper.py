from bs4 import BeautifulSoup
import requests

def verificarNif(nif):
    sum = 0
    for j in range(len(nif) - 1):
        sum += int(nif[j]) * (9 - j)

    remainder = sum // 11
    if remainder == 0 or remainder == 1:
        if int(nif[8] == 0):
            return True
    elif int(nif[8]) == (11 - remainder):
            return True
    return False

def fetchCAE(nif):
    if verificarNif(nif):
        url = "http://www.sicae.pt/Detalhe.aspx?NIPC="
        page = requests.get(url + nif)
        if page.status_code == 200:
            parsedPage = BeautifulSoup(page.content, 'html.parser')
            name = parsedPage.select_one("input#ctl00_MainContent_ipFirma")
            if name['value'] == "NIPC não encontrado":
                return []
            else:
                table = parsedPage.select("div#letrasCAE")
                mainCode = ""
                secondaryCodes = []
                for i  in range(len(table)):
                    if len(table[i].get_text()) == 5:
                        if table[i-1].get_text() == "CAE Principal":
                            mainCode = table[i].get_text()
                        else:
                            secondaryCodes.append(table[i].get_text())
                return [mainCode, secondaryCodes]
    else:
        return[]
