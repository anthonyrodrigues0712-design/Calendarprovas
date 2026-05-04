import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def extrair_dados():
    # URL do Informatica Integrado (Area 7)
    url = "http://provas.euclidesdacunha.ifba.edu.br/index.php?view=month&area=7"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        calendario_completo = []
        
        # Procura por todas as linhas da tabela (turmas)
        linhas = soup.find_all('tr')
        
        for linha in linhas:
            th_turma = linha.find('th', data_room=True)
            if th_turma:
                nome_turma = th_turma.get_text(strip=True).replace('0', '')
                eventos_turma = []
                
                # Procura provas nos dias dessa turma
                celulas_dias = linha.find_all('td')
                for celula in celulas_dias:
                    link_dia = celula.find('a', href=True)
                    prova_div = celula.find('div', class_='I')
                    
                    if prova_div and link_dia:
                        # Extrai a data da URL do link
                        # Ex: index.php?page_date=2026-05-20...
                        href = link_dia['href']
                        data_str = href.split('page_date=')[1].split('&')[0]
                        materia = prova_div.get('title')
                        
                        eventos_turma.append({
                            "data": data_str,
                            "disciplina": materia
                        })
                
                if eventos_turma:
                    calendario_completo.append({
                        "turma": nome_turma,
                        "provas": eventos_turma
                    })

        # Salva os dados
        resultado = {
            "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "dados": calendario_completo
        }
        
        with open('dados_provas.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        
        print("Dados atualizados com sucesso!")

    except Exception as e:
        print(f"Erro ao extrair dados: {e}")

if __name__ == "__main__":
    extrair_dados()