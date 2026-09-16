// Agrega esto en tu app.js

async function cargarCitasBarbero() {
    try {
        // 1. Consultamos las citas reales al backend
        const respuesta = await fetch('http://127.0.0.1:5000/api/citas');
        const citas = await respuesta.json();
        
        // 2. Seleccionamos el contenedor en el HTML
        const contenedor = document.getElementById('lista-itinerario');
        
        // 3. Limpiamos los datos de prueba
        contenedor.innerHTML = '';
        
        if (citas.length === 0) {
            contenedor.innerHTML = '<p style="color: white; opacity: 0.5;">No hay citas agendadas aún.</p>';
            return;
        }

        // 4. Dibujamos cada cita real en el panel
        citas.forEach(cita => {
            const divCita = document.createElement('div');
            // Asegúrate de que estas clases coincidan con tu CSS actual para que mantenga el diseño oscuro lindo
            divCita.className = 'appointment-item glass-card'; 
            divCita.innerHTML = `
                <div class="time-col">
                    <span class="time-main">${cita.hora_inicio}</span>
                </div>
                <div class="info-col">
                    <h4>${cita.cliente} <span class="status-badge">Pendiente</span></h4>
                    <p>✂️ ${cita.servicio} (${cita.duracion})</p>
                </div>
            `;
            contenedor.appendChild(divCita);
        });
        
    } catch (error) {
        console.error("Error al cargar citas:", error);
    }
}

// Ejecutar la función cuando el barbero haga clic en el botón de "Actualizar"
document.querySelector('.btn-actualizar').addEventListener('click', cargarCitasBarbero);

// Opcional: Llamar a la función automáticamente cuando el barbero inicie sesión con el PIN
// cargarCitasBarbero();