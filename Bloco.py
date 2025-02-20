class Bloco:
    def __init__(self):
        self.ocupado = False
        self.nomeArquivo = None
        self.proximoBloco = None  # para Alocação encadeada
        self.data = None

class FileSystem:
    def __init__(self, totalDeBlocos):
        self.totalDeBlocos = totalDeBlocos
        self.blocos = [Bloco() for _ in range(totalDeBlocos)]
        self.tabelaDeArquivo = {}  # Armazena metadados de Arquivo
        self.blocosDeIndice = {}  # Para alocação indexada

    def encontraBlocosContiguos(self, tamanho):

       # Encontra blocos contíguos para alocação
        contador = 0
        blocoDeInicio = -1
        
        for i in range(self.totalDeBlocos):
            if not self.blocos[i].ocupado:
                if contador == 0:
                    blocoDeInicio = i
                contador += 1
                if contador == tamanho:
                    return blocoDeInicio
            else:
                contador = 0
        return -1

    def alocacaoContigua(self, nomeArquivo, tamanho):

        # encontra blocos contíguos para alocação
        blocoDeInicio = self.encontraBlocosContiguos(tamanho)
        if blocoDeInicio == -1:
            return False, "Sem espaço contíguo suficiente para alocação"

        for i in range(blocoDeInicio, blocoDeInicio + tamanho):
            self.blocos[i].ocupado = True
            self.blocos[i].nomeArquivo = nomeArquivo

        self.tabelaDeArquivo[nomeArquivo] = {
            'blocoDeInicio': blocoDeInicio,
            'tamanho': tamanho,
            'tipo': 'contíguo'
        }
        return True, f"Arquivo alocado Contiguamente do bloco {blocoDeInicio} ao {blocoDeInicio + tamanho - 1}"

    def alocacaoEncadeada(self, nomeArquivo, tamanho):
       
        blocosLivres = []
        for i in range(self.totalDeBlocos):
            if not self.blocos[i].ocupado:
                blocosLivres.append(i)
                if len(blocosLivres) == tamanho:
                    break

        if len(blocosLivres) < tamanho:
            return False, "Sem Blocos Livres suficientes para alocação encadeada"

        # Conecta os blocos 
        for i in range(len(blocosLivres)):
            current_block = blocosLivres[i]
            self.blocos[current_block].ocupado = True
            self.blocos[current_block].nomeArquivo = nomeArquivo
            if i < len(blocosLivres) - 1:
                self.blocos[current_block].proximoBloco = blocosLivres[i + 1]

        self.tabelaDeArquivo[nomeArquivo] = {
            'blocoDeInicio': blocosLivres[0],
            'tamanho': tamanho,
            'tipo': 'Encadeada'
        }
        return True, f"Arquivo alocado usando alocação Encadeada. Bloco de Inicio: {blocosLivres[0]}"

    def alocacaoIndexada(self, nomeArquivo, tamanho):
        
        # Encontra um bloco para indices
        indiceBloco = -1
        for i in range(self.totalDeBlocos):
            if not self.blocos[i].ocupado:
                indiceBloco = i
                break

        if indiceBloco == -1:
            return False, "Sem espaço para bloco de Indice"

        # Encontra blocos para dados
        blocosDeDados = []
        for i in range(self.totalDeBlocos):
            if not self.blocos[i].ocupado and i != indiceBloco:
                blocosDeDados.append(i)
                if len(blocosDeDados) == tamanho:
                    break

        if len(blocosDeDados) < tamanho:
            return False, "Sem blocos suficientes para alocação indexada"

        # Aloca Bloco de índice e de dados
        self.blocos[indiceBloco].ocupado = True
        self.blocos[indiceBloco].nomeArquivo = nomeArquivo
        self.blocosDeIndice[nomeArquivo] = blocosDeDados

        for block_num in blocosDeDados:
            self.blocos[block_num].ocupado = True
            self.blocos[block_num].nomeArquivo = nomeArquivo

        self.tabelaDeArquivo[nomeArquivo] = {
            'blocoDeInicio': indiceBloco,
            'tamanho': tamanho,
            'tipo': 'Indexada'
        }
        return True, f"Arquivo alocado usando alocação Indexada. Bloco de índice: {indiceBloco}"

    def deletaArquivo(self, nomeArquivo):

        # Deleta um arquivo e libera seu Espaço no disco
        if nomeArquivo not in self.tabelaDeArquivo:
            return False, "Arquivo não encontrado"

        file_info = self.tabelaDeArquivo[nomeArquivo]
        
        if file_info['tipo'] == 'contíguo':
            inicio = file_info['blocoDeInicio']
            tamanho = file_info['tamanho']
            for i in range(inicio, inicio + tamanho):
                self.blocos[i].ocupado = False
                self.blocos[i].nomeArquivo = None
        
        elif file_info['tipo'] == 'Encadeada':
            atual = file_info['blocoDeInicio']
            while atual is not None:
                proximoBloco = self.blocos[atual].proximoBloco
                self.blocos[atual].ocupado = False
                self.blocos[atual].nomeArquivo = None
                self.blocos[atual].proximoBloco = None
                atual = proximoBloco
        
        elif file_info['tipo'] == 'Indexada':

            # libera bloco de índice
            blocoDeIndice = file_info['blocoDeInicio']
            self.blocos[blocoDeIndice].ocupado = False
            self.blocos[blocoDeIndice].nomeArquivo = None
            
            # Desaloca blocos de dados
            for numBloco in self.blocosDeIndice[nomeArquivo]:
                self.blocos[numBloco].ocupado = False
                self.blocos[numBloco].nomeArquivo = None
            
            del self.blocosDeIndice[nomeArquivo]

        del self.tabelaDeArquivo[nomeArquivo]
        return True, f"Arquivo {nomeArquivo} deletado com sucesso"

    def estadoDeDisco(self):
        
        print("\nEstado do Disco:")
        print("-" * 50)
        for i in range(self.totalDeBlocos):
            block = self.blocos[i]
            estado = f"Bloco {i:3d}: "
            if block.ocupado:
                estado += f"[Ocupado - {block.nomeArquivo}]"
                if block.proximoBloco is not None:
                    estado += f" -> {block.proximoBloco}"
            else:
                estado += "[Livre]"
            print(estado)
        print("-" * 50)
        print("\nTabela de Arquivo:")
        for nomeArquivo, info in self.tabelaDeArquivo.items():
            print(f"{nomeArquivo}: {info}")
        print("-" * 50)