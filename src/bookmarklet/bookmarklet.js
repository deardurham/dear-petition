const POST_URL =
  import.meta.env.MODE === 'development'
    ? 'http://localhost:8000'
    : 'https://www.durhamexpunction.org';
import { minify } from 'terser';

export const generateBookmarklet = async (username) =>
  (
    await minify(
      `
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
    
    form.appendChild(username_input);
    form.appendChild(textarea);
    iframe.appendChild(form);
    
    document.body.appendChild(iframe);
    
    form.submit();    
`,
      { mangle: false },
    )
  ).code;
