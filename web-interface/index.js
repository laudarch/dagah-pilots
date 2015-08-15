function ls() {
    
    var xmlhttp;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.open("GET","/ls",false);
    xmlhttp.send();
    document.getElementById("results").innerHTML=xmlhttp.responseText;
}

function ps() {
    
    var xmlhttp;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.open("GET","/ps",false);
    xmlhttp.send();
    document.getElementById("results").innerHTML=xmlhttp.responseText;
}

function clear_command(){ document.getElementById("command").innerHTML="python dagah.py"; }

function apply_M(){
    add_M();
    add_n();
    add_u();
    add_k();
}

function add_M(){
    var radios = document.getElementsByName('radio_M');
    var radio_value;
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            radio_value=radios[i].value;
            break;
        }
    }
    document.getElementById("command").innerHTML+=" -M "+radio_value;
}

function add_n(){
    var value = " -n ";
    value += document.getElementById("n_phone").value;
    document.getElementById("command").innerHTML+=value.toString();
}

function add_u(){
    var value = " -u ";
    value += document.getElementById("u_url").value;
    document.getElementById("command").innerHTML+=value.toString();
}

function add_k(){
    var value = " -k ";
    value += document.getElementById("k_key").value;
    document.getElementById("command").innerHTML+=value.toString();
}
