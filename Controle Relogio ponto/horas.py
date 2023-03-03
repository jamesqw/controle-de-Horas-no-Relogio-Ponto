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
    def __init__(self, nome, cracha, salario_hora, valor_hora_extra):
        self.nome = nome
        self.cracha = cracha
        self.registro_ponto = RegistroPonto(nome)
        self.salario_hora = salario_hora
        self.valor_hora_extra = valor_hora_extra
        self.horas_mes = 0
        self.horas_trabalhadas_mes = 0
        self.descontos = 0
    
    def registrar_entrada(self):
        self.registro_ponto.registrar_entrada()
    
    def registrar_saida(self):
        self.registro_ponto.registrar_saida()
    
    def listar_registros_ponto(self):
        registros = self.registro_ponto.listar_registros()
        horas_trabalhadas = 0
        valor_horas_trabalhadas = 0
        valor_horas_extra = 0
        for i in range(0, len(registros)-1, 2):
            entrada = registros[i]['hora']
            saida = registros[i+1]['hora']
            tempo_trabalhado = datetime.datetime.strptime(saida, '%d/%m/%Y %H:%M:%S') - datetime.datetime.strptime(entrada, '%d/%m/%Y %H:%M:%S')
            horas_trabalhadas += tempo_trabalhado.total_seconds() / 3600
            if horas_trabalhadas <= self.horas_mes:
                valor_horas_trabalhadas += self.salario_hora * (tempo_trabalhado.total_seconds() / 3600)
            else:
                horas_extras = horas_trabalhadas - self.horas_mes
                valor_horas_trabalhadas += self.salario_hora * (self.horas_mes)
                valor_horas_extra += self.valor_hora_extra * (horas_extras)
        self.horas_trabalhadas_mes += horas_trabalhadas
        salario_bruto = valor_horas_trabalhadas + valor_horas_extra
        salario_liquido = salario_bruto - self.descontos
        return {'registros': registros, 'horas_trabalhadas': horas_trabalhadas, 'salario_bruto': salario_bruto, 'salario_liquido': salario_liquido}