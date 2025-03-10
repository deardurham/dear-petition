import { useRef, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPencilAlt, faPlus, faSave, faTimes } from '@fortawesome/free-solid-svg-icons';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import Input from '../../../elements/Input/Input';
import AddressInput from './AddressInput';
import AutocompleteInput from '../../../elements/Input/AutocompleteInput';
import {
  useLazySearchClientsQuery,
  useAssignClientToBatchMutation,
  useUpdateClientMutation,
} from '../../../../service/api';
import Button, { ModalButton } from '../../../elements/Button';
import { useModalContext } from '../../../elements/Button/ModalButton';
import { CreateClient } from '../../../../features/CreateClient';

const TextInput = styled(Input)`
  input {
    padding: 0.9rem;
    width: 100%;
    background-color: ${(props) => props.disabled && 'hsl(0, 0%, 95%)'};
  }
  &:not(:last-child) {
    margin-bottom: 1rem;
  }
`;

const dobWarningMsg = `Warning: Date of birth entered does not match CIPRS record pdf.
  Petitioner Information date of birth will be used.`;

export const CreateClientModal = ({ onCreate, handleWarnings, handleDobWarning, warnings }) => {
  const modalElement = useRef();
  const { closeModal } = useModalContext();
  return (
    <div className="w-[550px] px-40 py-20" ref={modalElement}>
      <CreateClient
        onClose={closeModal}
        category="client"
        onSubmitSuccess={(submitData) => onCreate(submitData)}
        handleWarnings={handleWarnings}
        handleDobWarning={handleDobWarning}
        warnings={warnings}
      />
    </div>
  );
};

const DEFAULT_ADDRESS_STATE = {
  name: '',
  address: '',
  city: '',
  zipcode: '',
  state: { label: 'NC', value: 'NC' },
};

const getPetitionerData = (petitioner) => {
  if (!petitioner) {
    return DEFAULT_ADDRESS_STATE;
  }
  const { pk: _pk, ...clientData } = petitioner;
  return clientData;
};

export default function PetitionerInput({ petitioner, batchDob, errors, onClearError }) {
  const { batchId } = useParams();
  const [triggerSuggestionsFetch] = useLazySearchClientsQuery();
  const [triggerAssignClientToBatch] = useAssignClientToBatchMutation();
  const [triggerClientUpdate] = useUpdateClientMutation();
  const [isEditing, setIsEditing] = useState(false);
  const [editErrors, setEditErrors] = useState({});
  const [editWarnings, setEditWarnings] = useState({});

  const [petitionerData, setPetitionerData] = useState(getPetitionerData(petitioner));
  const { name, dob, ...address } = petitionerData;

  const addError = (key, error) => setEditErrors((prev) => ({ ...prev, [key]: [error] }));
  const clearError = (key) => setEditErrors((prev) => ({ ...prev, [key]: [] }));
  const clearAllErrors = () => setEditErrors({});

  // Note that this currently only supports 1 warning message per key. If more than one warning per key is needed,
  // change to something like ({ ...prev, [key]: prev[key] ? [...(prev[key]), warningMsg] : [warningMsg] }))
  const addWarning = (key, warningMsg) => setEditWarnings((prev) => ({ ...prev, [key]: [warningMsg] }));
  const clearWarning = (key) => setEditWarnings((prev) => ({ ...prev, [key]: [] }));

  const handleWarnings = (data) => {
    // this function is used to check warnings for all fields on create client save
    // (note only dob field has a warning as of now)
    const inputDob = data.dob;
    handleDobWarning(inputDob);
  };

  const handleDobWarning = (inputDob) => {
    // this function is split off from handleWarnings so it can also be used
    // when editing existing client dob
    if (batchDob && inputDob && inputDob !== batchDob) {
      addWarning('dob', dobWarningMsg);
    } else {
      clearWarning('dob');
    }
  };

  const clientErrors = (errors?.client ?? editErrors?.client)?.map((errMsg) => (
    <p key={errMsg} className="text-red">
      {errMsg}
    </p>
  ));

  const addOrEditClient = (
    <>
      <ModalButton
        className="h-full border border-gray-700 rounded-md shadow-md font-semibold"
        title={
          <span>
            <FontAwesomeIcon icon={faPlus} /> New Client
          </span>
        }
      >
        <CreateClientModal
          onCreate={async (clientData) => {
            onClearError('client');
            clearError('client');
            try {
              await triggerAssignClientToBatch({
                batchId: batchId,
                data: { client_id: clientData.pk },
              }).unwrap();
              setPetitionerData(getPetitionerData(clientData));
            } catch (e) {
              addError('client', 'Unable to select new client. Please try searching and selecting the new client.');
            }
          }}
          handleWarnings={handleWarnings}
          handleDobWarning={handleDobWarning}
          warnings={editWarnings}
        />
      </ModalButton>
      {petitioner && (
        <Button
          colorClass="neutral"
          className="h-full border border-gray-700 rounded-md shadow-md font-semibold"
          onClick={() => {
            setIsEditing(true);
            handleWarnings(petitionerData);
          }}
        >
          <span>
            <FontAwesomeIcon icon={faPencilAlt} /> Edit
          </span>
        </Button>
      )}
    </>
  );

  const saveOrCancelChanges = (
    <>
      <Button
        className="h-full border border-gray-700 rounded-md shadow-md font-semibold"
        onClick={async () => {
          clearAllErrors();
          handleWarnings(petitionerData);
          try {
            await triggerClientUpdate({
              id: petitioner.pk,
              data: { ...petitionerData, category: 'client' },
            }).unwrap();
            setIsEditing(false);
          } catch (e) {
            const errorItems = Object.entries(e?.data);
            if (errorItems.length > 0) {
              errorItems.forEach(([key, value]) => addError(key, value));
            } else {
              addError('client', 'Error: Unable to select client');
            }
          }
        }}
      >
        <span>
          <FontAwesomeIcon icon={faSave} /> Save
        </span>
      </Button>
      <Button
        colorClass="neutral"
        className="h-full border border-gray-700 rounded-md shadow-md font-semibold"
        onClick={() => {
          setIsEditing(false);
          clearAllErrors();
          setPetitionerData(getPetitionerData(petitioner));
          handleWarnings(getPetitionerData(petitioner));
        }}
      >
        <span>
          <FontAwesomeIcon icon={faTimes} /> Cancel
        </span>
      </Button>
    </>
  );

  return (
    <>
      <div className="flex gap-4">
        <div className="flex flex-col">
          <AutocompleteInput
            placeholder="Search for a client..."
            className="w-[250px]"
            onSelect={async ({ pk, ...clientData }) => {
              onClearError('client');
              clearError('client');
              try {
                await triggerAssignClientToBatch({
                  batchId: batchId,
                  data: { client_id: pk },
                }).unwrap();

                setPetitionerData(clientData);
              } catch (e) {
                addError('client', 'Error: Unable to select client');
              }
            }}
            getSuggestionLabel={({ name: label }) => label}
            fetchSuggestions={async (searchValue) => {
              const data = await triggerSuggestionsFetch(
                {
                  search: searchValue,
                },
                true,
              ).unwrap();
              return data.results;
            }}
          />
        </div>
        {!isEditing ? addOrEditClient : saveOrCancelChanges}
      </div>
      {clientErrors &&
        clientErrors.map((errMsg) => (
          <p key={errMsg} className="text-red">
            {errMsg}
          </p>
        ))}
      {petitioner && (
        <div>
          <TextInput
            label="Name"
            value={name}
            onChange={(e) => setPetitionerData((prev) => ({ ...prev, name: e.target.value }))}
            errors={isEditing && editErrors.name}
            onClearError={onClearError}
            disabled={!isEditing}
          />
          <TextInput
            label="Date of Birth"
            value={dob}
            onChange={(e) => {
              setPetitionerData((prev) => ({ ...prev, dob: e.target.value }));
              handleDobWarning(e.target.value);
            }}
            errors={isEditing && editErrors.dob}
            warnings={isEditing && editWarnings.dob}
            onClearError={onClearError}
            disabled={!isEditing}
            type="date"
          />
          <AddressInput
            address={address}
            setAddress={setPetitionerData}
            errors={editErrors}
            onClearError={onClearError}
            disabled={!isEditing}
          />
        </div>
      )}
    </>
  );
}
