import pandas as pd
from typing import Dict, List

class ProcessadorDadosSenado:
    @staticmethod
    def senadores_para_dataframe(senadores: List[Dict]) -> pd.DataFrame:
        """Converte lista de senadores para DataFrame"""
        dados_processados = []
        
        for senador in senadores:
            try:
                identificacao = senador['IdentificacaoParlamentar']
                dados_processados.append({
                    'id': identificacao['CodigoParlamentar'],
                    'nome': identificacao['NomeParlamentar'],
                    'partido': identificacao.get('SiglaPartidoParlamentar', ''),
                    'uf': identificacao.get('UfParlamentar', ''),
                    'email': identificacao.get('EmailParlamentar', ''),
                    'foto_url': identificacao.get('UrlFotoParlamentar', ''),
                    'pagina_url': identificacao.get('UrlPaginaParlamentar', '')
                })
            except KeyError as e:
                print(f"Erro ao processar senador: {e}")
                continue
        
        return pd.DataFrame(dados_processados)
    
    @staticmethod
    def materias_para_dataframe(materias: List[Dict]) -> pd.DataFrame:
        """Converte lista de matérias para DataFrame"""
        dados_processados = []
        
        for materia in materias:
            try:
                dados_processados.append({
                    'id': materia['CodigoMateria'],
                    'sigla': materia['Sigla'],
                    'numero': materia['Numero'],
                    'ano': materia['Ano'],
                    'ementa': materia.get('Ementa', ''),
                    'data_apresentacao': materia.get('DataApresentacao', ''),
                    'autor': materia.get('Autor', {}).get('NomeAutor', '')
                })
            except KeyError as e:
                print(f"Erro ao processar matéria: {e}")
                continue
        
        return pd.DataFrame(dados_processados)
    
    @staticmethod
    def tramitacoes_para_dataframe(tramitacoes: List[Dict]) -> pd.DataFrame:
        """Converte lista de tramitações para DataFrame"""
        dados_processados = []
        
        for tramitacao in tramitacoes:
            try:
                dados_processados.append({
                    'data_tramitacao': tramitacao.get('DataTramitacao', ''),
                    'descricao_situacao': tramitacao.get('DescricaoSituacao', ''),
                    'descricao_tramitacao': tramitacao.get('DescricaoTramitacao', ''),
                    'orgao': tramitacao.get('NomeOrgao', ''),
                    'sigla_orgao': tramitacao.get('SiglaOrgao', '')
                })
            except KeyError as e:
                print(f"Erro ao processar tramitação: {e}")
                continue
        
        return pd.DataFrame(dados_processados)
