import pandas as pd
from apps.accounts.models import Assessor


# ex: Transformar string 'R$ 1.250,50' ou 1250.5 para float 1250.5
def limpar_decimal(valor):
    if valor == '' or valor is None:
        return '0.00'
    
    valor_limpo = valor.strip().replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
    valor_limpo = format(float(valor_limpo), '.2f')

    return float(valor_limpo)





def importar_excel_pj1(arquivo_excel):
    df = pd.read_excel(arquivo_excel)

    df = df.drop(
        columns=[
            "Cód. Assessor Indireto I",
            "Repasse (%) Assessor Indireto I",
            "Comissão (R$) Assessor Indireto I",
            "Cód. Assessor Indireto II",
            "Repasse (%) Assessor Indireto II",
            "Comissão (R$) Assessor Indireto II",
            "Cód. Assessor Indireto III",
            "Repasse (%) Assessor Indireto III",
            "Comissão (R$) Assessor Indireto III",
        ]
    )

    codigos_assessores = tuple(Assessor.objects.values_list('codigo_assessor', flat=True))

    for assessor in codigos_assessores:
        df_filtrado = df[df["Cód. Assessor Direto"] == assessor]
        print(df_filtrado)
        
    return None


# print(Assessor.cod_assessor)

# def importar_excel_pj1(arquivo_excel, data_competencia):
#     """
#     Lê a planilha de PJ1 e cria os registros vinculados a cada assessor.
#     """
#     wb = openpyxl.load_workbook(arquivo_excel, data_only=True)
#     sheet = wb.active
#     linhas = list(sheet.iter_rows(values_only=True))
#     if not linhas:
#         return 0
#     # Pega o cabeçalho (primeira linha)
#     cabecalho = [str(col).strip() if col else "" for col in linhas[0]]
#     total_salvo = 0
#     # Percorre as linhas a partir da segunda linha
#     for linha in linhas[1:]:
#         if not any(linha):  # Pula linhas vazias
#             continue
#         dados = dict(zip(cabecalho, linha))
        
#         # Pega o código do assessor na planilha
#         cod_assessor = str(dados.get("Cód. Assessor Direto") or dados.get("Cod. Assessor Direto") or "").strip()
#         if not cod_assessor:
#             continue
#         # Procura o assessor cadastrado no sistema
#         assessor = Assessor.objects.filter(codigo_assessor=cod_assessor).first()
#         if not assessor:
#             # Se o assessor ainda não estiver cadastrado, pula a linha (ou você pode cadastrá-lo antes)
#             continue
#         # Salva o lançamento no banco
#         LancamentoPJ1.objects.create(
#             assessor=assessor,
#             data=data_competencia,
#             categoria=str(dados.get("Categoria") or ""),
#             produto=str(dados.get("Produto") or "N/A"),
#             nivel_1=str(dados.get("Nível 1") or dados.get("Nivel 1") or ""),
#             nivel_2=str(dados.get("Nível 2") or dados.get("Nivel 2") or ""),
#             nivel_3=str(dados.get("Nível 3") or dados.get("Nivel 3") or ""),
#             cod_cliente=str(dados.get("Cód. Cliente") or dados.get("Cod. Cliente") or ""),
#             cod_assessor_direto=cod_assessor,
#             receita=limpar_decimal(dados.get("Receita (R$)")),
#             receita_liquida=limpar_decimal(dados.get("Receita Líquida (R$)")),
#             repasse_escritorio=limpar_decimal(dados.get("Repasse (%) Escritório")),
#             comissao_bruta_escritorio=limpar_decimal(dados.get("Comissão Bruta (R$) Escritório")),
#             repasse_assessor=limpar_decimal(dados.get("Repasse (%) Assessor Direto")),
#             comissao_assessor=limpar_decimal(dados.get("Comissão (R$) Assessor Direto")),
#         )
#         total_salvo += 1
#     return total_salvo
