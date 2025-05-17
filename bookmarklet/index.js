const POST_URL = window.location.origin;
const PORTAL_URL = 'https://portal-nc.tylertech.cloud/Portal/';
const PORTAL_APP_URL = 'https://portal-nc.tylertech.cloud';
const PORTAL_APP_PATHNAME = '/app/RegisterOfActions/#/';

export function generateBookmarklet(username) {
  return `
  if (window.location.origin !== '${PORTAL_APP_URL}' && !window.location.pathname.startsWith('${PORTAL_APP_PATHNAME}')) {
    alert('Failed to import case. To use the Portal Importer, please navigate to ${PORTAL_URL} and click this bookmark while viewing a a case.');
    return;
  }

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

  var url_input = document.createElement('input');
  url_input.name = 'url';
  url_input.value = window.location.href;

  form.appendChild(username_input);
  form.appendChild(location_input);
  form.appendChild(textarea);
  form.appendChild(url_input);
  iframe.appendChild(form);
  
  document.body.appendChild(iframe);
  
  form.submit();

  alert("Submitted case summary to Expunction Tool");
  `;
}
