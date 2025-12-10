from models.usuario import Usuario

print('Creando usuario de prueba...')
try:
    u = Usuario.create_cliente('prueba123', 'secreto', {'nombre':'Prueba','email':'prueba123@example.com','telefono':'600'})
    print('Usuario creado:', u.username, 'id_cliente=', u.id_cliente)
except Exception as e:
    print('Error al crear usuario:', e)

print('Intentando login correcto...')
res = Usuario.login('prueba123', 'secreto')
print('Login ok:', bool(res))

print('Intentando login con contraseña errónea...')
res2 = Usuario.login('prueba123', 'mal')
print('Login ok:', bool(res2))
