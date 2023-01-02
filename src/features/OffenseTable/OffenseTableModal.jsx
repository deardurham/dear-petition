import React, { useEffect, useState } from 'react';
import { usePetitionQuery, useRecalculatePetitionsMutation } from '../../service/api';
import StyledDialog from '../../components/elements/Modal/Dialog';
import OffenseTable from './OffenseTable';
import { Button } from '../../components/elements/Button';
import { Spinner } from '../../components/elements/Spinner';
import { Tooltip } from '../../components/elements/Tooltip/Tooltip';
import { DISABLED, POSITIVE } from '../../components/elements/Button/Button';

const OffenseTableModal = ({ isOpen, onClose, petitionId }) => (
  <StyledDialog isOpen={isOpen} onClose={() => onClose()}>
    <ModalWrapper petitionId={petitionId}>
      <ModalContent petitionId={petitionId} onClose={onClose} />
    </ModalWrapper>
  </StyledDialog>
);

const ModalWrapper = ({ children, petitionId }) => {
  const { isLoading } = usePetitionQuery({ petitionId });
  if (isLoading) {
    return (
      <div className="w-[900px] h-[500px] p-10 flex flex-col items-center justify-center gap-8">
        <Spinner size="2xl" />
      </div>
    );
  }
  return <div className="w-[900px] h-[500px] p-10 flex flex-col gap-8">{children}</div>;
};

const ModalContent = ({ petitionId, onClose }) => {
  const { data: petition } = usePetitionQuery({ petitionId });
  const [isModified, setIsModified] = useState(false);
  const [selectedRows, setSelectedRows] = useState(petition?.active_records ?? []);

  useEffect(() => {
    setSelectedRows(petition?.active_records);
  }, [petition?.active_records]);

  const [recalculatePetitions] = useRecalculatePetitionsMutation();
  if (!petition) {
    return null;
  }
  const { offense_records: offenseRecords } = petition;

  const onSelect = (offenseRecordId) => {
    setSelectedRows((prevSelectedRows) => {
      const newArray = [...prevSelectedRows];
      const selectedRowIndex = newArray.findIndex(
        (selectedRowId) => selectedRowId === offenseRecordId
      );

      // de-select row id if already in list
      if (selectedRowIndex >= 0) {
        newArray.splice(selectedRowIndex, 1);
        return newArray;
      }

      // otherwise, add id
      newArray.push(offenseRecordId);
      return newArray;
    });
    setIsModified(true);
  };

  const onRecalculatePetitions = async () => {
    try {
      await recalculatePetitions({ petitionId, offenseRecordIds: selectedRows }).unwrap();
      setIsModified(false);
    } catch (_e) {
      // no-op
    }
  };

  const petitionerDOB = offenseRecords?.find((record) => !!record?.dob)?.dob;

  return (
    <>
      <h3>View / Modify Offenses</h3>
      <p className="text-[1.6rem]">
        Please select or de-select offenses here if you wish to include or exclude them from the
        petition.
      </p>
      {petitionerDOB && (
        <p className="flex gap-2">
          <b>Petitioner DOB:</b>
          <span>{petitionerDOB}</span>
        </p>
      )}
      <OffenseTable
        offenseRecords={offenseRecords}
        selectedRows={selectedRows}
        onSelect={onSelect}
        dob={new Date(petitionerDOB)}
      />
      <div className="self-center flex gap-8">
        <Button
          className="w-[15rem]"
          colorClass={isModified ? POSITIVE : DISABLED}
          onClick={() => onRecalculatePetitions()}
          title={!isModified && 'You must modify the selected offenses to update the the petition'}
          disabled={!isModified}
        >
          Update Petition
        </Button>
        <Button className="px-4" onClick={() => onClose()}>
          Close
        </Button>
      </div>
    </>
  );
};

export default OffenseTableModal;
