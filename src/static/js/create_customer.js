const button = document.getElementById("bt-submit");


button.addEventListener("click", function(e){
    e.preventDefault();
    const name = document.getElementById('name').value;
    const phone_num = document.getElementById('phone_num').value;
    const email = document.getElementById('email').value;
    data = {
        "name": name,
        "phone_num" : name,
        "email" : email
    }
    $.ajax({
        url : "/api/v1/customer",
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
                alert(msg);
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