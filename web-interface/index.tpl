<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="index.css">
<script src="index.js" ></script>
</head>
<body>
<h1>Dagah</h1>
<hr>
<h2>The Command To Execute</h2>
<h3><div id="command">python dagah.py</div></h3>
<button onclick="clear_command()">CLEAR</button>
<hr>
<h2>Command Builder</h2>
<h3>Dagah (Shevirah Phishing) Usage:</h3>
<h4>Required Command Line Options:</h4>
<div class="parameter_group">
  <div class="parameter">-M: <input type="radio" name="radio_M" id="M_app" value="app" >app <input type="radio" id="M_usb" name="radio_M" value="usb" > usb (type of attached mobile modem)</div>
  <div class="parameter">-n: <input type="text" id="n_phone"> phone number of modem</div>
  <div class="parameter">-u: <input type="text" id="u_url"> url on webserver where modem checks in</div>
  <div class="parameter">-k: <input type="text" id="k_key"> key to control modem</div>
  <div class="parameter"><button onclick="apply_M()">apply</button></div>
</div>
<br />
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
</body>
</html>
