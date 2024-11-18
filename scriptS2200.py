import os
import xml.etree.ElementTree as ET


# Função para adicionar o namespace ao caminho do elemento
def ns(tag, namespace):
    return f"{{{namespace}}}{tag}"


# Função para buscar informações no XML
def buscar_informacoes_por_cpf(caminho_arquivo, cpf, namespace_evt, namespace_retorno):
    try:
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()

        # Procurar o CPF no XML
        trabalhador = root.find(
            f".//{ns('trabalhador', namespace_evt)}/{ns('cpfTrab', namespace_evt)}"
        )

        if trabalhador is not None and trabalhador.text == cpf:
            # Encontrar o ID do evento
            id_evento_novo_element = root.find(f".//{ns('evtAdmissao', namespace_evt)}")
            id_evento_novo = (
                id_evento_novo_element.attrib.get("Id")
                if id_evento_novo_element is not None
                else None
            )

            # Procurar o nrRecibo dentro da tag <retornoEvento> > <recibo> > <nrRecibo>
            nr_recibo = root.find(
                f".//{ns('retornoEvento', namespace_retorno)}/{ns('recibo', namespace_retorno)}/{ns('nrRecibo', namespace_retorno)}"
            )

            # Verificar se o número do recibo foi encontrado
            nr_recibo_text = (
                nr_recibo.text if nr_recibo is not None else "NR_RECIBO_NAO_ENCONTRADO"
            )

            return id_evento_novo, nr_recibo_text, trabalhador.text

        return None

    except ET.ParseError as e:
        print(f"Erro ao parsear o arquivo XML: {caminho_arquivo}, erro: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao processar {caminho_arquivo}: {e}")
        return None


# Função principal para processar a lista de IDs e CPFs
def processar_lista_cpfs(
    lista_ids_cpfs, caminho_pasta_xml, namespace_evt, namespace_retorno
):
    resultados = []

    # Percorrer cada ID antigo e CPF da lista
    for id_antigo, cpf in lista_ids_cpfs:
        for arquivo in os.listdir(caminho_pasta_xml):
            if arquivo.endswith(".xml"):
                caminho_completo = os.path.join(caminho_pasta_xml, arquivo)

                informacoes = buscar_informacoes_por_cpf(
                    caminho_completo, cpf, namespace_evt, namespace_retorno
                )

                # Se encontrar as informações, armazenar no resultado
                if informacoes is not None:
                    id_evento_novo, nr_recibo, cpf_encontrado = informacoes
                    resultados.append(
                        (id_evento_novo, nr_recibo, cpf_encontrado, id_antigo)
                    )
                    break  # Sai do loop se as informações foram encontradas

    return resultados


# Funções para salvar os resultados em um arquivo TXT
def salvar_resultados_em_txt(resultados, caminho_arquivo_txt):
    with open(caminho_arquivo_txt, "w") as f:
        for resultado in resultados:
            f.write(
                f"update esocial.s2200 set idevento='{resultado[0]}', situacao='1' where cpftrab='{resultado[2]}' and idevento='{resultado[3]}';\n\n"
            )
            f.write(
                f"update esocial.historico set idevento='{resultado[0]}', nr_recibo='{resultado[1]}', message='201 - Lote processado com sucesso', status='P' where idevento='{resultado[3]}';\n\n"
            )


# Namespaces do XML
namespace_evt = "http://www.esocial.gov.br/schema/evt/evtAdmissao/v_S_01_01_00"
namespace_retorno = "http://www.esocial.gov.br/schema/evt/retornoEvento/v1_2_1"

# Lista de IDs antigos e CPFs fornecida
lista_ids_cpfs = [
    ("IDEVENTO", "CPF"),
]

# Caminho para a pasta contendo os arquivos XML
caminho_pasta_xml = "C:/Users/itarg/Downloads/S2200final"

# Processar a lista e obter os resultados
resultados = processar_lista_cpfs(
    lista_ids_cpfs, caminho_pasta_xml, namespace_evt, namespace_retorno
)

# Caminho para salvar o arquivo TXT com os resultados
caminho_arquivo_txt = "C:/Users/itarg/Downloads/resultados.txt"

# Salvar os resultados em um arquivo TXT
salvar_resultados_em_txt(resultados, caminho_arquivo_txt)
