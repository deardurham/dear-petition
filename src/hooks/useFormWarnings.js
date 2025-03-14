import { useState } from 'react';

const useFormWarnings = (warningCheckers, warningMsgs) => {
  /**
   * This is a hook to create state to track warnings state for forms, and returns the warnings
   * state as well as handlers for updating all warnings and updating a single field's warning.
   *
   * @param {object} warningCheckers - object that maps array of warning checker functions for each field
   * e.g. {'dob': [fn, fn2], 'otherField': [otherFieldFn]}, where fn is a function that
   * returns true if a warning should be displayed, false otherwise (e.g. fn = (dob) => { dob != expectedDob })
   * @param {object} warningMsgs - object that maps array of warning message strings for each field
   * e.g. { 'dob': ['Warning: DOB does not match expected value.', 'other type of warning message for this field'],
   *                  'otherField': ['Warning message for other field.']}
   * Note that array indices must match between corresponding warningChecker and warningMsg
   * @returns {object} object containing:
   * reference to the warnings state, a single-field warning handler, and an all-fields warning handler
   */

  const [warnings, setWarnings] = useState({});
  // note: reworked addWarning so that it can store more than one non-duplicate warning per field
  const addWarning = (key, warningMsg) => {
    // only add the warning if not a duplicate
    if (!warnings[key] || !warnings[key].includes(warningMsg)) {
      setWarnings((prev) => ({ ...prev, [key]: [...(prev[key] ?? []), warningMsg] }));
    }
  };
  // note: reworked clearWarning so that it can remove warningMsg from a list of warningMsgs for the field
  const clearWarning = (key, warningMsg) => {
    if (warnings[key] && warnings[key].includes(warningMsg)) {
      setWarnings((prev) => ({ ...prev, [key]: prev[key].filter((msg) => msg != warningMsg) }));
    }
  };

  const handleWarning = (fieldName, value) => {
    /*
        Use this function to check if a certain field needs warnings displayed based on its current value.
        Updates the warnings state to true for that field if warning should be displayed, false otherwise.
        */
    const warningCheckersForField = warningCheckers[fieldName];
    const warningMsgsForField = warningMsgs[fieldName];

    // since there could potentially be more than one possible warning type per field,
    // loop through the list of warningCheckers and warningMsgs and check for each warning type
    for (let i = 0; i < warningCheckersForField.length; i++) {
      const checkForWarning = warningCheckersForField[i];
      const warningMsg = warningMsgsForField[i];

      if (checkForWarning(value)) {
        addWarning(fieldName, warningMsg);
      } else {
        clearWarning(fieldName, warningMsg);
      }
    }
  };

  const handleAllWarnings = (values) => {
    /*
        Use this function to check all fields of a form to see if any warnings need to be displayed based on
        forms current values. Updates the warnings state for all fields using the 
        handleWarning(fieldName, value) function.
        */
    Object.keys(warningCheckers).forEach((fieldName) => {
      handleWarning(fieldName, values[fieldName]);
    });
  };

  return { warnings, handleWarning, handleAllWarnings };
};

export default useFormWarnings;
