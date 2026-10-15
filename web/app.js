const formulario = document.getElementById("formulario");
const campo = document.getElementById("cantidad");
const mensaje = document.getElementById("mensaje");
const lista = document.getElementById("historial");
const contador = document.getElementById("contador");
const vacio = document.getElementById("vacio");
const botonBorrar = document.getElementById("borrar");

async function validar(evento) {
  evento.preventDefault();

  const respuesta = await fetch("/api/validar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cantidad: campo.value }),
  });
  const resultado = await respuesta.json();

  if (resultado.valido) {
    mensaje.textContent = "✔ " + resultado.mensaje;
    mensaje.className = "mensaje ok";
    campo.className = "ok";
  } else {
    mensaje.textContent = "✖ " + resultado.mensaje;
    mensaje.className = "mensaje error";
    campo.className = "error";
    campo.select();
  }

  cargarHistorial();
}

async function cargarHistorial() {
  const respuesta = await fetch("/api/historial");
  const registros = await respuesta.json();

  lista.innerHTML = "";
  for (const registro of registros) {
    lista.appendChild(crearFila(registro));
  }

  const aceptadas = registros.filter((r) => r.resultado === "Aceptado").length;
  contador.textContent = `${aceptadas} aceptadas · ${registros.length - aceptadas} rechazadas`;
  vacio.hidden = registros.length > 0;
}

function crearFila(registro) {
  const estado = registro.resultado === "Aceptado" ? "ok" : "error";
  const fila = document.createElement("li");

  // Se usa textContent (no innerHTML) para que nadie pueda inyectar HTML.
  fila.append(
    crearElemento("punto " + estado, ""),
    crearElemento("valor", registro.valor || "(vacío)"),
    crearElemento("motivo", registro.motivo || "Aceptado"),
    crearElemento("fecha", registro.fecha.slice(11, 16)),
  );
  return fila;
}

function crearElemento(clase, texto) {
  const span = document.createElement("span");
  span.className = clase;
  span.textContent = texto;
  return span;
}

async function borrarHistorial() {
  if (confirm("¿Borrar todo el historial?")) {
    await fetch("/api/historial", { method: "DELETE" });
    cargarHistorial();
  }
}

formulario.addEventListener("submit", validar);
botonBorrar.addEventListener("click", borrarHistorial);
campo.addEventListener("input", () => (campo.className = ""));

cargarHistorial();
