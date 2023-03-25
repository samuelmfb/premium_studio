const project = document.getElementById('project').getAttribute('project');
const project_name = document.getElementById('project_name');
const producer = document.getElementById('producer');
const customer = document.getElementById('customer');
const full_value = document.getElementById('full_value');

$(document).ready(function() {
    login_validation();
    $.ajax({
        url : "/api/v1/project/" + project,
        type : 'get',
        contentType: "application/json; charset=utf-8",
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        project_name.innerText = response['description'];
        producer.innerText = "Produtor: " + response['producer'];
        customer.innerText = "Cliente: " + response['customer'];
        full_value.innerText = "Valor: " + response['full_value'];
        $.ajax({
            url : "/api/v1/task/" + project,
            type : 'get',
            contentType: "application/json; charset=utf-8",
            headers: {"Authorization": "Bearer " + getCookie('premium_access')}
       })
        .done(function(response, msg, data){
            project_name.innerText = response['description'];
            producer.innerText = "Produtor: " + response['producer'];
            customer.innerText = "Cliente: " + response['customer'];
            full_value.innerText = "Valor: " + response['full_value'];
            
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