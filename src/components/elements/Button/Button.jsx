import PropTypes from 'prop-types';
import styled from 'styled-components';
import keyAndAmbientShadows from '../../../styles/shadows';
import { fontPrimary } from '../../../styles/fonts';

export const Button = ({ className, children, colorClass, ref, onClick, disabled }) => {
  const buttonColor = !disabled ? mapTypeToStartingState(colorClass) : mapTypeToStartingState(DISABLED);
  // renaming className for clarity
  const parentStyles = className;

  return (
    <button
      ref={ref}
      onClick={onClick}
      disabled={disabled}
      className={`cursor-pointer rounded-[3px] p-[0.5rem] outline-none
              text-[length:inherit] font-[${fontPrimary}]
              shadow-[0_4px_6px_-1px_rgb(0_0_0/0.1),0_2px_4px_-2px_rgb(0_0_0/0.1)]
              ${parentStyles} ${buttonColor}`}
    >
      {children}
    </button>
  );
};

export const CloseButton = styled(Button)`
  padding: 0 0.25rem;
  border-radius: 0;
  transition: none;
  transform: none;
  font-size: 1.25rem;
  ${keyAndAmbientShadows.dp1};

  &:hover {
    transform: none;
    ${keyAndAmbientShadows.dp1};
  }

  &:active {
    transform: none;
  }
`;

export const POSITIVE = 'positive';
export const CAUTION = 'caution';
export const NEUTRAL = 'neutral';
export const DISABLED = 'disabled';

function mapTypeToStartingState(colorClass) {
  switch (colorClass) {
    case POSITIVE:
      return positive;
    case CAUTION:
      return caution;
    case NEUTRAL:
      return neutral;
    case DISABLED:
      return disabled;
    default:
      return positive;
  }
}

// const disabled = css`
//   background: ${greyScale(7.25)};
//   border: 1px solid ${greyScale(7.25)};
//   color: ${colorWhite};
// `;

// note: had trouble finding a way to get tailwind to accept the hsl color we had been using,
// so added an equivalent color in tailwind config as gray-disabled
const disabled = `bg-gray-disabled border-[1px] border-solid border-gray-disabled text-white`;

const positive = 'bg-primary border-[1px] border-solid border-primary text-white';

const caution = 'bg-red border-[1px] border-solid border-red text-white';

const neutral = 'bg-white border-[1px] border-solid border-primary text-primary';

Button.propTypes = {
  /** Reflects the state of the button */
  colorClass: PropTypes.oneOf([POSITIVE, CAUTION, NEUTRAL, DISABLED]),
  /** What happens when the button is clicked */
  onClick: PropTypes.func.isRequired,
};

Button.defaultProps = {
  colorClass: POSITIVE,
};
