import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCog, faList, faPlus } from '@fortawesome/free-solid-svg-icons';

import PageBase from './PageBase';
import { useAgenciesQuery } from '../../service/api';
import AgenciesTable from '../features/AgenciesManagement/AgenciesTable';
import CreateAgency from '../features/AgenciesManagement/CreateAgency';
import { Button } from '../elements/Button';
import StyledDialog from '../elements/Modal/Dialog';
import Select from '../elements/Input/Select';
import { calculateNumberOfPages } from '../elements/Table';

const DEFAULT_NUM_AGENCIES = 10;
const NUM_AGENCIES_OPTIONS = [10, 25, 50].map((value) => ({ value, label: value }));
const MODALS = {
  CREATE_AGENCY: 'CREATE_AGENCY',
  DISPLAY_SETTINGS: 'DISPLAY_SETTINGS',
};

const ActionsRow = ({ agenciesCount, numDisplayAgencies, onSetPageNumber, onSetNumAgencies }) => {
  const [selectedModal, setSelectedModal] = useState('');
  const onCloseModal = () => setSelectedModal('');
  const test = calculateNumberOfPages(agenciesCount, numDisplayAgencies);
  console.log({ test });
  return (
    <div className="flex gap-8 mb-1">
      <>
        <Button
          className="flex gap-2 font-semibold px-2 py-1"
          colorClass="neutral"
          onClick={() => setSelectedModal(MODALS.CREATE_AGENCY)}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add New Agency
        </Button>
        <StyledDialog isOpen={selectedModal === MODALS.CREATE_AGENCY} onClose={onCloseModal}>
          <CreateAgency onClose={onCloseModal} />
        </StyledDialog>
      </>

      <>
        <Button
          className="flex gap-2 font-semibold px-2 py-1"
          colorClass="neutral"
          onClick={() => setSelectedModal(MODALS.DISPLAY_SETTINGS)}
        >
          <FontAwesomeIcon icon={faCog} />
          Display Settings
        </Button>
        <StyledDialog isOpen={selectedModal === MODALS.DISPLAY_SETTINGS} onClose={onCloseModal}>
          <div className="px-24 py-16 flex flex-col gap-8">
            <h2 className="self-center">Settings</h2>
            <Select
              label="# of agencies to display"
              value={{ value: numDisplayAgencies, label: numDisplayAgencies }}
              options={NUM_AGENCIES_OPTIONS}
              onChange={({ value }) => onSetNumAgencies(value)}
            />
            <Button className="self-center w-fit px-6 py-2" onClick={() => onCloseModal()}>
              Close
            </Button>
          </div>
        </StyledDialog>
      </>

      <>
        <Button
          className="flex gap-2 font-semibold px-2 py-1"
          colorClass="neutral"
          onClick={() => setSelectedModal('')}
        >
          <FontAwesomeIcon icon={faList} />
          Filters
        </Button>
      </>

      <div className="flex-1 flex items-end justify-end gap-4">
        {[...Array(test).keys()].map((pageIndex) => {
          const pageNum = pageIndex + 1;
          return (
            <button key={pageNum} type="button" onClick={() => onSetPageNumber(pageNum)}>
              {pageNum}
            </button>
          );
        })}
      </div>
    </div>
  );
};

const ADDRESS_SORT_FIELD = ['address1', 'address2'];

const getOrdering = ({ field, dir }) => {
  const sortDir = dir === 'asc' ? '-' : '';
  if (field === 'address') {
    return ADDRESS_SORT_FIELD.map((addressField) => `${sortDir}${addressField}`).join(',');
  }
  return `${sortDir}${field}`;
};

const getOffset = (pageNumber, numAgenciesPerPage) => (pageNumber - 1) * numAgenciesPerPage;

const AgenciesPage = () => {
  const [sortBy, setSortBy] = useState({ field: 'name', dir: 'dsc' });
  const [pageNumber, setPageNumber] = useState(1);
  const [numAgenciesPerPage, setNumAgenciesPerPage] = useState(DEFAULT_NUM_AGENCIES);
  const onSortBy = (field, dir) => {
    setSortBy({ field, dir });
  };
  const { data } = useAgenciesQuery({
    params: {
      ordering: getOrdering(sortBy),
      offset: getOffset(pageNumber, numAgenciesPerPage),
      limit: numAgenciesPerPage,
    },
  });
  return (
    <PageBase>
      <div className="flex flex-col gap-4">
        <h2>Arresting Agencies</h2>
        <ActionsRow
          onSetPageNumber={(nextNumber) => setPageNumber(nextNumber)}
          agenciesCount={data?.count ?? 0}
          numDisplayAgencies={numAgenciesPerPage}
          onSetNumAgencies={(n) => setNumAgenciesPerPage(n)}
        />
        <AgenciesTable agencies={data?.results ?? []} sortBy={sortBy} onSortBy={onSortBy} />
      </div>
    </PageBase>
  );
};

export default AgenciesPage;
