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
    
    def listar_registros(self):
        registros_formatados = []
        for registro in self.registros:
            registro_formatado = {'hora': registro['hora'].strftime('%d/%m/%Y %H:%M:%S'), 'tipo': registro['tipo']}
            registros_formatados.append(registro_formatado)
        return registros_formatados

class Funcionario:
    def __init__(self, nome, cracha):
        self.nome = nome
        self.cracha = cracha
        self.registro_ponto = RegistroPonto(nome)
        self.horas_acumuladas = 0
    
    def registrar_entrada(self):
        self.registro_ponto.registrar_entrada()
    
    def registrar_saida(self):
        self.registro_ponto.registrar_saida()
    
    def listar_registros_ponto(self):
        registros = self.registro_ponto.listar_registros()
        horas_trabalhadas = 0
        for i in range(0, len(registros)-1, 2):
            entrada = registros[i]['hora']
            saida = registros[i+1]['hora']
            tempo_trabalhado = datetime.datetime.strptime(saida, '%d/%m/%Y %H:%M:%S') - datetime.datetime.strptime(entrada, '%d/%m/%Y %H:%M:%S')
            horas_trabalhadas += tempo_trabalhado.total_seconds() / 3600
        self.horas_acumuladas += horas_trabalhadas
        return {'registros': registros, 'horas_trabalhadas': horas_trabalhadas, 'horas_acumuladas': self.horas_acumuladas}

class Empresa:
    def __init__(self, cnpj, nome):
        self.cnpj = cnpj
        self.nome = nome
        self.funcionarios = []
    
    def contratar_funcionario(self, nome, cracha):
        self.funcionarios.append(Funcionario(nome, cracha))
    
    def demitir_funcionario(self, nome):
        for funcionario in self.funcionarios:
            if funcionario.nome == nome:
                self.funcionarios.remove(funcionario)
                break
    
    def registrar_entrada_por_cracha(self, cracha):
        for funcionario in self.funcionarios:
            if funcionario.cracha == cracha:
                funcionario.registrar_entrada()
                break
    
    def registrar_saida_por_cracha(self, cracha):
        for funcionario in self.funcionarios:
            if funcionario.cracha == cracha:
                funcionario.registrar_saida()
                break
    
    def listar_registros_ponto_por_funcionario(self, nome_funcionario):
        for funcionario in self.funcionarios:
            if funcionario.nome == nome_funcionario:
                return funcionario.listar
