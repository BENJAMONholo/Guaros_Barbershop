import pywhatkit

def enviar_notificacion(cliente, servicio, fecha, hora, barbero):
    # IMPORTANTE: Reemplaza este número por el tuyo incluyendo el +569
    NUMERO_BARBERO = "+56950963280" 
    
    mensaje = f"""💈 *NUEVA RESERVA EN GUARO'S* 💈

*Cliente:* {cliente}
*Servicio:* {servicio}
*Fecha:* {fecha}
*Hora:* {hora}

Revisa tu panel de agendamiento para más detalles."""

    print("🤖 Preparando el envío por WhatsApp Web...")
    try:
        # Abre el navegador, pega el mensaje y lo envía. 
        # wait_time=15 le da 15 segundos a tu internet para cargar WhatsApp Web
        # tab_close=True cierra la pestaña automáticamente después de enviar
        pywhatkit.sendwhatmsg_instantly(
            phone_no=NUMERO_BARBERO, 
            message=mensaje, 
            wait_time=15, 
            tab_close=True, 
            close_time=3
        )
        print("✅ WhatsApp enviado con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar el WhatsApp: {e}")