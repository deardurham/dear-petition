import React, { useState, useEffect } from 'react';
import { GenerationInputsStyled, } from './GenerationInputs.styled';
import Input from '../../elements/Input/Input';
import Select from '../../elements/Input/Select';

const FAKE_ATTORNEYS = [
    { id: 0, name: "Jeff" },
    { id: 1, name: "Madge" },
]

function GenerationInputs(props) {
    const [ssn, setSSN] = useState('');
    const [license, setLicense] = useState('');
    const [attorney, setAttorney] = useState('');

    useEffect(() => {
        // fetch attornies
    })

    const mapAttorneysToOptions = () => FAKE_ATTORNEYS.map(att => ({ value: att.id, name: att.name }))

    return (
        <GenerationInputsStyled>
            <Select label="Attorney" value={attorney} onChange={e => setAttorney(e.target.value)} options={mapAttorneysToOptions()} />
            <Input label="SSN" value={ssn} onChange={e => setSSN(e.target.value)} />
            <Input label="License #" value={license} onChange={e => setLicense(e.target.value)} />
        </GenerationInputsStyled>
    );
}

export default GenerationInputs;
