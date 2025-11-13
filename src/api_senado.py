import requests
import pandas as pd
from typing import Dict, List
from processador_dados import ProcessadorDadosSenado
import ssl
from requests.adapters import HTTPAdapter

# Adaptador customizado para forçar o TLSv1.2 (compatível com urllib3 >= 2.0)
class TLSv1_2Adapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        # Cria um contexto SSL que só permite TLSv1.2
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        # Usa o contexto SSL customizado no PoolManager
        self.poolmanager = requests.packages.urllib3.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context
        )

class APISenado:
    def __init__(self):
        self.base_url = "https://legis.senado.leg.br/dadosabertos"
        self.session = requests.Session()
        
        # Monta o adaptador para todas as requisições HTTPS
        self.session.mount('https://', TLSv1_2Adapter()) 
        
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Python-API-Senado/1.0'
        })
            
    def _fazer_requisicao(self, endpoint: str, params: Dict = {}) -> Dict:
        """Faz requisição para a API e trata erros"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            #response = self.session.get(url, params=params, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para {url}: {e}")
            return {}
    
    def buscar_senadores_atuais(self) -> List[Dict]:
        """Busca lista de todos os senadores em exercício"""
        endpoint = "senador/lista/atual"
        dados = self._fazer_requisicao(endpoint)
        
        try:
            senadores = dados['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']
            return senadores if isinstance(senadores, list) else [senadores]
        except (KeyError, TypeError):
            return []
    
    def buscar_dados_senador(self, id_senador: int) -> Dict:
        """Busca dados detalhados de um senador específico"""
        endpoint = f"senador/{id_senador}"
        dados = self._fazer_requisicao(endpoint)
        
        try:
            return dados['DetalheParlamentar']['Parlamentar']
        except (KeyError, TypeError):
            return {}
    
    def buscar_materias(self, sigla: str = "", numero: int = 0, ano: int = 0) -> List[Dict]:
        """Busca matérias legislativas com filtros"""
        endpoint = "materia/pesquisa/lista"
        params = {}
        
        if sigla:
            params['sigla'] = sigla
        if numero:
            params['numero'] = numero
        if ano:
            params['ano'] = ano
        
        dados = self._fazer_requisicao(endpoint, params)
        
        try:
            materias = dados['PesquisaBasicaMateria']['Materias']['Materia']
            return materias if isinstance(materias, list) else [materias]
        except (KeyError, TypeError):
            return []
    
    def buscar_tramitacao_materia(self, id_materia: int) -> List[Dict]:
        """Busca a tramitação de uma matéria específica"""
        endpoint = f"materia/{id_materia}/tramitacoes"
        dados = self._fazer_requisicao(endpoint)
        
        try:
            tramitacoes = dados['HistoricoTramitacao']['Tramitacoes']['Tramitacao']
            return tramitacoes if isinstance(tramitacoes, list) else [tramitacoes]
        except (KeyError, TypeError):
            return []
    
    def buscar_votacoes_senador(self, id_senador: int) -> List[Dict]:
        """Busca votações de um senador"""
        endpoint = f"senador/{id_senador}/votacoes"
        dados = self._fazer_requisicao(endpoint)
        
        try:
            votacoes = dados['VotacaoParlamentar']['Votacoes']['Votacao']
            return votacoes if isinstance(votacoes, list) else [votacoes]
        except (KeyError, TypeError):
            return []
    
    def buscar_sessoes(self, data_inicio: str = "", data_fim: str = "") -> List[Dict]:
        """Busca sessões do plenário"""
        endpoint = "plenario/lista/sessao"
        params = {}
        
        if data_inicio:
            params['dataInicio'] = data_inicio
        if data_fim:
            params['dataFim'] = data_fim
        
        dados = self._fazer_requisicao(endpoint, params)
        
        try:
            sessoes = dados['ListaSessoes']['Sessoes']['Sessao']
            return sessoes if isinstance(sessoes, list) else [sessoes]
        except (KeyError, TypeError):
            return []


## Código 2
    
## Código 3
def main():
    # Inicializar a conexão
    api = APISenado()
    
    print("🔍 Conectando à API do Senado...")
    
    # 1. Buscar todos os senadores atuais
    print("\n📊 Buscando senadores em exercício...")
    senadores = api.buscar_senadores_atuais()
    
    if senadores:
        df_senadores = ProcessadorDadosSenado.senadores_para_dataframe(senadores)
        print(f"✅ Encontrados {len(df_senadores)} senadores")
        print(df_senadores[['nome', 'partido', 'uf']].head())
        
        # Salvar em CSV
        df_senadores.to_csv('senadores_atuais.csv', index=False)
        print("💾 Dados salvos em 'senadores_atuais.csv'")
    
    # 2. Buscar matérias específicas
    print("\n📋 Buscando matérias legislativas...")
    materias = api.buscar_materias(sigla='PL', ano=2024)
    
    if materias:
        df_materias = ProcessadorDadosSenado.materias_para_dataframe(materias)
        print(f"✅ Encontradas {len(df_materias)} matérias")
        print(df_materias[['sigla', 'numero', 'ano', 'ementa']].head())
        
        # Salvar em CSV
        df_materias.to_csv('materias_legislativas.csv', index=False)
        print("💾 Dados salvos em 'materias_legislativas.csv'")
    
    # 3. Buscar tramitação de uma matéria específica (exemplo)
    if materias:
        primeira_materia_id = materias[0]['CodigoMateria']
        print(f"\n🔄 Buscando tramitação da matéria ID {primeira_materia_id}...")
        
        tramitacoes = api.buscar_tramitacao_materia(primeira_materia_id)
        
        if tramitacoes:
            df_tramitacoes = ProcessadorDadosSenado.tramitacoes_para_dataframe(tramitacoes)
            print(f"✅ Encontradas {len(df_tramitacoes)} tramitações")
            print(df_tramitacoes.head())
    
    # 4. Buscar dados de um senador específico
    if senadores:
        primeiro_senador_id = senadores[0]['IdentificacaoParlamentar']['CodigoParlamentar']
        print(f"\n👤 Buscando dados detalhados do senador ID {primeiro_senador_id}...")
        
        senador_detalhes = api.buscar_dados_senador(primeiro_senador_id)
        if senador_detalhes:
            print(f"✅ Dados do senador: {senador_detalhes.get('IdentificacaoParlamentar', {}).get('NomeParlamentar', '')}")

if __name__ == "__main__":
    main()

## Código 4
def analise_avancada():
    """Exemplo de análise mais avançada dos dados"""
    api = APISenado()
    
    # Buscar senadores e fazer análise
    senadores = api.buscar_senadores_atuais()
    df_senadores = ProcessadorDadosSenado.senadores_para_dataframe(senadores)
    
    # Análise por partido
    if not df_senadores.empty:
        analise_partidos = df_senadores.groupby('partido').size().sort_values(ascending=False)
        print("\n🏛️ Distribuição por partido:")
        print(analise_partidos)
        
        # Análise por UF
        analise_uf = df_senadores.groupby('uf').size().sort_values(ascending=False)
        print("\n🗺️ Distribuição por UF:")
        print(analise_uf)

# Executar análise
analise_avancada()

## Código 5
