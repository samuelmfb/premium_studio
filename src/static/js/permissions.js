const list = document.getElementById("lista");
const search = document.getElementById("search");



$(document).ready(function() {
    login_validation();
});


function list_roles() {
    $.ajax({
        url : "/api/v1/user_role",
        type : 'get',
        contentType: "application/json; charset=utf-8",
        async: false, 
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        let html = "<select class='form-select m-3' aria-label='Atribuir perfil de acesso' style='width:250px'> \
            <option selected>Atribuir perfil de acesso</option>";
        const roles = response['data'];
        for (role in roles) {
            html += "<option value='" + role + "'>" + roles[role]['user_role_name'] + "</option>";
        }
        html += "</select>";
        return html;
        
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
        console.log("Usuário logado.");
        
   })
   .fail(function(response, textStatus, msg){
    console.log("Usuário não logado.");
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

function search_user() {
    var users = document.getElementsByClassName("user");
    let search_text = ""; 
    search_text = search.value;
    console.log(search_text)
    search_length = search_text.length;
    for (var i = 0; i < users.length; i++) {
        let user = users[i].innerText.split('\n')[0];
        console.log("oculto:",users[2])
        if (user.trim().substring(0,search_length) != search_text) {
            console.log(user.trim().substring(0,search_length), search_text, "diferente - oculta")
            users[i].setAttribute("style", "display: none !important;");
            document.getElementById(users[i].id).innerHTML = users[i].innerHTML;
        } else if (search_text == "") {
            console.log(user.trim().substring(0,search_length), search_text, "igual - exibe")
            users[i].setAttribute("style", "");
            document.getElementById(users[i].id).innerHTML = users[i].innerHTML;
        } else {
            console.log(user.trim().substring(0,search_length), search_text, "igual - exibe")
            users[i].setAttribute("style", "");
            document.getElementById(users[i].id).innerHTML = users[i].innerHTML;
        };
    }
}

function check_option(item) {
    id = item
        .parentNode
        .id;
    option = item.value;
    // create new producer
    if (option == 2){
        create_producer(id);
    }
    // 
}

function create_producer(id) {
    data = {"id_user": id };
    $.ajax({
        url : "/api/v1/producer/user_producer",
        type : 'post',
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg){
        console.log(response,msg);
        alert('Registro adicionado com sucesso!');
        location.reload();
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