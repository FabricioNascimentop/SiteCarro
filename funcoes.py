def data_preco(obj_carro):
    obj_carro.registro = obj_carro.registro.strftime('%d/%m/%Y')
    obj_carro.preco = moedinha(obj_carro.preco)
    return obj_carro

def moedinha(numero):
    numero_formatado = '{:.2f}'.format(numero)
    parte_inteira, parte_decimal = numero_formatado.split('.')
    parte_inteira = '{:,}'.format(int(parte_inteira)).replace(',', '.')
    valor_formatado = f'R$ {parte_inteira},{parte_decimal}'
    return valor_formatado

def enviar_email(assunto, texto, remetente, destinatário):
    import smtplib
    import email.message  
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatário
    password = 'yohplhritxndnazq'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(texto)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('email enviado com sucesso')


