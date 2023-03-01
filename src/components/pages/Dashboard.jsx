import React from 'react';
import { Tab } from '@headlessui/react';
import cx from 'classnames';
import { Link } from 'react-router-dom';
import PageBase from './PageBase';
import useAuth from '../../hooks/useAuth';
import { ExistingPetitions } from '../../features/ExistingPetitions';
import { NewPetition } from '../../features/NewPetition';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';

/*
  Enhance Help Page
    - Step by step instructions on generating petion
    - Steps on how to send CIPRS documents to expunction tool
      - Allow user to email themselves the instructions?
  "View" vs "View Petitions"
      probably an issue with using table format vs something like cards
      seems to be a width constraint issue
*/

export const Dashboard = () => {
  const { user } = useAuth();
  const hasExistingPetitions = false;
  return (
    <PageBase>
      <div className="flex flex-col gap-4">
        <span className="flex gap-2 items-center">
          <FontAwesomeIcon className="text-[18px] text-blue-primary" icon={faInfoCircle} />
          First time creating an expunction petition form?
          <Link to="/help">Click here for instructions</Link>
        </span>
        <Tab.Group defaultIndex={hasExistingPetitions ? 1 : 0}>
          <Tab.List className="flex">
            <div className="flex bg-blue-primary p-2 gap-1 rounded-md text-white font-bold">
              <Tab as="div">
                {({ selected }) => (
                  <button
                    type="button"
                    className={cx(
                      'px-4 py-2 rounded-md border-0',
                      selected ? 'bg-white text-blue-primary' : 'bg-inherit hover:bg-white/[0.25]'
                    )}
                    colorClass={selected ? 'neutral' : 'positive'}
                  >
                    New Petition
                  </button>
                )}
              </Tab>
              <Tab as="div">
                {({ selected }) => (
                  <button
                    type="button"
                    className={cx(
                      'px-4 py-2 rounded-md border-0',
                      selected ? 'bg-white text-blue-primary' : 'bg-inherit hover:bg-white/[0.25]'
                    )}
                    colorClass={selected ? 'neutral' : 'positive'}
                  >
                    Existing Petition
                  </button>
                )}
              </Tab>
            </div>
          </Tab.List>
          <Tab.Panels as="div" className="mt-4">
            <Tab.Panel>
              <NewPetition />
            </Tab.Panel>
            <Tab.Panel>
              <ExistingPetitions />
            </Tab.Panel>
          </Tab.Panels>
        </Tab.Group>
      </div>
      <div className="flex flex-col">
        <h3 className="mt-12">Upload CIPRS Record via Court Email System</h3>
        <div className="mt-4 [&_li]:text-[17px]">
          <ul className="list-disc list-inside flex flex-col gap-2">
            <li>
              You may send an email with CIPRS record attachments to {user.username}
              @inbox.durhamexpunction.org to view and generate documents.
            </li>
            <li>
              You may optionally add a label for the CIPRS records by adding a `+`. For example:{' '}
              {user.username}+JohnDoeDurhamRecords@inbox.durhamexpunction.org
            </li>
          </ul>
        </div>
      </div>
    </PageBase>
  );
};
