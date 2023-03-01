import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { Button } from '../components/elements/Button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../components/elements/Table';
import { Tooltip } from '../components/elements/Tooltip/Tooltip';

export const ExistingPetitions = () => {
  const test = 0;
  return (
    <div className="flex flex-col">
      <h3 className="mb-2">Recent Petitions</h3>
      <p>Petitions you have recently worked on will show up here </p>
      <div className="w-full">
        <Table className="text-[1.7rem]" columnSizes="4fr 2fr 3fr 6fr">
          <TableHeader>
            <TableCell header>Label</TableCell>
            <TableCell header># Petitions</TableCell>
            <TableCell header>
              <Tooltip
                tooltipContent={
                  <p>Records are available for 24 hours before they need to be uploaded again</p>
                }
              >
                <div className="flex gap-2">
                  Time until removed
                  <FontAwesomeIcon icon={faQuestionCircle} />
                </div>
              </Tooltip>
            </TableCell>
            <TableCell header />
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell>Test Client Wake records</TableCell>
              <TableCell>
                <Button>1 Petition</Button>
              </TableCell>
              <TableCell>23 hours</TableCell>
              <TableCell className="flex gap-2">
                <Button>Download</Button>
                <Button>Advice Letter</Button>
                <Button>Record Summary</Button>
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Rob Gries</TableCell>
              <TableCell>
                <Button>4 Petitions</Button>
              </TableCell>
              <TableCell>2 hours</TableCell>
              <TableCell className="flex gap-2">
                <Button>Download</Button>
                <Button>Advice Letter</Button>
                <Button>Record Summary</Button>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  );
};
