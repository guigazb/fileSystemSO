from Bloco import FileSystem

#Cria um Sistema de arquivos (memória virtual) de 20 blocos
fs = FileSystem(20)

# Exibe o estado inicial do disco
print("Estado Inicial:")
fs.estadoDeDisco()

# Testando alocação contígua
print("\nAlocando arquivo1.txt (contíguo, 3 blocos):")
sucesso, mensagemRetorno = fs.alocacaoContigua("arquivo1.txt", 3)
print(mensagemRetorno)
fs.estadoDeDisco()

# Testa alocação encadeada
print("\nAlocando arquivo2.txt (Encadeado, 4 blocos):")
sucesso, mensagemRetorno = fs.alocacaoEncadeada("arquivo2.txt", 4)
print(mensagemRetorno)
fs.estadoDeDisco()

# Testa alocação indexada
print("\nAlocando arquivo3.txt (indexado, 3 blocos):")
sucesso, mensagemRetorno = fs.alocacaoIndexada("arquivo3.txt", 3)
print(mensagemRetorno)
fs.estadoDeDisco()

# Testa exclusão de arquivo
print("\nDeletando arquivo1.txt:")
sucesso, mensagemRetorno = fs.deletaArquivo("arquivo1.txt")
print(mensagemRetorno)
fs.estadoDeDisco()

# Aloca o arquivo4
print("\nAlocando arquivo4.txt (Encadeado, 4 blocos):")
sucesso, mensagemRetorno = fs.alocacaoEncadeada("arquivo4.txt", 4)
print(mensagemRetorno)
fs.estadoDeDisco()