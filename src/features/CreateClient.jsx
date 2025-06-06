import { useForm, useWatch } from 'react-hook-form';

import { useCreateClientMutation } from '../service/api';
import US_STATES from '../constants/US_STATES';
import FormInput from '../components/elements/Input/FormInput';
import FormSelect from '../components/elements/Input/FormSelect';
import FormDateInput from '../components/elements/Input/FormDateInput';
import FormTextArea from '../components/elements/Input/FormTextArea';
import { Button } from '../components/elements/Button';
import DobWarning from '../components/elements/Warning/DobWarning';

export const CreateClient = ({
  onClose,
  category,
  onSubmitSuccess,
  submitAndKeepOpenTitle = '',
  submitAndCloseTitle = 'Submit',
  expectedDob,
}) => {
  const [triggerCreate] = useCreateClientMutation();
  const { control, handleSubmit, reset } = useForm({
    defaultValues: {
      name: '',
      address: '',
      city: '',
      zipcode: '',
      state: { label: 'NC', value: 'NC' },
      dob: null,
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
    const data = await triggerCreate({ data: { ...submitData, category } }).unwrap();
    reset();
    onSubmitSuccess?.(data);
  };
  const onSubmitAndClose = async (data) => {
    await onSubmit(data);
    onClose();
  };
  const dobFieldValue = useWatch({ control, name: 'dob' });
  return (
    <div className="flex flex-col gap-8">
      <h3>{'Add New Client'}</h3>
      <form className="flex flex-col gap-4">
        <FormInput
          label="Name"
          inputProps={{
            control,
            name: 'name',
            rules: { required: true },
          }}
        />
        <FormDateInput
          label="Date of Birth"
          inputProps={{
            control,
            name: 'dob',
            rules: { required: false },
          }}
        />
        <DobWarning
          enabled={expectedDob && dobFieldValue && dobFieldValue !== expectedDob}
          expectedValue={expectedDob}
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

export default CreateClient;
