import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useDeleteAgencyMutation, useUpdateAgencyMutation } from '../../service/api';
import {
  EditableRow,
  HeaderCell,
  SortableHeader,
  Table,
  TableBody,
  TableCell,
  TableHeader,
} from '../../components/elements/Table';
import { Button } from '../../components/elements/Button';
import FormInput from '../../components/elements/Input/FormInput';
import FormTextArea from '../../components/elements/Input/FormTextArea';
import StyledDialog from '../../components/elements/Modal/Dialog';

const getFormattedAddress = (address1, address2) =>
  address2 ? `${address1}\n${address2}` : address1;

const AgencyInputRow = ({ agencyData, onStopEditing }) => {
  const [triggerUpdate, { error }] = useUpdateAgencyMutation();
  const { data: errorData } = error ?? {};

  const { control, handleSubmit, formState } = useForm({
    defaultValues: {
      name: agencyData.name,
      address: getFormattedAddress(agencyData.address1, agencyData.address2),
      city: agencyData.city,
      zipcode: agencyData.zipcode,
    },
    reValidateMode: 'onSubmit',
  });
  const { dirtyFields, errors: formErrors } = formState;
  const hasErrors = error || Object.keys(formErrors).length > 0;

  const onSubmit = async (formData) => {
    const modifiedFields = Object.keys(dirtyFields);
    if (modifiedFields.length === 0) {
      onStopEditing();
      return;
    }
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
    try {
      await triggerUpdate({ id: agencyData.pk, data: submitData }).unwrap();
      onStopEditing();
    } catch (e) {
      // noop
    }
  };

  return (
    <>
      <TableCell>
        <FormInput
          className="w-full"
          inputProps={{
            control,
            name: 'name',
            rules: {
              required: true,
            },
          }}
          errors={errorData?.name && [errorData.name]}
        />
      </TableCell>
      <TableCell>
        <FormTextArea
          rows={2}
          inputProps={{
            control,
            name: 'address',
            rules: {
              required: true,
              validate: (value) => !!value?.trim() && !!value.split('\n')[0],
            },
          }}
          errors={
            (errorData?.address1 || errorData?.address2) && [
              ...(errorData?.address1 ?? []),
              ...(errorData?.address2 ?? []),
            ]
          }
        />
      </TableCell>
      <TableCell>
        <FormInput
          className="w-fit"
          inputProps={{
            control,
            name: 'city',
            rules: {
              required: true,
            },
          }}
          errors={errorData?.city}
        />
      </TableCell>
      <TableCell>
        <FormInput
          className="w-full"
          maxLength={5}
          inputProps={{
            control,
            name: 'zipcode',
            rules: {
              minLength: 5,
              required: true,
              validate: (value) => !Number.isNaN(+value),
            },
          }}
          errors={errorData?.zipcode}
        />
      </TableCell>
      <TableCell className="flex flex-col gap-4">
        <div className="flex gap-2">
          <Button type="button" colorClass="neutral" className="h-fit" onClick={onStopEditing}>
            Cancel
          </Button>
          <Button type="button" className="h-fit" onClick={handleSubmit(onSubmit)}>
            Save
          </Button>
        </div>
        {hasErrors && <span className="text-red whitespace-normal">Error: Unable to submit!</span>}
      </TableCell>
    </>
  );
};

const AgenciesTable = ({ agencies, sortBy, onSortBy }) => {
  const [editingId, setEditingId] = useState(null);
  const [deleteModalId, setDeleteModalId] = useState(null);
  const [triggerDelete] = useDeleteAgencyMutation();
  const onDelete = (agency) => {
    triggerDelete({ id: agency.pk });
    onCloseDeleteModal();
  };
  const onCloseDeleteModal = () => {
    setDeleteModalId(null);
  };
  return (
    <Table className="grid-cols-[6fr_4fr_3fr_2fr_3fr]">
      <TableHeader sortedHeader={sortBy.field} sortDir={sortBy.dir} onSelectColumn={onSortBy}>
        <SortableHeader field="name">Name</SortableHeader>
        <SortableHeader field="address">Address</SortableHeader>
        <SortableHeader field="city">City</SortableHeader>
        <SortableHeader field="zipcode">Zip</SortableHeader>
        <HeaderCell>Actions</HeaderCell>
      </TableHeader>
      <TableBody>
        {agencies.map((agencyData) => (
          <EditableRow
            key={agencyData.pk}
            isEditing={editingId === agencyData.pk}
            editingRow={
              <AgencyInputRow agencyData={agencyData} onStopEditing={() => setEditingId(null)} />
            }
          >
            <TableCell tooltip={agencyData.name}>{agencyData.name}</TableCell>
            <TableCell tooltip={agencyData.formatted_address}>
              {agencyData.formatted_address}
            </TableCell>
            <TableCell>{agencyData.city}</TableCell>
            <TableCell>{agencyData.zipcode}</TableCell>
            <TableCell className="flex gap-2">
              <Button type="button" onClick={() => setEditingId(agencyData.pk)}>
                Edit
              </Button>
              <Button
                type="button"
                colorClass="caution"
                onClick={() => setDeleteModalId(agencyData.pk)}
              >
                Delete
              </Button>
              <StyledDialog
                isOpen={deleteModalId === agencyData.pk}
                onClose={() => onCloseDeleteModal()}
              >
                <div className="max-w-[600px] p-24 flex flex-col gap-8">
                  <p className="self-center text-3xl font-bold">WARNING</p>
                  <p className="text-[1.6rem] flex flex-wrap gap-x-2 gap-y-4">
                    <span>This action will PERMANENTLY delete the agency:</span>
                    <span className="font-semibold">{agencyData.name}</span>
                  </p>
                  <div className="self-end flex gap-4 text-lg">
                    <Button
                      type="button"
                      className="p-2"
                      colorClass="neutral"
                      onClick={() => onCloseDeleteModal()}
                    >
                      Cancel
                    </Button>
                    <Button
                      type="button"
                      className="p-2"
                      colorClass="caution"
                      onClick={() => onDelete(agencyData)}
                    >
                      Delete
                    </Button>
                  </div>
                </div>
              </StyledDialog>
            </TableCell>
          </EditableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default AgenciesTable;
