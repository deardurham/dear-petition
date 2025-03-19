import { useState, useRef } from 'react';

/**
 * Hook which creates state to track warning status for forms, and returns the warnings
 * state as well as a handler for updating a single field's warning, a handler for updating warnings for all fields,
 * and a function for registering new warning types.
 *
 * Initialize by getting warnings state and handlers from useFormWarnings(), then addWarningType() for each warning needed.
 *
 * Then use handleWarning(dobValue) or handleAllWarnings(formValues) on events
 * where you want warnings be re-checked, such as field value changes or form submission.
 *
 * @returns {{
 *   warnings: object,
 *   handleWarning: function(fieldName, value): void,
 *   handleAllWarnings: function(values): void,
 *   addWarningType: function(fieldName, condition, warningMsg): void
 * }}
 */
const useFormWarnings = () => {
  // state for storing current warnings state, which will be returned to the Component calling this hook
  const [warnings, setWarnings] = useState({});
  // object to store list of specifications for warnings for each field
  // e.g. {'fieldName': [{'condition': fn, 'warningMsg': 'Warning message here'}, ...]}
  const warningsSpecificationsByField = useRef({});

  /*
    Handlers use this function to add a warning to the list of warnings for fieldName
    */
  const addWarning = (fieldName, warningMsg) => {
    // only add the warning if not a duplicate
    if (!warnings[fieldName] || !warnings[fieldName].includes(warningMsg)) {
      setWarnings((prev) => ({ ...prev, [fieldName]: [...(prev[fieldName] ?? []), warningMsg] }));
    }
  };

  /*
    Handlers use this function to delete a warning from the list of warnings 
    if it should no longer be displayed
    */
  const clearWarning = (fieldName, warningMsg) => {
    // remove the warning if it is in the list for fieldName, otherwise do nothing
    if (warnings[fieldName] && warnings[fieldName].includes(warningMsg)) {
      setWarnings((prev) => ({ ...prev, [fieldName]: prev[fieldName].filter((msg) => msg != warningMsg) }));
    }
  };

  /*
    Use this function to check if a certain field needs warnings displayed based on its current value.
    Updates the warnings state to true for that field if warning should be displayed, false otherwise.
    */
  const handleWarning = (fieldName, value) => {
    const warningSpecifications = warningsSpecificationsByField.current[fieldName];

    warningSpecifications.forEach((warningSpec) => {
      const warningMsg = warningSpec.warningMsg;

      if (warningSpec.condition(value)) {
        addWarning(fieldName, warningMsg);
      } else {
        clearWarning(fieldName, warningMsg);
      }
    });
  };

  /*
    Use this function to check all fields of a form to see if any warnings need to be displayed based on
    form's current values. Updates the warnings state for all fields using the 
    handleWarning(fieldName, value) function.
    */
  const handleAllWarnings = (values) => {
    Object.keys(warningsSpecificationsByField.current).forEach((fieldName) => {
      handleWarning(fieldName, values[fieldName]);
    });
  };

  /**
   * Register a new type of warning message for the specified field during initialization.
   * Stores the conditions to check for this field, and the warning message to display if
   * these conditions are met, so that this info can be used by the handler functions later on.
   * Note that it is possible for more than one warning type to be associated with a single field.
   * @param {string} fieldName - field warning will apply to
   * @param {function} condition - boolean function that returns true if warning should display, false otherwise
   * @param {string} warningMsg - the warning message associated with this type of warning
   */
  const addWarningType = (fieldName, condition, warningMsg) => {
    const warningSpecification = { condition: condition, warningMsg: warningMsg };

    // if no array for this fieldName yet in the ref, initialize an empty array for it
    if (!(fieldName in warningsSpecificationsByField.current)) {
      warningsSpecificationsByField.current[fieldName] = [];
    }

    const currentWarningSpecs = warningsSpecificationsByField.current[fieldName];

    // add the new warning spec unless a spec with same warningMsg already exists
    if (!currentWarningSpecs.some((spec) => spec.warningMsg === warningMsg)) {
      currentWarningSpecs.push(warningSpecification);
    }
  };

  return { warnings, handleWarning, handleAllWarnings, addWarningType };
};

export default useFormWarnings;
