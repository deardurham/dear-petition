import { AnimatePresence, motion } from 'framer-motion';

export const DobWarning = ({ enabled, expectedValue }) => {
  // parsing date as UTC here to prevent unexpected changes of date value from using locale time
  const dob = new Date(expectedValue + 'Z');
  const expectedDobString = dob.toLocaleDateString('en-US', {
    timeZone: 'UTC',
    month: '2-digit',
    day: '2-digit',
    year: 'numeric',
  });

  return (
    <>
      <AnimatePresence initial={false}>
        {enabled && (
          <motion.div
            className="mt-0.5 mb-2"
            initial={{ opacity: 0, y: -25 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 25 }}
            key="DobWarning"
          >
            <p className="text-amber-700 text-sm lg:text-base whitespace-normal">
              Note: Date of birth entered does not match date found in CIPRS form pdf: {expectedDobString}. Petitioner
              Information date of birth will be used.
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default DobWarning;
