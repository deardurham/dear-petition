import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';
import { Tab } from '@headlessui/react';
import cx from 'classnames';
import { Link } from 'react-router-dom';
import PageBase from './PageBase';
import { useGetUserBatchesQuery } from '../../service/api';
import useAuth from '../../hooks/useAuth';
import { ExistingPetitions } from '../../features/ExistingPetitions';
import { NewPetition } from '../../features/NewPetition';
import { Spinner } from '../elements/Spinner';

export const Dashboard = () => {
  const { user } = useAuth();
  const { data, isLoading, isUninitialized } = useGetUserBatchesQuery({ user: user.pk });
  const hasExistingPetitions = data?.results?.length > 0;
  if (isLoading || isUninitialized) {
    return (
      <div className="h-screen w-full flex items-center justify-center">
        <Spinner size="2xl" />
      </div>
    );
  }
  return (
    <PageBase>
      <div className="flex flex-col gap-8">
        <span className="flex gap-3 items-center">
          <FontAwesomeIcon className="text-[18px] text-blue-primary" icon={faInfoCircle} />
          First time creating an expunction petition form?
          <Link to="/help">See the Help page for more information.</Link>
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
                  >
                    Existing Petitions
                  </button>
                )}
              </Tab>
            </div>
          </Tab.List>
          <Tab.Panels as="div">
            <Tab.Panel>
              <NewPetition />
            </Tab.Panel>
            <Tab.Panel>
              <ExistingPetitions />
            </Tab.Panel>
          </Tab.Panels>
        </Tab.Group>
      </div>
    </PageBase>
  );
};
