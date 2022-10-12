import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { Menu } from '@headlessui/react';
import { Button, DISABLED, NEUTRAL, POSITIVE } from './Button';

const DropdownButtonElement = ({ label, setIsMenuOpen, disabled }) => (
  <Button colorClass={disabled ? DISABLED : undefined} className="flex items-center">
    <span className="pr-4 border-r">{label}</span>
    <div className="pl-2">
      <FontAwesomeIcon icon={faChevronDown} onMouseOver={() => setIsMenuOpen(true)} />
    </div>
  </Button>
);

export const DropdownButton = ({ choices, className, defaultSelection, disabled }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  if (!choices || choices.length === 0) {
    throw new Error('Must provide list of choices');
  }

  const defaultIndex = defaultSelection
    ? choices.findIndex(({ label }) => label === defaultSelection)
    : 0;

  if (defaultIndex < 0) {
    throw new Error('Default selection does not exist in choices list');
  }

  const { label: defaultLabel, onClick: defaultOnClick } = choices[defaultIndex];
  const restChoices = choices.slice();
  restChoices.splice(defaultIndex, 1);
  return (
    <Menu as="div" className={className} onMouseLeave={() => setIsMenuOpen(false)}>
      <Menu.Button onClick={() => defaultOnClick()} disabled={disabled}>
        <DropdownButtonElement
          label={defaultLabel}
          disabled={disabled}
          setIsMenuOpen={setIsMenuOpen}
        />
      </Menu.Button>
      <Menu.Items static>
        {!disabled && isMenuOpen && (
          <div className="flex flex-col py-1">
            {restChoices.map(({ label: itemLabel, onClick }) => (
              <Menu.Item key={itemLabel}>
                {({ active }) => (
                  <Button colorClass={active ? POSITIVE : NEUTRAL} onClick={onClick}>
                    {itemLabel}
                  </Button>
                )}
              </Menu.Item>
            ))}
          </div>
        )}
      </Menu.Items>
    </Menu>
  );
};
