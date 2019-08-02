$(document).ready(function(){

    $('#login').click(function(){
        window.location.href = "login"
    });

    function showError(error){
        $('#error').html(error)
    }

    $('#submit').click(function(){
        var login = $('#login_text').val(),
            password = $('#password'),
            password2 = $('#password2');
        console.log(login, password.val(), password2.val());
        if(password.val() === password2.val()){
            console.log(login, 'if pass the same');
            if (login  && password){
                $.post('signin', {'login': login, 'password': password.val()}, function(data){
                    console.log(data);
                    if (data.error){
                        showError(data.error)
                    }else{
                        window.location.href = '/'
                    }
                });
            }else{
                showError('Please fill all fields')
            }
        }else{
            showError('Passwords must be the same');
        }
    });
});
