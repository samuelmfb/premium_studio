// Adicionar nova tarefa:
const btNewTask = document.getElementById("bt-new-task");
btNewTask.addEventListener("click", function(e) {
    e.preventDefault();
    window.location.replace("/tarefa")
});

// Ocultar concluidas:
const btOcultarConcluidas = document.getElementById("flexSwitchOcultarConcluidas");
btOcultarConcluidas.addEventListener("click", function(){
    if (btOcultarConcluidas.checked == true) {
        alert("Ocultou as tarefas concluidas");
    } else {
        alert("Mostrou as tarefas concluidas");
    }
});

// Deletar tarefas:
document.querySelectorAll(".bt-delete-task").forEach(item => {
    item.addEventListener("click", () => {
        let nomeTarefa = item.parentElement.querySelector("#taskName").textContent;
        alert(`Clicou para deletar a tarefa: ${nomeTarefa}`);
    })
});

// Marcar tarefa como concluida:
document.querySelectorAll(".flexCheckDefault").forEach(item =>{
    item.addEventListener("click", () =>{
        let nomeTarefa = item.parentElement.querySelector("#taskName").textContent;
        if (item.checked == true){
            alert(`Concluiu a tarefa: ${nomeTarefa}`);
        } else {
            alert(`Restaurou a tarefa: ${nomeTarefa}`);
        }
    })
});


// PARTE DO SAMUEL:

$(document).ready(function() {
    login_validation();
    
})
function login_validation() {
    if (getCookie('premium_access') == "") {
        alert('Usuário não logado. Redirecionando para a tela de login.');
                window.location.replace("/login")
    }
    $.ajax({
        url : "/api/v1/auth/me",
        type : 'get',
        contentType: "application/json; charset=utf-8",
        async: false,
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        console.log(response, msg);

   })
   .fail(function(response, textStatus, msg){
    console.log(response, msg);
        if ('msg'in response['responseJSON']){
            msg = response['responseJSON']['msg'];
            if (msg == 'Token has expired') {
                alert('Token expirou. Redirecionando para a tela de login.');
                window.location.replace("/login");
            };
        }
        if ('error'in response['responseJSON']){
            const error = response['responseJSON']['error'];
            if (error) {
                alert(error);
            };
        }
    });
}
function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

function getCookie(cname) {
let name = cname + "=";
let ca = document.cookie.split(';');
for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
    c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
    return c.substring(name.length, c.length);
    }
}
return "";
}
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})