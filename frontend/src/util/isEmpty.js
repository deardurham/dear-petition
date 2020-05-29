export default function isEmpty(obj) {
  if (!obj) return;
  if (Array.isArray(obj) && obj.length === 0) return true;
  if (Object.keys(obj).length === 0) return true;
  let innerEmpty = true;
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      if (Array.isArray(obj[key])) {
        if (obj[key].length > 0) {
          innerEmpty = false;
          break;
        }
      }

      if (
        !Array.isArray(obj[key]) &&
        obj[key] !== null &&
        obj[key] !== undefined &&
        obj[key] !== ''
      ) {
        innerEmpty = false;
        break;
      }
    }
  }
  return innerEmpty;
}
