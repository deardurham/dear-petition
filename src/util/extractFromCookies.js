export default function extractFromCookies(type) {
  const cookies = document.cookie.split(';');
  return cookies.find((cookie) => cookie.trim().startsWith(`${type}=`));
}
