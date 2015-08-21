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
    add_option("-M", "M_type");
    add_option("-n", "M_n_phone");
    add_option("-u", "M_u_url");
    add_option("-k", "M_k_key");
}
function apply_P(){
    add_option("-P", "P_type-of-attack");
    add_option("-u", "P_u_url-on-webserver");
    add_option("-d", "P_d_delivery-method");
    add_option("-p", "P_p_page-name");
    add_option("-t", "P_t_custom-text-SMS");
    add_option("-c", "P_c_page-to-clone");
    add_option("-f", "P_f_file-to-import");
    add_option("-l", "P_l_label-for-campaign");
    add_option("-a", "P_a_appstore-link");
}
function apply_A(){
    add_option("-A", "A_start-API");
    add_option("-u", "A_u_url-for-API");
    add_option("-k", "A_k_api-key");
}
function apply_S(){
    add_option("-S", "S_poller-to-shutdown")
}
function apply_R(){
    add_option("-R","R_reporting-function");
}
function add_option(parameter, id){
    var val = " ";
    val+=parameter;
    val+=" ";
    val+=document.getElementById(id).value;
    document.getElementById("command").innerHTML+=val.toString();
}

