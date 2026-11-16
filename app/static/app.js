// Comportamentos simples de interface (front-end em JavaScript puro).

// 1) Pede confirmação antes de enviar formulários destrutivos (ex.: excluir).
document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
  form.addEventListener("submit", function (evento) {
    if (!window.confirm(form.dataset.confirmar)) {
      evento.preventDefault();
    }
  });
});

// 2) Mostra quantos caracteres ainda podem ser digitados na descrição.
document.querySelectorAll("textarea[data-contador]").forEach(function (campo) {
  var contador = document.getElementById(campo.dataset.contador);
  function atualizar() {
    var restantes = campo.maxLength - campo.value.length;
    contador.textContent = restantes + " caracteres restantes";
  }
  campo.addEventListener("input", atualizar);
  atualizar();
});

// 3) Some com as mensagens de sucesso depois de alguns segundos.
document.querySelectorAll(".alerta-sucesso").forEach(function (alerta) {
  setTimeout(function () { alerta.remove(); }, 4000);
});
