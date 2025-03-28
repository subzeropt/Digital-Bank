#!/usr/bin/python3
import json
from datetime import datetime
class Cliente:
    def __init__(self,nome,numero, nif, email,telemovel):
        self._numero = numero
        self._nome = nome
        self._nif = nif
        self._email = email
        self._telemovel= telemovel
        self.contas = []
    
    def criar_conta(self, conta):
        self.contas.append(conta)

    @property
    def numero(self):
        return self._numero
        
    @numero.setter
    def numero(self, novo_numero):
      self._numero = novo_numero
      
    @property
    def nome(self):
        return self._nome
       
    @nome.setter
    def nome(self,novo_nome):
       self._nome = novo_nome
        
    @property
    def nif(self):
        return self._nif
     
    @nif.setter
    def nif(self, novo_nif):
        if len(novo_nif)==9:
            self._nif = novo_nif
        else:
            print("Nif inválido!")
            
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, novo_email):
        if '@' in novo_email:
            self._email = novo_email
        else:
            print("Email inválido!")
            
    def __str__(self):
        return f"Cliente: {self.nome}, NIF: {self.nif}, Email: {self.email}, Telemóvel: {self.telemovel}"
    
        
# Subclasse para ClienteParticular
class ClienteParticular(Cliente):
    def __init__(self, nome, numero, nif, email, telemovel, tipo_documento="cc",profissao=""): #cc=cartão de cidadão
        super().__init__(nome, numero, nif, email, telemovel)
        self._tipo_documento = tipo_documento  # Documento específico da pessoa física (Cartão de Cidadão ou outro)
        self._profissao=profissao
    
    def __str__(self):
        return f"Cliente Pessoa Física: {self.nome}, NIF: {self.nif}, Tipo Documento: {self.tipo_documento}, Email: {self.email}"



# Subclasse para ClienteEmpresa
class ClienteEmpresa(Cliente):
    def __init__(self, nome, numero, nif, email, telemovel, tipo_documento="crc",representantes=[],tipo_atividade=""): #crc=Certificado de Registo Comercial
        super().__init__(nome, numero, nif, email, telemovel)
        self._tipo_documento = tipo_documento  # Documento específico da pessoa jurídica (Certificado de Registo Comercial ou outro)
        self._representantes = representantes  # Lista de representantes legais da empresa
        self._tipo_atividade = tipo_atividade
        
    def adicionar_representante(self, representante):
        self._representantes.append(representante)
        
    def __str__(self):
        return f"Cliente Pessoa Jurídica: {self.nome}, NIF: {self.nif}, Tipo Documento: {self.tipo_documento}, Email: {self.email}"	


class Conta:
    def __init__(self, numero, tipo, saldo=0.0, cliente=None,estado="Ativo"):
        self._numero = numero
        self._tipo = tipo
        self._saldo = saldo
        self._cliente = cliente
        self._estado = estado

        if cliente:
            cliente.criar_conta(self)  # Associar a conta ao cliente
    

    def __add__(self, outra_conta):
        if isinstance(outra_conta, Conta):
            return self.saldo + outra_conta.saldo
        return NotImplemented
		
    def __eq__(self, outra_conta):
        if isinstance(outra_conta, Conta):
            return self.numero == outra_conta.numero
        return False
		
    def __gt__(self, outra_conta):
        if isinstance(outra_conta, Conta):
            return self.saldo > outra_conta.saldo
        return NotImplemented
    

    @property
    def cliente(self):
        return self._cliente
       
    @cliente.setter
    def cliente(self,novo_cliente):
       self._cliente = novo_cliente
       
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self,novo_numero):
       self._numero = novo_numero
      
    @property
    def tipo(self):
        return self._tipo
       
    @tipo.setter
    def tipo(self,novo_tipo):
       self._tipo = novo_tipo    
       
    @property
    def estado(self):
        return self._estado
       
    @estado.setter
    def estado(self,novo_estado):
       self._estado = novo_estado
       
    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, novo_valor):
        # Garantir que o saldo não seja negativo
        if novo_valor >= 0:
            self._saldo = novo_valor
        else:
            print("Não é possível definir um saldo negativo!")


    def deposito(self, valor):
        if valor > 0:
            print(f"Depósito efetuado com sucesso.")
            return True
        else:
            print("Valor inválido para depósito.")
            return False

    def levantamento(self, valor):
        if valor > 0 and self.saldo >= valor:
            self._saldo -= valor #validação efetuada no setter "saldo"
            print(f"Levantamento efetuado com sucesso.")
            return True
        else:
            print("Saldo insuficiente.")
            return False

    # # Resposta 1c
    def calcular_taxa_manutencao(self):
        """Método padrão, pode ser sobrescrito em subclasses"""
        return 0  # Contas normais não possuem taxa de manutenção



    def __str__(self):
        return f"Conta: {self.numero}, Tipo: {self.tipo}, Saldo: {self.saldo}"


class ContaPoupanca(Conta):
    def __init__(self, numero, saldo=0.0, cliente=None, taxa_juros=0.02, imposto=0.01,moeda="EUR"):
        super().__init__(numero, "Poupança", saldo, cliente,moeda)#codigoMoeda
        self.taxa_juros = taxa_juros
        self.imposto = imposto
    
    def aplicar_imposto(self):
        imposto = self.saldo * self.imposto
        self.saldo -= imposto
        print(f"Imposto de {imposto} aplicado. Novo saldo: {self.saldo}")

    # Resposta 1c)
    def calcular_taxa_manutencao(self):
        """Conta Poupança não tem taxa de manutenção, mas pode ter taxa sobre juros"""
        return self.saldo * 0.001  # 0.1% do saldo como taxa de manutenção

    def __str__(self):
        return f"Conta Poupança: {self.numero}, Saldo: {self.saldo}, Taxa de Juros: {self.taxa_juros}, Imposto: {self.imposto}"


class ContaCorrente(Conta):
    def __init__(self, numero, saldo=0.0, cliente=None, limite=1000):
        super().__init__(numero, "Corrente", saldo, cliente)
        self.limite = limite


     # Resposta 1a)
     # So faz levantamentos e depositos acima de 100eur
    def levantamento(self, valor):

        if valor > 100 :
          return super().levantamento(valor) 
    
    def deposito(self, valor):

         if valor > 100 :
          return super().deposito(valor)

    # Resposta 1c)
    def calcular_taxa_manutencao(self):
        """Conta Corrente tem uma taxa de manutenção fixa"""
        return 5.0  # Por exemplo, 5€ de taxa mensal
         
    def __str__(self):
        return f"Conta Corrente: {self.numero}, Saldo: {self.saldo}, Limite: {self.limite}"
        

class ClienteVIP(ClienteParticular,ContaCorrente):
    def __init__(self,nome,numero_cliente, nif, email,telemovel,numero_conta,saldo,limite=100000):
        ClienteParticular.__init__(self,nome,numero_cliente, nif, email,telemovel)
        ContaCorrente.__init__(self,numero_conta,saldo,self,limite)


class Transacao:
   def __init__(self, tipo, valor, conta_origem, conta_destino=None):
        self.tipo = tipo
        self.valor = valor
        self.data = datetime.now()
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
   
   def __str__(self):
        if self.conta_destino:
            return f"{self.tipo} de {self.valor} na conta {self.conta_origem.numero} para {self.conta_destino.numero} em {self.data}"
        return f"{self.tipo} de {self.valor} na conta {self.conta_origem.numero} em {self.data}"		
		
		
class Banco:
    clientes = []
    movimentos = []
        
    def __init__(self, nome,nif,swiftcode):
        self._nome = nome
        self._nif = nif
        self._swiftcode = swiftcode
      
    @property
    def nome(self):
        return self._nome
       
    @nome.setter
    def nome(self,novo_nome):
       self._nome = novo_nome
       
       
    @property
    def nif(self):
        return self._nif
       
    @nif.setter
    def nif(self,novo_nif):
       self._nif = novo_nif
       
    @property
    def swiftcode(self):
        return self._swiftcode
       
    @swiftcode.setter
    def swiftcode(self,novo_swift):
       self._swiftcode = novo_swift
       
    def criar_cliente(self, cliente):
        self.clientes.append(cliente)
		
        print(f"Cliente {cliente.nome} criado com sucesso.")

    def encontrar_conta(self, numero_conta):
        for conta in self.contas:
            if conta.numero == numero_conta:
                return conta
        return None

    def deposito(self,conta,valor):
        value=conta.deposito(valor)
        if value==True:
          self.movimentos.append(Transacao("Depósito",valor,conta.numero,None))

    def levantamento(self,conta,valor):
        value=conta.levantamento(valor)
        if value==True:
          self.movimentos.append(Transacao("Levantamento",valor,conta.numero,None))


    def transferencia(self, conta_origem=None, conta_destino=None, valor=100):
        print(f"Transferências múltiplas....")
        if isinstance(valor, list) and isinstance(conta_destino, list):
            if len(valor) != len(conta_destino):
                print("Número de valores e contas de destino não coincidem.")
                return
            for v, c in zip(valor, conta_destino):
                value = conta_origem.levantamento(v)
                if value:
                    c.deposito(v)
            print(f"Transferências múltiplas realizadas com sucesso.")
        elif isinstance(valor, (int, float)) and isinstance(conta_destino, Conta):
            value = conta_origem.levantamento(valor)
            if value:
                conta_destino.deposito(valor)
            print(f"Transferência efetuada com sucesso.")
        else:
            print("Parâmetros inválidos.")
            
    def listar_clientes(self):
        for cliente in self.clientes:
            print(".Numero",cliente.numero,".Nome",cliente.nome," nif:",cliente.nif," email:",cliente.email)

    def listar_contas(self):
        for ficha_cliente in self.clientes:
          #print('.Numero conta:',conta_cliente.contas[0].numero)    
          for conta_cliente in ficha_cliente.contas:
            print('.Numero conta:',conta_cliente.numero,' .saldo:',conta_cliente.saldo)
        
    def listar_movimentos(self):
        for mov in self.movimentos:
            print("Tipo:",mov.tipo," Conta Origem:",mov.conta_origem," Valor:",mov.valor)	
		
####################### Fim das classes    #######################



# Resposta 2 a)
import pandas as pd
import matplotlib.pyplot as plt

def grafico_distribuicao_saldo(banco):
    # Criar lista de dicionários com as contas
    dados_contas = []
    for cliente in banco.clientes:
        for conta in cliente.contas:
            conta_dict = {
                "Cliente": cliente.nome,
                "Tipo Conta": conta.tipo,
                "Saldo": conta.saldo
            }
            dados_contas.append(conta_dict)
    
    # Criar DataFrame("Pandas")
    df_contas = pd.DataFrame(dados_contas)
    
    # Plotar a distribuição dos saldos
    plt.figure(figsize=(10, 6))
    plt.hist(df_contas["Saldo"], bins=20, edgecolor='black')
    plt.title("Distribuição de Saldo das Contas")
    plt.xlabel("Saldo")
    plt.ylabel("Número de Contas")
    plt.show()



#+++++++++++++++++++++++++++ Inicio das funções +++++++++++++++++++++++++
def carregar_dados(banco, ficheiro_dados="/home/osboxes/code/Python/BancoDigital/dados_banco.json"):
#def carregar_dados(banco, ficheiro_dados="dados_banco.json"):
    try:
        with open(ficheiro_dados, "r") as f:
            # Verifica se o arquivo não está vazio
            conteudo = f.read().strip()
            if not conteudo:
                print("Ficheiro sem dados.")
                return
            # Volta para o início do arquivo
            f.seek(0)
            dados = json.load(f)
            
        for cliente_dict in dados.get("clientes", []):
            if cliente_dict["tipo"] == "Particular":
                cliente = ClienteParticular(
                    cliente_dict["nome"], cliente_dict["numero"],
                    cliente_dict["nif"], cliente_dict["email"],
                    cliente_dict["telemovel"], profissao=cliente_dict.get("profissao", "")
                )
            else:
                cliente = ClienteEmpresa(
                    cliente_dict["nome"], cliente_dict["numero"],
                    cliente_dict["nif"], cliente_dict["email"],
                    cliente_dict["telemovel"],
                    representantes=cliente_dict.get("representantes", []),
                    tipo_atividade=cliente_dict.get("tipo_atividade", "")
                )
            
            for conta_dict in cliente_dict.get("contas", []):
                if conta_dict["tipo"] == "Poupança":
                    conta = ContaPoupanca(
                        conta_dict["numero"], conta_dict["saldo"], cliente
                    )
                else:
                    conta = ContaCorrente(
                        conta_dict["numero"], conta_dict["saldo"], cliente
                    )
                conta.estado = conta_dict.get("estado", "Ativo")
                cliente.criar_conta(conta)
            
            banco.criar_cliente(cliente)
        
        for mov_dict in dados.get("movimentos", []):
            movimento = Transacao(
                mov_dict["tipo"], mov_dict["valor"], 
                mov_dict["conta_origem"], mov_dict.get("conta_destino")
            )
            movimento.data = datetime.strptime(mov_dict["data"], "%Y-%m-%d %H:%M:%S")
            banco.movimentos.append(movimento)
    
    except FileNotFoundError:
        print("Não foi encontrado nenhum ficheiro com dados: o sistema começa sem dados")
    except json.JSONDecodeError:
        print("Erro ao carregar o arquivo JSON. O ficheiro pode estar corrompido ou sem dados.")



def gravar_dados(banco, ficheiro_dados="/home/osboxes/code/Python/BancoDigital/dados_banco.json"):
#def gravar_dados(banco, ficheiro_dados="dados_banco.json"):
    dados = {
        "clientes": [],
        "movimentos": []
    }
    
    for cliente in banco.clientes:
        cliente_dict = {
            "numero": cliente.numero,
            "nome": cliente.nome,
            "nif": cliente.nif,
            "email": cliente.email,
            "telemovel": cliente._telemovel,
            "tipo": "Particular" if isinstance(cliente, ClienteParticular) else "Empresa",
            "contas": [
                {
                    "numero": conta.numero,
                    "tipo": conta.tipo,
                    "saldo": conta.saldo,
                    "estado": conta.estado,
                    "moeda": conta.moeda #codigoMoeda
                } for conta in cliente.contas
            ]
        }
        if isinstance(cliente, ClienteParticular):
            cliente_dict["profissao"] = cliente._profissao
        elif isinstance(cliente, ClienteEmpresa):
            cliente_dict["representantes"] = cliente._representantes
            cliente_dict["tipo_atividade"] = cliente._tipo_atividade
        
        dados["clientes"].append(cliente_dict)
    
    for mov in banco.movimentos:
        dados["movimentos"].append({
            "tipo": mov.tipo,
            "valor": mov.valor,
            "data": mov.data.strftime("%Y-%m-%d %H:%M:%S"),
            "conta_origem": mov.conta_origem,
            "conta_destino": mov.conta_destino
        })
    
    if dados["clientes"] or dados["movimentos"]: 
      with open(ficheiro_dados, "w") as f: 
        json.dump(dados, f, indent=4) 
    else: 
        print("Sem dados para gravar.")
        
        
def criar_cliente(banco):
    linha = "+" + "-" * 38 + "+"
    print(linha)
    print("|{:^38}|".format("Escolher o tipo de cliente a criar:"))
    print(linha)
    print("|{:^38}|".format("1. Cliente Particular"))
    print("|{:^38}|".format("2. Cliente Empresa"))
    #codigoVIP
    print("|{:^38}|".format("3. Cliente VIP"))
    print("|{:^38}|".format("4. Voltar ao menu anterior"))
    print(linha)
    opcao = input("Opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        numero = input("Número do cliente: ")
        nif = input("NIF: ")
        email = input("Email: ")
        telemovel = input("Telemóvel: ")
        profissao = input("Profissão: ")
        tipo_documento="cc"
        #(self, nome, numero, nif, email, telemovel, tipo_documento="cc",profissao="")
        cliente = ClienteParticular(nome, numero, nif, email, telemovel,tipo_documento,profissao)
        banco.criar_cliente(cliente)
        print(f"Cliente {nome} criado com sucesso.")
    elif opcao == "2":
        representantes=[]
        
        numero = input("Número do cliente: ")
        nome = input("Nome da empresa: ")
        nif = input("NIF: ")
        email = input("Email: ")
        telemovel = input("Telemóvel: ")
        tipo_atividade = input("Atividade: ")
        nome_representante = input("Nome representante: ")
        representantes.append(nome_representante)
        tipo_documento="crc"
        cliente = ClienteEmpresa(nome, numero, nif, email, telemovel,tipo_documento,representantes,tipo_atividade)
        banco.criar_cliente(cliente)
        print(f"Cliente {nome} criado com sucesso.")
    #codigoVIP 
    elif opcao == "3":
        nome = input("Nome: ")
        numero = input("Número do cliente: ")
        nif = input("NIF: ")
        email = input("Email: ")
        telemovel = input("Telemóvel: ")
        profissao = input("Profissão: ")
        tipo_documento="cc"
        numero_conta = input("Numero conta: ")
        saldo = input("Saldo inicial: ")
        cliente = ClienteParticular(nome, numero, nif, email, telemovel,tipo_documento,profissao)
        cliente_vip=ClienteVIP(nome=nome,
                               numero_cliente=numero,
                               nif=nif,
                               email=email,
                               telemovel=telemovel,
                               numero_conta=numero_conta,
                               saldo=saldo
                               )
  
        banco.criar_cliente(cliente_vip)
        print(f"Cliente {nome} criado com sucesso.")   
    elif opcao == "4":
        return
    else:
        print("Opção inválida!")


def criar_conta(banco):
    numero_cliente = input("Número do cliente para criar a conta: ")
    cliente = None
    for c in banco.clientes:
        if c.numero == numero_cliente:
            cliente = c
            break

    if cliente is None:
        print("Cliente não encontrado!")
        return

    linha = "+" + "-" * 28 + "+"
    print(linha)
    print("|{:^28}|".format("Escolha o tipo de conta:"))
    print(linha)
    print("|{:^28}|".format("1 - Conta Corrente"))
    print("|{:^28}|".format("2 - Conta Poupança"))
    print("|{:^28}|".format("3 - Voltar ao menu anterior"))
    print(linha)
    opcao = input("Opção: ")

    if opcao == "1":
        numero = input("Número da conta: ")
        saldo = float(input("Saldo inicial: "))
        moeda = input("Moeda: ").upper()#codigoMoeda
        conta = ContaCorrente(numero=numero, saldo=saldo, cliente=cliente,moeda=moeda)
        #cliente.criar_conta(conta)
        print(f"Conta Corrente {numero} criada com sucesso para o cliente {cliente.nome}.")
    elif opcao == "2":
        numero = input("Número da conta: ")
        saldo = float(input("Saldo inicial: "))
        moeda = input("Moeda: ").upper()#codigoMoeda
        conta = ContaPoupanca(numero=numero, saldo=saldo, cliente=cliente)
        print(f"Conta Poupança {numero} criada com sucesso para o cliente {cliente.nome}.")
    elif opcao == "3":
        return
    else:
        print("Opção inválida!")      

def efetuar_transferencia(banco):
    linha = "+" + "-" * 38 + "+"
    print(linha)
    print("|{:^38}|".format("Escolha o tipo de conta:"))
    print(linha)
    print("|{:^38}|".format("1 - Transferência única"))
    print("|{:^38}|".format("2 - Transferência múltipla"))
    print(linha)
    opcao = input("Opção: ")
    
    if opcao == "1":
        numero_conta_origem = input("Número da conta origem: ")
        numero_conta_destino = input("Número da conta destino: ")
        valor = float(input("Montante: "))
        
        conta_origem = None
        conta_destino = None
        for cliente in banco.clientes:
            for c in cliente.contas:
                if c.numero == numero_conta_origem:
                    conta_origem = c
                if c.numero == numero_conta_destino:
                    conta_destino = c

        if conta_origem and conta_destino:
            banco.transferencia(conta_origem, conta_destino, valor)
        else:
            print("Conta(s) não encontrada(s)!")
    
    elif opcao == "2":
        numero_conta_origem = input("Número da conta origem: ")
        conta_origem = None
        for cliente in banco.clientes:
            for c in cliente.contas:
                if c.numero == numero_conta_origem:
                    conta_origem = c
                    break

        if not conta_origem:
            print("Conta de origem não encontrada!")
            return

        destinos = []
        valores = []

        while True:
            numero_conta_destino = input("Número da conta destino (ou 'fim' para terminar): ")
            if numero_conta_destino.lower() == "fim":
                break
            valor = float(input(f"Montante para a conta {numero_conta_destino}: "))
            
            conta_destino = None
            for cliente in banco.clientes:
                for c in cliente.contas:
                    if c.numero == numero_conta_destino:
                        conta_destino = c
                        break

            if conta_destino:
                destinos.append(conta_destino)
                valores.append(valor)
            else:
                print(f"Conta destino {numero_conta_destino} não encontrada.")

        if destinos and valores:
            banco.transferencia(conta_origem, destinos, valores)
        else:
            print("Nenhuma transferência foi realizada. Verifique as informações fornecidas.")
    elif opcao == "3":
      return
    else:
        print("Opção inválida!")
        
        
def efetuar_levantamento(banco):
    numero_conta = input("-número da conta para levantamento: ")
    valor = float(input("Montante: "))
    conta = None
    for cliente in banco.clientes:
        for c in cliente.contas:
            if c.numero == numero_conta:
                conta = c
                break
    if conta:
        conta.levantamento(valor)
        banco.movimentos.append(Transacao("Levantamento", valor, conta))
    else:
        print("Conta não encontrada!")  


def efetuar_deposito(banco):
    numero_conta = input("Número da conta para depósito: ")
    valor = float(input("Montante: "))
    conta = None
    for cliente in banco.clientes:
        for c in cliente.contas:
            if c.numero == numero_conta:
                conta = c
                break
    if conta:
        conta.deposito(valor)
        banco.movimentos.append(Transacao("Depósito", valor, conta))
    else:
        print("Conta não encontrada!")        
#+++++++++++++++++++++++++++ Fim das funções    +++++++++++++++++++++++++



if __name__ == "__main__":
    
  banco = Banco("Super Banco M++","505789123","SBMMPTPL")
  
  carregar_dados(banco)
  grafico_distribuicao_saldo(banco)
  


  try:
    while True:
      linha = "+" + "-" * 28 + "+"
      print(linha)
      print("|{:^28}|".format("Menu principal"))
      print(linha)
      print("|{:^28}|".format("1 - Criar Cliente"))
      print("|{:^28}|".format("2 - Criar Conta"))
      print("|{:^28}|".format("3 - Depósito"))
      print("|{:^28}|".format("4 - Levantamento"))
      print("|{:^28}|".format("5 - Transferências"))
      print("|{:^28}|".format("6 - Listar Clientes"))
      print("|{:^28}|".format("7 - Listar Contas"))
      print("|{:^28}|".format("8 - Listar Movimentos"))
      print("|{:^28}|".format("9 - Sair"))
      print(linha)
      opcao = input("Opção: ")
        
      if opcao == "1":
        criar_cliente(banco)
        gravar_dados(banco)
      elif opcao == "2":
        criar_conta(banco)
        gravar_dados(banco)
      elif opcao == "3":
        efetuar_deposito(banco)
        gravar_dados(banco)
      elif opcao == "4":
        efetuar_levantamento(banco)
        gravar_dados(banco)
      elif opcao == "5":
        efetuar_transferencia(banco)
        gravar_dados(banco)
      elif opcao == "6":
        banco.listar_clientes()
      elif opcao == "7":
        banco.listar_contas()
      elif opcao == "8":
        banco.listar_movimentos()
      elif opcao == "9":
        print("Programa a terminar ...")
        break
      else:
        print("Opção inválida!") 
  finally:
    gravar_dados(banco)
    print("Fim de programa")  
        