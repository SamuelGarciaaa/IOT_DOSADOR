let p_trocar = document.getElementById('p_trocar');
let login_register_title = document.getElementById('login_register_title');
let hide_area = document.getElementById('hide-area');

//Função pra trocar o texto
function trocar_texto(){
    let input  = document.getElementById('variableToTellWhatWeAreUsing');

    //Condição para transformar em login
    if(input.value === 'register'){
        input.value = 'login';
        hide_area.classList.add('d-none');
        login_register_title.textContent = 'Fazer login';
        p_trocar.textContent = 'Não possui conta? Crie uma';
    }

    //Condição para transformar em cadastro
    else{
        input.value = 'register';
        hide_area.classList.remove('d-none');
        login_register_title.textContent = 'Criar uma conta';
        p_trocar.textContent = 'Já tem uma conta? Faça login';
    }
}