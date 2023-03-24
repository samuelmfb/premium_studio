const list = document.getElementById("lista");

$(document).ready(function() {
    let html_roles = "";
    $.ajax({
        url : "/api/v1/user_role",
        type : 'get',
        contentType: "application/json; charset=utf-8",
        async: false, 
        headers: {"Authorization": "Bearer " + getCookie('premium_access')}
   })
    .done(function(response, msg, data){
        html_roles = "<select class='form-select m-3' aria-label='Atribuir perfil de acesso' style='width:250px'> \
            <option selected>Atribuir perfil de acesso</option>";
        const roles = response['data'];
        for (role in roles) {
            html_roles += "<option value='" + role + "'>" + roles[role]['user_role_name'] + "</option>";
        }
        html_roles += "</select>";
        $.ajax({
            url : "/api/v1/user",
            type : 'get',
            contentType: "application/json; charset=utf-8",
            async: false, 
            headers: {"Authorization": "Bearer " + getCookie('premium_access')}
       })
        .done(function(response, msg, data){
            html = "";
            users = response['data'];
            console.log(roles)
            for (user in users) {
                html += "<div id='" + user +"' class='container-md bg-light-blue d-flex justify-content-between align-content-center ml-0 mb-3' > \
                    <p class='m-3'>" + users[user]['user_name']+ "</p> \
                    " + html_roles + " \
                </div>"
            }
            list.innerHTML = html;
            
       })
       .fail(function(response, textStatus, msg){
            const error = response['responseJSON']['error'];
            alert(error);
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
        console.log(html)
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