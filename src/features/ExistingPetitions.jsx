import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { formatDistance } from 'date-fns';
import { Link } from 'react-router-dom';
import { manualAxiosRequest } from '../service/axios';
import { Button, ModalButton } from '../components/elements/Button';
import { Table, TableBody, TableCell, TableHeader, TableRow } from '../components/elements/Table';
import { Tooltip } from '../components/elements/Tooltip/Tooltip';
import { useDeleteBatchMutation, useGetUserBatchesQuery } from '../service/api';
import useAuth from '../hooks/useAuth';
import { DownloadDocumentsModal } from './DownloadDocuments';
import { hasValidationsErrors } from '../util/errors';
import { downloadFile } from '../util/downloadFile';
import { CAUTION, NEUTRAL } from '../components/elements/Button/Button';
import { useModalContext } from '../components/elements/Button/ModalButton';

const DeleteBatchModal = ({ batch }) => {
  const [triggerDelete] = useDeleteBatchMutation();
  const { closeModal } = useModalContext();
  return (
    <div className="flex flex-col gap-10 justify-center w-[450px] h-[200px]">
      <p className="text-[1.6rem] flex flex-wrap gap-x-2 gap-y-4 px-16">
        <span>
          <span className="text-red">Warning:</span>This action will PERMANENTLY delete the petition group:
        </span>
        <span className="font-semibold">{batch.label}</span>
      </p>
      <div className="flex gap-8 justify-center">
        <Button colorClass={CAUTION} className="w-[100px]" onClick={() => triggerDelete({ id: batch.pk })}>
          Delete
        </Button>
        <Button colorClass={NEUTRAL} className="w-[100px]" onClick={() => closeModal()}>
          Cancel
        </Button>
      </div>
    </div>
  );
};

// TODO: Rename batches to "Petition Groups"
export const ExistingPetitions = () => {
  const { user } = useAuth();
  const { data } = useGetUserBatchesQuery({ user: user.pk });
  const [downloadDocumentBatch, setDownloadDocumentBatch] = useState(null);

  return (
    <div className="flex flex-col">
      <h3 className="mb-2">Recent Petitions</h3>
      <p>Petitions you have recently worked on will show up here </p>
      <div className="w-full">
        <Table className="text-[1.7rem]" columnSizes="4fr 2fr 2fr 6fr">
          <TableHeader>
            <TableCell header>Label</TableCell>
            <TableCell header># Petitions</TableCell>
            <TableCell header>
              <div className="flex gap-2">
                Deletion Date
                <Tooltip
                  tooltipContent={
                    <p className="w-[300px] whitespace-normal text-black">
                      Note: Records are available for 48 hours before they need to be uploaded again
                    </p>
                  }
                  offset={[-10, 15]}
                >
                  <FontAwesomeIcon icon={faQuestionCircle} />
                </Tooltip>
              </div>
            </TableCell>
            <TableCell header />
          </TableHeader>
          <TableBody>
            {data?.results?.map((batch) => (
              <TableRow key={batch.pk}>
                <TableCell>{batch.label}</TableCell>
                <TableCell>
                  <Link to={`/generate/${batch.pk}`}>
                    <Button className="w-[105px]">
                      {`${batch.petitions.length} Petition${batch.petitions.length === 1 ? '' : 's'}`}
                    </Button>
                  </Link>
                </TableCell>
                <TableCell>{formatDistance(new Date(batch.automatic_delete_date), new Date())}</TableCell>
                <TableCell className="flex gap-2">
                  <Button
                    disabled={batch.petitions.every((petition) => hasValidationsErrors(petition.generation_errors))}
                    title={
                      batch.petitions.every((petition) => hasValidationsErrors(petition.generation_errors))
                        ? 'No available petitions for download. Click on the petition button to the left to fix.'
                        : undefined
                    }
                    onClick={() => {
                      setDownloadDocumentBatch(batch);
                    }}
                  >
                    Download
                  </Button>
                  {/*
                    Legal team requested this be temporarily removed from UI

                    <Button
                      disabled={!!batch?.generate_letter_errors?.batch}
                      title={batch?.generate_letter_errors?.batch?.join(' ') ?? ''}
                      onClick={() => {
                        manualAxiosRequest({
                          url: `/batch/${batch.pk}/generate_advice_letter/`,
                          responseType: 'arraybuffer',
                          method: 'post',
                        }).then((adviceLetter) => {
                          const docBlob = new Blob([adviceLetter.data], {
                            type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                          });
                          downloadFile(docBlob, 'Advice Letter.docx');
                        });
                      }}
                    >
                      Advice Letter
                    </Button>
                  */}
                  <Button
                    disabled={!!batch?.generate_summary_errors?.batch}
                    title={batch?.generate_summary_errors?.batch?.join(' ') ?? ''}
                    onClick={() => {
                      manualAxiosRequest({
                        url: `/batch/${batch.pk}/generate_summary/`,
                        responseType: 'arraybuffer',
                        method: 'post',
                      }).then((recordsSummary) => {
                        const docBlob = new Blob([recordsSummary.data], {
                          type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        });
                        downloadFile(docBlob, 'Records Summary.docx');
                      });
                    }}
                  >
                    Records Summary
                  </Button>
                  <ModalButton title="Delete" colorClass={CAUTION}>
                    <DeleteBatchModal batch={batch} />
                  </ModalButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <DownloadDocumentsModal
          petitions={downloadDocumentBatch?.petitions ?? []}
          isOpen={!!downloadDocumentBatch}
          onClose={() => setDownloadDocumentBatch(null)}
        />
      </div>
    </div>
  );
};
