// Comportamentos simples de interface (front-end em JavaScript puro).

// 1) Pede confirmação antes de enviar formulários destrutivos (ex.: excluir).
document.querySelectorAll("form[data-confirmar]").forEach(function (form) {
  form.addEventListener("submit", function (evento) {
    if (!window.confirm(form.dataset.confirmar)) {
      evento.preventDefault();
    }
  });
});

// 2) Trava o botão depois do primeiro envio, para dois cliques não criarem dois registros.
document.querySelectorAll("form[method='post']").forEach(function (form) {
  form.addEventListener("submit", function (evento) {
    if (evento.defaultPrevented) return; // a confirmação foi cancelada
    if (form.dataset.enviando) { evento.preventDefault(); return; } // já está enviando
    form.dataset.enviando = "1";
    form.querySelectorAll("button[type='submit']").forEach(function (botao) {
      botao.dataset.textoOriginal = botao.textContent;
      botao.disabled = true;
      if (botao.dataset.textoEnviando) botao.textContent = botao.dataset.textoEnviando;
    });
  });
});

// Ao voltar para a página pelo botão Voltar do navegador, libera os botões de novo.
window.addEventListener("pageshow", function () {
  document.querySelectorAll("form[data-enviando]").forEach(function (form) {
    delete form.dataset.enviando;
    form.querySelectorAll("button[type='submit']").forEach(function (botao) {
      botao.disabled = false;
      if (botao.dataset.textoOriginal) botao.textContent = botao.dataset.textoOriginal;
    });
  });
});

// 3) Mostra quantos caracteres ainda podem ser digitados na descrição.
document.querySelectorAll("textarea[data-contador]").forEach(function (campo) {
  var contador = document.getElementById(campo.dataset.contador);
  function atualizar() {
    var restantes = campo.maxLength - campo.value.length;
    contador.textContent = restantes + " caracteres restantes";
  }
  campo.addEventListener("input", atualizar);
  atualizar();
});

// 4) Mensagens de sucesso ficam na tela até a pessoa fechar.
document.querySelectorAll(".alerta-sucesso").forEach(function (alerta) {
  var fechar = document.createElement("button");
  fechar.type = "button";
  fechar.className = "fechar";
  fechar.setAttribute("aria-label", "Fechar mensagem");
  fechar.textContent = "×";
  fechar.addEventListener("click", function () { alerta.remove(); });
  alerta.appendChild(fechar);
});

// 5) No computador, o filtro já começa aberto; no celular, fica recolhido para a lista aparecer primeiro.
if (window.matchMedia("(min-width: 700px)").matches) {
  document.querySelectorAll("details[data-abrir-no-computador]").forEach(function (caixa) {
    caixa.open = true;
  });
}
