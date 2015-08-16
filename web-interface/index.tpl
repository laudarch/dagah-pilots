<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="index.css">
<link rel="stylesheet" href="jquery-ui.min.css">
<script src="jquery.js"></script>
<script src="jquery-ui.min.js"></script>
<script src="index.js" ></script>
<script>
  $(function() {
    $( "#accordion" ).accordion({
      collapsible: true
    });
  });
  </script>
</head>
<body>
<h1>Dagah</h1>
<hr>
<h2>The Command To Execute</h2>
<h3><div id="command">python dagah.py</div></h3>
<button onclick="clear_command()">CLEAR</button><br />
<button onclick="execute_command()">EXECUTE</button>
<hr>
<h2>Command Builder</h2>
<h4>Required Command Line Options:</h4>
<div id="accordion">
  <h3>-M :type of attached modem (app/usb)</h3>
  <div>
    <ul class="parameter_list">
      <li class="parameter">
        <input type="text" id="M_type"> -M :type of attached modem (app/usb)
      </li>
      <li class="parameter">
        <input type="text" id="M_n_phone"> -n :phone number of modem
      </li>
      <li class="parameter">
        <input type="text" id="M_u_url"> -u :url on webserver where modem checks in
      </li>
      <li class="parameter">
        <input type="text" id="M_k_key"> -k :key to control modem
      </li>
      <li class="parameter"><button onclick="apply_M()">apply</button></li>
    </ul>
  </div>
  <h3>-P :type of phishing attack (basic,harvester,autopwn,autoagent)</h3>
  <div>
    <ul class="parameter_list">
      <li class="parameter">
        <input type="text" id="P_type-of-attack"> -P :type of phishing attack (basic,harvester,autopwn,autoagent)
      </li>
      <li class="parameter">
        <input type="text" id="P_u_url-on-webserver"> -u :url on webserver
      </li>
      <li class="parameter">
        <input type="text" id="P_d_delivery-method"> -d :delivery method (sms/nfc)
      </li>
      <li class="parameter">
        <input type="text" id="P_n_url"> -n/-N :number/file of numbers to attack(fix me)
      </li>
      <li class="parameter">
        <input type="text" id="P_p_page-name"> -p :page name
      </li>
      <li class="parameter">
        <input type="text" id="P_t_custom-text-SMS"> -t :custom text for SMS
      </li>
      <li class="parameter">
        <input type="text" id="P_c_page-to-clone"> -c :page to clone for credential harvester
      </li>
      <li class="parameter">
        <input type="text" id="P_f_file-to-import"> -f :file to import
      </li>
      <li class="parameter">
        <input type="text" id="P_l_label-for-campaign"> -l :label for campaign
      </li>
      <li class="parameter">
        <input type="text" id="P_a_appstore-link"> -a :appstore link for hosted app (official or third party)
      </li>
      <li class="parameter"><button onclick="apply_P()">apply</button></li>
    </ul>
  </div>
  <h3>-A :Start API (REST)</h3>
  <div>
    <li class="parameter">
      <input type="text" id="A_start-API"> -A :Start API (REST)
    </li>
    <li class="parameter">
      <input type="text" id="A_u_url-for-API"> -u :url on webserver for API
    </li>
    <li class="parameter">
      <input type="text" id="A_k_api-key"> -k :api key
    </li>
    <li class="parameter"><button onclick="apply_A()">apply</button></li>
  </div>
  <h3>-S :poller to shutdown (api, modem, all)</h3>
  <div>
    <li class="parameter">
      <input type="text" id="S_poller-to-shutdown"> -S :poller to shutdown (api, modem, all)
    </li>
    <li class="parameter"><button onclick="apply_S()">apply</button></li>
  </div>
  <h3>-R :reporting function (get, drop)</h3>
  <div>
    <li class="parameter">
      <input type="text" id="R_reporting-function"> -R :reporting function (get, drop)
    </li>
    <li class="parameter"><button onclick="apply_R()">apply</button></li>
  </div>
</div>



<!--


<div class="parameter_group">
  <ul class="parameter_list">
    <li class="parameter">
      <fieldset class="parameter">
        <legend>Type of phishing attack</legend>
        <ul class="radio">
          <li><input type="radio" name="phishing_type" id="phishing_basic" value="basic" ><label for="M_app">basic</label></li>
          <li><input type="radio" name="phishing_type" id="phishing_harvester" value="harvester" ><label for="M_app">harvester</label></li>
          <li><input type="radio" name="phishing_type" id="phishing_autopwn" value="autopwn" ><label for="M_app">autopwn</label></li>
          <li><input type="radio" name="phishing_type" id="phishing_autoagent" value="autoagent" ><label for="M_app">autoagent</label></li>
        </ul>
      </fieldset>
    </li>
    <li class="parameter">
      <fieldset class="parameter">
        <legend>url on webserver</legend>
        <input type="text" id="u_url">
      </fieldset>
    </li>
    <li class="parameter">
      <fieldset class="parameter">
        <legend>url on webserver where modem checks in</legend>
        <input type="text" id="u_url">
      </fieldset>
    </li>
    <li class="parameter">
      <fieldset class="parameter">
        <legend>url on webserver where modem checks in</legend>
        <input type="text" id="u_url">
      </fieldset>
    </li>
  </ul>
  
</div>
<div class="parameter_group">
    -P <phishing attack> (basic,harvester,autopwn,autoagent)<br />
    -u <url on webserver><br />
    -d <delivery method> (sms/nfc)<br />
    -n/-N <number/file of numbers> to attack<br />
    -p <page name><br />
    -t <custom text> for SMS<br />
    -c <page> to clone for credential harvester<br />
    -f <file> to import<br />
    -l <label> for campaign<br />
    -a <appstore> link for hosted app (official or third party)<br />
    -A <API> Start API (REST)<br />
    -u <url on webserver> for API<br />
    -k <api key><br />
    -S <poller> to shutdown (api, modem, all)<br />
    -R <reporting function> (get, drop)<br />
</div>
<hr>
<p id="results"></p>
-->
</body>
</html>
