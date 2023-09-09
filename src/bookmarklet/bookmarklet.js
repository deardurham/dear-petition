var username = prompt("Enter your Durham Expunction username");
var html = document.documentElement.innerHTML;
var loaded = 0;

var iframe = document.createElement('iframe');
iframe.name = 'bookmarklet-' + Math.floor((Math.random() * 10000) + 1);
iframe.style.display = 'none';

iframe.onload = function () {
    if (++loaded == 1) {
        return;
    }


    document.body.removeChild(iframe);
};

var form = document.createElement('form');
form.method = "POST";
form.action = "https://27a9-99-92-50-211.ngrok-free.app/portal/bookmarklet/?nocache=" + Math.random();
form.target = iframe.name;

var username_input = document.createElement('input');
username_input.name = 'user';
username_input.value = username;

var textarea = document.createElement('textarea');
textarea.name = 'source';
textarea.value = html;

form.appendChild(username_input);
form.appendChild(textarea);
iframe.appendChild(form);

document.body.appendChild(iframe);

form.submit();
