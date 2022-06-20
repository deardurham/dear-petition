import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCog, faList, faPlus } from '@fortawesome/free-solid-svg-icons';

import PageBase from './PageBase';
import { useAgenciesQuery } from '../../service/api';
import AgenciesTable from '../../features/AgenciesManagement/AgenciesTable';
import { CreateAgencyModal } from '../../features/AgenciesManagement/CreateAgency';
import { ModalButton } from '../elements/Button';
import Select from '../elements/Input/Select';
import SearchInput from '../elements/ManagementTable/SearchInput';
import { calculateNumberOfPages, LegacyPageSelection } from '../elements/Table';
import { DisplaySettingsModal } from '../elements/ManagementTable/DisplaySettings';
import { AgencyFiltersModal } from '../../features/AgenciesManagement/AgencyFilters';

const DEFAULT_NUM_AGENCIES = 10;
const NUM_AGENCIES_OPTIONS = [10, 25, 50].map((value) => ({ value, label: value }));

const ADDRESS_SORT_FIELD = ['address1', 'address2'];

const getOrdering = ({ field, dir }) => {
  const sortDir = dir === 'asc' ? '-' : '';
  if (field === 'address') {
    return ADDRESS_SORT_FIELD.map((addressField) => `${sortDir}${addressField}`).join(',');
  }
  return `${sortDir}${field}`;
};

const getOffset = (pageNumber, numAgenciesPerPage) => (pageNumber - 1) * numAgenciesPerPage;

const getFilters = (filterSelections) =>
  Object.keys(filterSelections).map((key) => [`${key}__in`, filterSelections[key].join(',')]);

const AgenciesPage = () => {
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState({ field: 'name', dir: 'dsc' });
  const [pageNumber, setPageNumber] = useState(1);
  const [numAgenciesPerPage, setNumAgenciesPerPage] = useState(DEFAULT_NUM_AGENCIES);
  const [filterSelections, setFilterSelections] = useState({ city: [], zipcode: [] });
  const onSortBy = (field, dir) => {
    setSortBy({ field, dir });
  };
  const onFilter = (field, selections) => {
    setFilterSelections((prev) => ({ ...prev, [field]: selections }));
  };
  const { data } = useAgenciesQuery({
    queryString: new URLSearchParams([
      ['search', search],
      ['ordering', getOrdering(sortBy)],
      ['offset', getOffset(pageNumber, numAgenciesPerPage)],
      ['limit', numAgenciesPerPage],
      ...getFilters(filterSelections),
    ]).toString(),
  });
  return (
    <PageBase>
      <div className="flex flex-col gap-4">
        <h2>Arresting Agencies</h2>
        <div className="flex gap-6 mb-1">
          <ModalButton
            className="flex gap-2 font-semibold px-2 py-1"
            title={
              <span>
                <FontAwesomeIcon icon={faPlus} /> Add New Agency
              </span>
            }
          >
            <CreateAgencyModal />
          </ModalButton>
          <ModalButton
            className="flex gap-2 font-semibold px-2 py-1"
            title={
              <span>
                <FontAwesomeIcon icon={faCog} /> Display Settings
              </span>
            }
          >
            <DisplaySettingsModal>
              <Select
                label="# of agencies to display"
                value={{ value: numAgenciesPerPage, label: numAgenciesPerPage }}
                options={NUM_AGENCIES_OPTIONS}
                onChange={({ value }) => setNumAgenciesPerPage(value)}
              />
            </DisplaySettingsModal>
          </ModalButton>
          <ModalButton
            className="flex gap-2 font-semibold px-2 py-1"
            title={
              <span>
                <FontAwesomeIcon icon={faList} /> Filters
              </span>
            }
          >
            <AgencyFiltersModal onFilter={onFilter} filterSelections={filterSelections} />
          </ModalButton>
          <SearchInput
            className="w-[300px]"
            onSearch={(value) => setSearch(value)}
            placeholder="Search agency name..."
          />
          <div className="flex-1 flex items-end justify-end gap-4">
            <LegacyPageSelection
              currentPage={pageNumber}
              numPages={calculateNumberOfPages(data?.count ?? 0, numAgenciesPerPage)}
              onPageSelect={(pageNum) => setPageNumber(pageNum)}
            />
          </div>
        </div>
        <AgenciesTable agencies={data?.results ?? []} sortBy={sortBy} onSortBy={onSortBy} />
      </div>
    </PageBase>
  );
};

export default AgenciesPage;
