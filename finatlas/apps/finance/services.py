import unicodedata
import pandas as pd
from apps.accounts.models import Assessor
from .models import LancamentoPJ1, LancamentoPJ2Previdencia


def normalizar_texto(texto):
    """Remove acentos e espaços para busca flexível de colunas."""
    if not texto:
        return ""
    clean = "".join(
        c for c in unicodedata.normalize("NFKD", str(texto)) if not unicodedata.combining(c)
    ).lower().strip()
    return "".join(c for c in clean if c.isalnum() or c.isspace())


def obter_coluna(row, col_map, *chaves_possiveis, padrao=""):
    """Retorna o valor de uma coluna testando diferentes variações de nomes."""
    for chave in chaves_possiveis:
        chave_norm = normalizar_texto(chave)
        col_real = col_map.get(chave_norm)
        if col_real is not None and col_real in row and pd.notna(row[col_real]):
            return row[col_real]
    return padrao


def limpar_decimal(valor):
    if pd.isna(valor) or valor is None or valor == "":
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)

    valor_str = str(valor).strip().replace(" ", "").replace("R$", "").replace("%", "")
    valor_str = valor_str.replace(".", "").replace(",", ".")
    try:
        return float(valor_str)
    except (ValueError, TypeError):
        return 0.0


def importar_excel_pj1(arquivo_excel, data_competencia=None):
    df = pd.read_excel(arquivo_excel)

    colunas_para_remover = [
        "Cód. Assessor Indireto I", "Repasse (%) Assessor Indireto I", "Comissão (R$) Assessor Indireto I",
        "Cód. Assessor Indireto II", "Repasse (%) Assessor Indireto II", "Comissão (R$) Assessor Indireto II",
        "Cód. Assessor Indireto III", "Repasse (%) Assessor Indireto III", "Comissão (R$) Assessor Indireto III",
    ]
    df = df.drop(columns=[col for col in colunas_para_remover if col in df.columns], errors="ignore")

    assessores_dict = {
        str(a.codigo_assessor).strip(): a
        for a in Assessor.objects.select_related("user").all()
    }

    lancamentos_para_criar = []

    for _, row in df.iterrows():
        cod_assessor = str(row.get("Cód. Assessor Direto") or row.get("Cod. Assessor Direto") or "").strip()
        if not cod_assessor or cod_assessor not in assessores_dict:
            continue

        assessor_obj = assessores_dict[cod_assessor]

        data_final = data_competencia
        if not data_final and pd.notna(row.get("Data")):
            data_final = pd.to_datetime(row.get("Data")).date()

        lancamento = LancamentoPJ1(
            assessor=assessor_obj,
            data=data_final,
            categoria=str(row.get("Categoria") or "") if pd.notna(row.get("Categoria")) else "",
            produto=str(row.get("Produto") or "N/A") if pd.notna(row.get("Produto")) else "N/A",
            nivel_1=str(row.get("Nível 1") or row.get("Nivel 1") or "") if pd.notna(row.get("Nível 1") or row.get("Nivel 1")) else "",
            nivel_2=str(row.get("Nível 2") or row.get("Nivel 2") or "") if pd.notna(row.get("Nível 2") or row.get("Nivel 2")) else "",
            nivel_3=str(row.get("Nível 3") or row.get("Nivel 3") or "") if pd.notna(row.get("Nível 3") or row.get("Nivel 3")) else "",
            cod_cliente=str(row.get("Cód. Cliente") or row.get("Cod. Cliente") or "") if pd.notna(row.get("Cód. Cliente") or row.get("Cod. Cliente")) else "",
            cod_assessor_direto=cod_assessor,
            receita=limpar_decimal(row.get("Receita (R$)")),
            receita_liquida=limpar_decimal(row.get("Receita Líquida (R$)")),
            repasse_escritorio=limpar_decimal(row.get("Repasse (%) Escritório")),
            comissao_bruta_escritorio=limpar_decimal(row.get("Comissão Bruta (R$) Escritório")),
            repasse_assessor=limpar_decimal(row.get("Repasse (%) Assessor Direto")),
            comissao_assessor=limpar_decimal(row.get("Comissão (R$) Assessor Direto")),
        )
        lancamentos_para_criar.append(lancamento)

    if lancamentos_para_criar:
        LancamentoPJ1.objects.bulk_create(lancamentos_para_criar)

    return len(lancamentos_para_criar)


def importar_excel_pj2(arquivo_excel, data_competencia=None):
    """
    Importa qualquer planilha de PJ2 (Banco XP, Mercado Internacional, XPCS, Previdência, etc.).
    """
    df = pd.read_excel(arquivo_excel)

    # Mapeia colunas normalizadas: {'codigo assessor': 'Cdigo Assessor', ...}
    col_map = {normalizar_texto(c): c for c in df.columns}

    assessores_dict = {
        str(a.codigo_assessor).strip(): a
        for a in Assessor.objects.select_related("user").all()
    }

    lancamentos_para_criar = []

    for _, row in df.iterrows():
        cod_assessor = str(obter_coluna(row, col_map, "Codigo Assessor", "Cod Assessor", "Assessor")).strip()

        if not cod_assessor or cod_assessor not in assessores_dict:
            continue

        assessor_obj = assessores_dict[cod_assessor]

        data_final = data_competencia
        data_col = obter_coluna(row, col_map, "Data")
        if not data_final and data_col:
            try:
                data_final = pd.to_datetime(data_col, dayfirst=True).date()
            except Exception:
                data_final = data_competencia

        lancamento = LancamentoPJ2Previdencia(
            assessor=assessor_obj,
            data=data_final,
            classificacao=str(obter_coluna(row, col_map, "Classificacao", "Classificacao Operacao")),
            categoria=str(obter_coluna(row, col_map, "Categoria", "Produto", padrao="PJ2 Geral")),
            nivel_1=str(obter_coluna(row, col_map, "Nivel 1")),
            nivel_2=str(obter_coluna(row, col_map, "Nivel 2")),
            nivel_3=str(obter_coluna(row, col_map, "Nivel 3")),
            nivel_4=str(obter_coluna(row, col_map, "Nivel 4")),
            codigo_cliente=str(obter_coluna(row, col_map, "Codigo Cliente", "Cod Cliente")),
            codigo_assessor=cod_assessor,
            receita_bruta=limpar_decimal(obter_coluna(row, col_map, "Receita Bruta")),
            receita_liquida=limpar_decimal(obter_coluna(row, col_map, "Receita Liquida")),
            # comissao_pct_escritorio=limpar_decimal(obter_coluna(row, col_map, "Comissao Escritorio", "Comissao pct Escritorio", "Repasse")),
            comissao_pct_escritorio=limpar_decimal(obter_coluna(row, col_map, "Comissao pct Escritorio", "Repasse")),
            comissao_escritorio=limpar_decimal(obter_coluna(row, col_map, "Comissao Escritorio")),
        )
        lancamentos_para_criar.append(lancamento)

    if lancamentos_para_criar:
        LancamentoPJ2Previdencia.objects.bulk_create(lancamentos_para_criar)

    return len(lancamentos_para_criar)
