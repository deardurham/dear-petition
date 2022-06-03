import React, { useState } from 'react';
import { useForm } from 'react-hook-form';

import PageBase from './PageBase';
import { useAgenciesQuery, useCreateAgencyMutation } from '../../service/api';
import AgenciesTable from '../features/AgenciesTable/AgenciesTable';
import { Button } from '../elements/Button';
import FormInput from '../elements/Input/FormInput';
import FormTextArea from '../elements/Input/FormTextArea';
import StyledDialog from '../elements/Modal/Dialog';

const ADDRESS_SORT_FIELD = ['address1', 'address2'];

const getOrdering = ({ field, dir }) => {
  const sortDir = dir === 'asc' ? '-' : '';
  if (field === 'address') {
    return ADDRESS_SORT_FIELD.map((addressField) => `${sortDir}${addressField}`).join(',');
  }
  return `${sortDir}${field}`;
};

const CreateAgency = ({ onClose }) => {
  const [triggerCreate] = useCreateAgencyMutation();
  const { control, handleSubmit } = useForm({
    defaultValues: {
      name: '',
      address: '',
      city: '',
      zipcode: '',
    },
    reValidateMode: 'onSubmit',
  });
  const onSubmit = async (formData) => {
    console.log({ formData });
    const submitData = {};
    Object.keys(formData).forEach((field) => {
      if (field === 'address') {
        const [address1, address2] = formData.address.split('\n');
        submitData.address1 = address1.trim();
        submitData.address2 = address2 ? address2.trim() : '';
      } else {
        submitData[field] = formData[field];
      }
    });
    await triggerCreate({ data: submitData }).unwrap();
  };
  const onSubmitAndClose = async (data) => {
    try {
      await onSubmit(data);
      onClose();
    } catch (e) {
      // noop
      console.log('dont close');
    }
  };
  return (
    <div className="w-[550px] px-40 py-20 flex flex-col gap-8">
      <h3>Add New Arresting Agency</h3>
      <form className="flex flex-col gap-4">
        <FormInput
          label="Name"
          inputProps={{
            control,
            name: 'name',
            rules: { required: true },
          }}
        />
        <FormTextArea
          label="Address"
          rows={2}
          inputProps={{
            control,
            name: 'address',
            // Server should treat address1 as required
            rules: { validate: (value) => !!value?.trim() && !!value.split('\n')[0] },
          }}
        />
        <FormInput
          label="City"
          className="w-[200px]"
          inputProps={{
            control,
            name: 'city',
            rules: { required: true },
          }}
        />
        <FormInput
          label="Zipcode"
          className="w-[200px]"
          maxLength={5}
          inputProps={{
            control,
            name: 'zipcode',
            rules: {
              required: true,
              minLength: 5,
              validate: (value) => !Number.isNaN(+value),
            },
          }}
        />
      </form>
      <div className="flex flex-row gap-4 justify-center">
        <Button type="submit" onClick={handleSubmit(onSubmitAndClose)}>
          Save
        </Button>
        <Button colorClass="neutral" onClick={() => onClose()}>
          Cancel
        </Button>
      </div>
    </div>
  );
};

const AgenciesPage = () => {
  const [sortBy, setSortBy] = useState({ field: 'name', dir: 'dsc' });
  const [showCreateModal, setShowCreateModal] = useState(false);
  const onSortBy = (field, dir) => {
    setSortBy({ field, dir });
  };
  const { data } = useAgenciesQuery({ params: { ordering: getOrdering(sortBy) } });
  return (
    <PageBase>
      <div className="flex flex-col gap-4">
        <h2>Arresting Agencies</h2>
        <div className="flex mb-4">
          <Button
            className="font-semibold px-2 py-1"
            colorClass="neutral"
            onClick={() => setShowCreateModal(true)}
          >
            Add New Agency +
          </Button>
          <StyledDialog isOpen={showCreateModal} onClose={() => setShowCreateModal(false)}>
            <CreateAgency onClose={() => setShowCreateModal(false)} />
          </StyledDialog>
        </div>
        <AgenciesTable agencies={data?.results ?? []} sortBy={sortBy} onSortBy={onSortBy} />
      </div>
    </PageBase>
  );
};

export default AgenciesPage;
