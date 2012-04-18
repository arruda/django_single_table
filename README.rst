...
gerar ModelManager dinamicamente para os modelos proxies em que criam as queries são diferenciadas pelo tipo da classe 'pai'(que nao é proxy)

alterar o save do type de um modelo proxy para que ele salve com o valor que representa o proxy model.
mudar o default do valor do campo type tmb?

colocar o campo type no 'pai' automaticamente(heranca ou decorator), e onde o campo teria o nome como:
__class__.__name__+_type
