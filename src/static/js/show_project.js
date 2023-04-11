// Ocultar concluidas:
const btOcultarConcluidas = document.getElementById("flexSwitchOcultarConcluidas");
btOcultarConcluidas.addEventListener("click", function(){
    if (btOcultarConcluidas.checked == true) {
        document.querySelectorAll(".task-row").forEach(item => {
            checked = item.querySelector('input').hasAttribute('checked');
            if (checked) {
                item.setAttribute("style", "display:none !important;")
            }
        });

    } else {
        document.querySelectorAll(".task-row").forEach(item => {
            item.setAttribute("style", "")
        });
    }
});

// Deletar tarefas:
document.querySelectorAll(".bt-delete-task").forEach(item => {
    item.addEventListener("click", () => {
        id = item
                .parentNode
                .parentNode
                .parentNode
                .id;
        delete_task(id);
        

    })
});

// Marcar tarefa como concluida:
document.querySelectorAll(".flexCheckDefault").forEach(item =>{
    item.addEventListener("click", () =>{
        let elementoTarefa = item.parentElement.querySelector("#taskName");
        console.log(elementoTarefa)
        row = item
                .parentNode
                .parentNode
                .parentNode
                .parentNode
                .parentNode;
        id = row.id;
        text = row.querySelector('.tachado');
        input = row.querySelector('input');
        
        finished = item.checked;
        toggle_task(id, finished);
        if (finished == true){
            // elementoTarefa.setAttribute("class", "form-check-label ml-3 task-complete");
            text.classList.toggle('checked');
            input.setAttribute('checked', '');
            // alert(`Tarefa concluída.`);
        } else {
            // elementoTarefa.setAttribute("class", "form-check-label ml-3");
            text.classList.toggle('checked');
            input.removeAttribute('checked');
            // alert(`Tarefa restaurada.`);
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

function add_task(id) {
    window.location.replace(`/tarefa/${id}`);
}

function toggle_task(id, finished) {

    data = {
        'id_task': id,
        'finished': finished
    }
    $.ajax({
        url : "/api/v1/task/toggle/",
        type : 'post',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        console.log("ajax",response,msg);
   })
   .fail(function(response, textStatus, msg){
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


function delete_task(id) {
    $.ajax({
        url : "/api/v1/task/" + id,
        type : 'delete',
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        console.log("ajax",response,msg);
        alert(response['message'])
        window.location.reload();
   })
   .fail(function(response, textStatus, msg){
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

$('.round').on("click", function(event) {
    // Do something here
    event.stopPropagation();
});

$('.bt-delete-task').on("click", function(event) {
    // Do something here
    event.stopPropagation();
});
