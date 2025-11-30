console.log("✅ JavaScript carregado");

// Admin padrão
const user_adm = "Rafael";
const key_adm = "12345";

// LOGIN
document.addEventListener("DOMContentLoaded", () => {
  const userInput = document.getElementById("user");
  const passInput = document.getElementById("pass");
  const loginBtn = document.getElementById("btn_entrar");
  const errorBox = document.getElementById("login_error");

  if(loginBtn) {
    loginBtn.addEventListener("click", async() => {
      errorBox.textContent = "";

      const usuario = userInput.value.trim();
      const senha = passInput.value.trim();

      if(!usuario || !senha) {
        errorBox.textContent = "Preencha usuário e senha.";
        return;
      }

      try{
        const response = await fetch("/api/login", {
          method: "POST",
          headers: {"Content-Type" : "application/json"},
          body: JSON.stringify({usuario, senha})
        });

        // Limite de tentativas
         if (response.status === 429) {
    const data = await response.json().catch(() => ({}));
    errorBox.textContent = data.erro || "Muitas tentativas. Tente novamente mais tarde.";
    return;
  }

  // tenta ler JSON; se falhar, trata
  let data;
  try {
    data = await response.json();
  } catch (parseErr) {
    console.error("Resposta não é JSON:", parseErr);
    errorBox.textContent = "Resposta inválida do servidor.";
    return;
  }

  console.log("STATUS:", response.status, "BODY:", data);

  if (response.status !== 200 || !data.ok) {
    errorBox.textContent = data.erro || "Usuário ou senha incorretos.";
    return;
  }

  errorBox.textContent = "";
  alert("Login efetuado com sucesso");
  // window.location.href = "/materia.html";

} catch (err) {
  console.error(err);
  errorBox.textContent = "Erro ao conectar com o servidor.";
}
      
    });
  }
});

// REGISTRO

const btn_registrar = document.getElementById("registrar");

if (btn_registrar) {
  btn_registrar.addEventListener("click", function (event) {
    event.preventDefault();

    const usuario = document.getElementById("new_user").value;
    const senha = document.getElementById("new_pass").value;
    const confirm = document.getElementById("confirm_pass").value;

    if (senha !== confirm || usuario.trim() === "") {
      alert("Verifique os dados!");
      return;
    }
    console.log("Botão de registro clicado!!")
    fetch('/api/registrar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuario, senha })
    })
    .then(res => res.text())
    .then(msg => {
      alert(msg);
      window.location.href = "teladelogin.html";
    })
    .catch(err => {
      alert("Erro ao registrar.");
      console.error(err);
    });
  });
}



// VOLTAR
const btn_back = document.getElementById("back");

if (btn_back) {
  btn_back.addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "teladelogin.html";
  });
}
