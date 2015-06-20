# Implementação de técnicas de detecção de erros
## Trabalho de TR1 1o/2015

* Daniella Angelos
* Francisco Anderson
* Guilherme Branco
* Lucas Amaral
* Pedro Henrique Lima

## Arquivo de configuração


A configuração é feita através de um arquivo no formato JSON, da seguinte maneira:

```
{
    "server" : {
        "flip" : 0,
        "port" : 12345
    },
    "clients" : {
        "algoritmo" : 1,
        "destinos" : [2,1,0],
        "server_port" : 12345
    }
}
```

Onde

* Flip: Modo de flipar os bits, pode ser:
 - 0 = Não flipar
 - 1 = Aleatório
 - 2 = Só os pares
 - 3 = Só os ímpares

* Port e server\_port são o mesmo valor, pra dizer qual a porta do servidor.

* Algoritmo é um número representando o algoritmo utilizado para se realizar o checksum, onde:
 - 0 = SHA1
 - 1 = MD5
 - 2 = Hamming
 - 3 = CRC

* As partes "server" e clients são independentes e utilizadas somente pelo respectivo programa.
