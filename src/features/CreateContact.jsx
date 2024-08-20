import { useRef } from 'react';
import { useForm } from 'react-hook-form';

import { useCreateAgencyMutation } from '../service/api';
import US_STATES from '../constants/US_STATES';
import FormInput from '../components/elements/Input/FormInput';
import FormSelect from '../components/elements/Input/FormSelect';
import FormTextArea from '../components/elements/Input/FormTextArea';
import { Button } from '../components/elements/Button';
import { useModalContext } from '../components/elements/Button/ModalButton';

export const CreateAgencyModal = () => {
  const modalElement = useRef();
  const { closeModal } = useModalContext();
  return (
    <div className="w-[550px] px-40 py-20" ref={modalElement}>
      <CreateContact
        onClose={closeModal}
        category="agency"
        submitAndKeepOpenTitle="Submit"
        submitAndCloseTitle="Submit and Close"
      />
    </div>
  );
};

const CATEGORY_TO_TITLE = {
  agency: 'Arresting Agency',
  client: 'Client',
  attorney: 'Attorney',
};

// TODO: SPlit out client/agency/attorney
export const CreateContact = ({
  onClose,
  category,
  onSubmitSuccess,
  submitAndKeepOpenTitle = '',
  submitAndCloseTitle = 'Submit',
}) => {
  const [triggerCreate] = useCreateAgencyMutation();
  const { control, handleSubmit, reset } = useForm({
    defaultValues: {
      name: '',
      address: '',
      city: '',
      zipcode: '',
      state: { label: 'NC', value: 'NC' },
      county: '',
      is_sheriff: false,
    },
    reValidateMode: 'onSubmit',
  });
  const onSubmit = async (formData) => {
    const submitData = {};
    Object.keys(formData).forEach((field) => {
      if (field === 'address') {
        const [address1, address2] = formData.address.split('\n');
        submitData.address1 = address1.trim();
        submitData.address2 = address2 ? address2.trim() : '';
      } else if (field === 'state') {
        submitData.state = formData.state.value;
      } else {
        submitData[field] = formData[field];
      }
    });
    const data = await triggerCreate({ data: { ...submitData } }).unwrap();
    reset();
    onSubmitSuccess?.(data);
  };
  const onSubmitAndClose = async (data) => {
    await onSubmit(data);
    onClose();
  };
  return (
    <div className="flex flex-col gap-8">
      <h3>{`Add New ${CATEGORY_TO_TITLE[category]}`}</h3>
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
          className="text-xl"
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
        <FormSelect
          className="w-[200px]"
          inputProps={{ control, name: 'state' }}
          label="State"
          options={US_STATES.map((s) => ({ value: s[0], label: s[0] }))}
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
        <FormInput
          label="County"
          className="w-[200px]"
          inputProps={{
            control,
            name: 'county',
            rules: {
              required: true,
            },
          }}
        />
        <FormInput
          type="checkbox"
          label="Is Sheriff?"
          className="w-[200px] flex flex-col gap-2 [&>input]:w-[20px]"
          inputProps={{
            control,
            name: 'is_sheriff',
            rules: {
              required: true,
            },
          }}
        />
      </form>
      <div className="flex flex-row gap-4 justify-center text-base">
        {submitAndKeepOpenTitle && (
          <Button type="submit" onClick={handleSubmit(onSubmit)}>
            {submitAndKeepOpenTitle}
          </Button>
        )}
        <Button type="submit" onClick={handleSubmit(onSubmitAndClose)}>
          {submitAndCloseTitle}
        </Button>
        <Button colorClass="neutral" onClick={() => onClose()}>
          Cancel
        </Button>
      </div>
    </div>
  );
};

export default CreateContact;
