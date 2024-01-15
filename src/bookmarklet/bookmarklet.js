const POST_URL = window.location.origin;

export function generateBookmarklet(username) {
  return `
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
  form.action = '${POST_URL}/portal/bookmarklet/';
  form.target = iframe.name;
  
  var username_input = document.createElement('input');
  username_input.name = 'user';
  username_input.value = '${username}';
  
  var textarea = document.createElement('textarea');
  textarea.name = 'source';
  textarea.value = html;
  
  var location_input = document.createElement('input');
  location_input.name = 'location';
  location_input.value = window.location;

  form.appendChild(username_input);
  form.appendChild(location_input);
  form.appendChild(textarea);
  iframe.appendChild(form);
  
  document.body.appendChild(iframe);
  
  form.submit();

  alert("Successfully submitted case summary to Expunction Tool");
  `
}
