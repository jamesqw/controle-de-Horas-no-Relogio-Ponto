import datetime

class RegistroPonto:
    def __init__(self, nome):
        self.nome = nome
        self.registros = []
    
    def registrar_entrada(self):
        agora = datetime.datetime.now()
        registro = {'tipo': 'entrada', 'hora': agora}
        self.registros.append(registro)
    
    def registrar_saida(self):
        agora = datetime.datetime.now()
        registro = {'tipo': 'saída', 'hora': agora}
        self.registros.append(registro)
    
    def imprimir_registros(self):
        for registro in self.registros:
            print(f"{registro['hora'].strftime('%d/%m/%Y %H:%M:%S')} - {registro['tipo']}")

class Funcionario:
    def __init__(self, nome):
        self.nome = nome
        self.registro_ponto = RegistroPonto(nome)
    
    def registrar_entrada(self):
        self.registro_ponto.registrar_entrada()
    
    def registrar_saida(self):
        self.registro_ponto.registrar_saida()
    
    def imprimir_registros(self):
        self.registro_ponto.imprimir_registros()

class Empresa:
    def __init__(self, cnpj, nome):
        self.cnpj = cnpj
        self.nome = nome
        self.funcionarios = []
    
    def contratar_funcionario(self, nome):
        self.funcionarios.append(Funcionario(nome))
    
    def demitir_funcionario(self, nome):
        for funcionario in self.funcionarios:
            if funcionario.nome == nome:
                self.funcionarios.remove(funcionario)
                break
    
    def registrar_entrada(self, nome_funcionario):
        for funcionario in self.funcionarios:
            if funcionario.nome == nome_funcionario:
                funcionario.registrar_entrada()
                break
    
    def registrar_saida(self, nome_funcionario):
        for funcionario in self.funcionarios:
            if funcionario.nome == nome_funcionario:
                funcionario.registrar_saida()
                break
    
    def imprimir_registros(self):
        print(f"Registros de ponto da empresa {self.nome} (CNPJ: {self.cnpj}):")
        for funcionario in self.funcionarios:
            print(f"Funcionário: {funcionario.nome}")
            funcionario.imprimir_registros()
            print()

# exemplo de uso
if __name__ == '__main__':
    empresa1 = Empresa('123456789', 'Empresa 1')
    empresa1.contratar_funcionario('João')
    empresa1.contratar_funcionario('Maria')
    empresa1.registrar_entrada('João')
    empresa1.registrar_saida('João')
    empresa1.registrar_entrada('Maria')
    empresa1.registrar_saida('Maria')
    empresa1.imprimir_registros()
    
    empresa2 = Empresa('987654321', 'Empresa 2')
    empresa2.contratar_funcionario('Pedro')
    empresa2.contratar_funcionario('Ana')
    empresa2.registrar_entrada('Pedro')
    empresa2.registrar_saida('Pedro')
    empresa2.registrar_entrada('Ana')
    empresa2.registrar_saida('Ana')
    empresa2.imprimir_registros()
