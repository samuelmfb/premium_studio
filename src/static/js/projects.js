const list = document.getElementById("lista");
const customer = (document.getElementById('project').getAttribute('customer'));

$(document).ready(function() {
    login_validation();
    id = "";
    if (customer != "") { 
        id = "/" + customer;
    } 
    $.ajax({
        url : "/api/v1/project" + id,
        type : 'get',
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        console.log("ajax",response,msg);
        html = "";
        projects = [];
        if (Array.isArray(response['data'])){
            projects = response['data']    
        } else {
            projects.push(response)
        }
        for (project in projects) {
            if (project == 0){
                html = "<h5>Sem projetos cadastrados para este cliente.</h5>"
                break
            }
            id = projects[project]['id_project'];
            html += "<div id='" + id +"' class='container-md bg-light-blue d-flex justify-content-between align-content-center ml-0 mb-3' onclick='show_project("+ id+")' > \
                <p class='m-3'>" + projects[project]['name']+ "</p> \
            </div>"
        }
        list.innerHTML = html;   
        
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
});

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

function show_project(id) {
    window.location.replace("/exibir_projeto/" + id);
}