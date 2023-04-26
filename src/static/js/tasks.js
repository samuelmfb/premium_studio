const button = document.getElementById("bt-submit");
const project = Number(document.getElementById('task').getAttribute('project'));
$(document).ready(function() {
    login_validation();
})
button.addEventListener("click", function(e){
    e.preventDefault();
    const title = document.getElementById('title').value;
    const deadline = document.getElementById('deadline').value;
    const description = document.getElementById('description').value;

    if (title.length == 0) {
        alert("Título da tarefa não pode estar em branco.");
        return false;
    }
    data = {
        "title": title,
        "deadline" : deadline,
        "description" : description,
        "id_project" : project
    }
    $.ajax({
        url : "/api/v1/task",
        type : 'post',
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg){
        console.log(response,msg);
        alert('Tarefa adicionada com sucesso!');
        window.location.replace("/exibir_projeto/" + project);
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
})

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
