export const getErrorList = (validationObject) => {
  const errorEntries = Object.entries(validationObject);
  if (errorEntries.length === 0) {
    return [];
  }
  return errorEntries.map(
    ([key, errorList]) => `${key.charAt(0).toLocaleUpperCase()}${key.slice(1)}: ${errorList.join(' ')}`,
  );
};

export const hasValidationsErrors = (validationObject) => Object.keys(validationObject).length > 0;
