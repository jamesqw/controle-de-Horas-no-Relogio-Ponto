import sqlite3
import datetime
import time

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
    

class BancoDados:
    def __init__(self, nome_banco):
        self.nome_banco = nome_banco
        self.conexao = sqlite3.connect(nome_banco)
        self.criar_tabela()
    
    def criar_tabela(self):
        cursor = self.conexao.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cracha TEXT, cnpj TEXT, entrada TIME, saida TIME, almoco_inicio TIME, almoco_fim TIME, horas_acumuladas INTEGER, ganhos FLOAT, descontos FLOAT)''')
        self.conexao.commit()
        
    def inserir_funcionario(self, nome, cracha, cnpj):
        entrada = time(0, 0)
        saida = time(0, 0)
        almoco_inicio = time(0, 0)
        almoco_fim = time(0, 0)
        horas_acumuladas = 0
        ganhos = 0.0
        descontos = 0.0
        
        self.cursor.execute('''INSERT INTO funcionarios (nome, cracha, cnpj, entrada, saida, almoco_inicio, almoco_fim, horas_acumuladas, ganhos, descontos) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (nome, cracha, cnpj, entrada, saida, almoco_inicio, almoco_fim, horas_acumuladas, ganhos, descontos))
        self.conexao.commit()
        print("Funcionário inserido com sucesso.")
        
    def listar_funcionarios(self):
        self.cursor.execute("SELECT * FROM funcionarios")
        funcionarios = self.cursor.fetchall()
        for funcionario in funcionarios:
            print(f"ID: {funcionario[0]}")
            print(f"Nome: {funcionario[1]}")
            print(f"Crachá: {funcionario[2]}")
            print(f"CNPJ: {funcionario[3]}")
            print(f"Entrada: {funcionario[4]}")
            print(f"Saída: {funcionario[5]}")
            print(f"Almoço início: {funcionario[6]}")
            print(f"Almoço fim: {funcionario[7]}")
            print(f"Horas acumuladas: {funcionario[8]}")
            print(f"Ganhos: {funcionario[9]}")
            print(f"Descontos: {funcionario[10]}")
            print("-" * 50)
        
    def buscar_funcionario_nome(self, nome):
        self.cursor.execute(f"SELECT * FROM funcionarios WHERE nome LIKE '%{nome}%'")
        funcionarios = self.cursor.fetchall()
        for funcionario in funcionarios:
            print(f"ID: {funcionario[0]}")
            print(f"Nome: {funcionario[1]}")
            print(f"Crachá: {funcionario[2]}")
            print(f"CNPJ: {funcionario[3]}")
            print(f"Entrada: {funcionario[4]}")
            print(f"Saída: {funcionario[5]}")
            print(f"Almoço início: {funcionario[6]}")
            print(f"Almoço fim: {funcionario[7]}")
            print(f"Horas acumuladas: {funcionario[8]}")

import sqlite3

class BancoDados:
    def __init__(self, nome_bd):
        self.nome_bd = nome_bd
        self.conexao = sqlite3.connect(nome_bd)
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS funcionarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                cracha TEXT UNIQUE NOT NULL,
                                cnpj TEXT NOT NULL,
                                horas_trabalhadas INTEGER DEFAULT 0,
                                hora_entrada TEXT,
                                hora_saida TEXT,
                                hora_entrada_almoço TEXT,
                                hora_saida_almoço TEXT
                                )''')
        self.conexao.commit()

    def inserir_funcionario(self, nome, cracha, cnpj):
        try:
            self.cursor.execute("INSERT INTO funcionarios (nome, cracha, cnpj) VALUES (?, ?, ?)",
                                (nome, cracha, cnpj))
            self.conexao.commit()
            print("Funcionário cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            print("Já existe um funcionário com esse crachá cadastrado.")

    def buscar_funcionario_por_nome(self, nome):
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome LIKE ?", ('%' + nome + '%',))
        return self.cursor.fetchall()

    def buscar_funcionario_por_cracha(self, cracha):
        self.cursor.execute("SELECT * FROM funcionarios WHERE cracha = ?", (cracha,))
        return self.cursor.fetchone()

    def buscar_funcionarios_por_cnpj(self, cnpj):
        self.cursor.execute("SELECT * FROM funcionarios WHERE cnpj = ?", (cnpj,))
        return self.cursor.fetchall()

    def listar_funcionarios(self):
        self.cursor.execute("SELECT * FROM funcionarios")
        return self.cursor.fetchall()

    def atualizar_horas_trabalhadas(self, cracha, horas):
        self.cursor.execute("UPDATE funcionarios SET horas_trabalhadas = horas_trabalhadas + ? WHERE cracha = ?", (horas, cracha))
        self.conexao.commit()
        print("Horas trabalhadas atualizadas com sucesso!")

    def atualizar_hora_entrada(self, cracha, hora):
        self.cursor.execute("UPDATE funcionarios SET hora_entrada = ? WHERE cracha = ?", (hora, cracha))
        self.conexao.commit()
        print("Hora de entrada atualizada com sucesso!")

    def atualizar_hora_saida(self, cracha, hora):
        self.cursor.execute("UPDATE funcionarios SET hora_saida = ? WHERE cracha = ?", (hora, cracha))
        self.conexao.commit()
        print("Hora de saída atualizada com sucesso!")

    def atualizar_hora_entrada_almoço(self, cracha, hora):
        self.cursor.execute("UPDATE funcionarios SET hora_entrada_almoço = ? WHERE cracha = ?", (hora, cracha))
        self.conexao.commit()
        print("Hora de entrada para o almoço atualizada com sucesso!")

    def atualizar_hora_saida_almoço(self, cracha, hora):
        self.cursor.execute("UPDATE funcionarios SET hora_saida_almoço = ? WHERE cracha = ?", (hora, cracha))
        self.conexao.commit()
        print("Hora de saída do almoço atualizada com sucesso!")
