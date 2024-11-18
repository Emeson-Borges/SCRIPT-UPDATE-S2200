# Atualizar Recibos do Evento S2200 -> eSocial

## Faça a consulta no banco de dados
`select idevento,cpftrab from esocial.s2200 where idevento in (select idevento from esocial.historico where status='A')`

pegue o resultado e coloque na lista dentro do Script em Python.

`lista_ids_cpfs = [`

 `   ("IDEVENTO", "CPF"),`

`]`

