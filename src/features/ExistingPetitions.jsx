import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { formatDistance } from 'date-fns';
import { Link } from 'react-router-dom';
import { manualAxiosRequest } from '../service/axios';
import { Button, ModalButton } from '../components/elements/Button';
import {
  LegacyPageSelection,
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
  calculateNumberOfPages,
} from '../components/elements/Table';
import { Tooltip } from '../components/elements/Tooltip/Tooltip';
import { useDeleteBatchMutation, useGetUserBatchesQuery, useCombineBatchesMutation } from '../service/api';
import useAuth from '../hooks/useAuth';
import { DownloadDocumentsModal } from './DownloadDocuments';
import { hasValidationsErrors } from '../util/errors';
import { downloadFile } from '../util/downloadFile';
import { POSITIVE, CAUTION, NEUTRAL } from '../components/elements/Button/Button';
import { useModalContext } from '../components/elements/Button/ModalButton';
import Input from '../components/elements/Input/Input';

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

const finishCombineModal = ({ batchIds, setBatchIdsToCombine, triggerCombine, newLabel, closeModal }) => {
  let postData = {
    batchIds: batchIds,
    label: newLabel,
  };

  triggerCombine(postData).then(() => {
    setBatchIdsToCombine([]);
    closeModal();
  });
};

const CombineBatchModalButton = ({ batchId, batchIdsToCombine, setBatchIdsToCombine }) => {
  if (batchIdsToCombine.includes(batchId)) {
    return (
      <Button
        title="Subtract"
        colorClass={NEUTRAL}
        onClick={() => {
          setBatchIdsToCombine((prevList) => prevList.filter((item) => item != batchId));
        }}
      >
        Subtract
      </Button>
    );
  } else {
    return (
      <Button
        title="Add"
        colorClass={POSITIVE}
        onClick={() => {
          setBatchIdsToCombine((prevList) => [...prevList, batchId]);
        }}
      >
        Add
      </Button>
    );
  }
};

const COMBINE_MODAL_NUM_PETITIONS_PER_PAGE = 5;

const CombineBatchModal = () => {
  const { user } = useAuth();
  const [newLabel, setNewLabel] = useState('');
  const { closeModal } = useModalContext();
  const [batchIdsToCombine, setBatchIdsToCombine] = useState([]);
  const [triggerCombine] = useCombineBatchesMutation();
  const [pageNumber, setPageNumber] = useState(1);

  const { data } = useGetUserBatchesQuery({
    user: user.pk,
    offset: (pageNumber - 1) * COMBINE_MODAL_NUM_PETITIONS_PER_PAGE,
    limit: COMBINE_MODAL_NUM_PETITIONS_PER_PAGE,
  });

  useEffect(() => {
    if (calculateNumberOfPages(data?.count ?? 0, COMBINE_MODAL_NUM_PETITIONS_PER_PAGE) < pageNumber) {
      setPageNumber(1);
    }
  }, [data?.count, pageNumber]);

  return (
    <div className="flex flex-col gap-10 justify-center min-w-[600px] min-h-[100px] p-10">
      <div>
        <LegacyPageSelection
          currentPage={pageNumber}
          numPages={calculateNumberOfPages(data?.count ?? 0, COMBINE_MODAL_NUM_PETITIONS_PER_PAGE)}
          onPageSelect={(pageNum) => setPageNumber(pageNum)}
        />
      </div>
      <div className="h-[300px]">
        <Table className="text-[1.7rem]" columnSizes="4fr 2fr">
          <TableHeader>
            <TableCell header>Label</TableCell>
            <TableCell header>Action</TableCell>
          </TableHeader>
          <TableBody>
            {data?.results?.map((batch) => (
              <TableRow key={batch.pk}>
                <TableCell>{batch.label}</TableCell>
                <TableCell>
                  <CombineBatchModalButton
                    batchId={batch.pk}
                    batchIdsToCombine={batchIdsToCombine}
                    setBatchIdsToCombine={setBatchIdsToCombine}
                  ></CombineBatchModalButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="flex flex-col gap-10 justify-center w-[450px] h-[200px]">
        <form>
          <TextInput label="New Label" onChange={(e) => setNewLabel(e.target.value)} />
        </form>
        <div className="flex gap-8 justify-center">
          <Button
            colorClass={POSITIVE}
            className="w-[100px]"
            onClick={() =>
              finishCombineModal({
                batchIds: batchIdsToCombine,
                setBatchIdsToCombine: setBatchIdsToCombine,
                triggerCombine: triggerCombine,
                newLabel: newLabel,
                closeModal: closeModal,
              })
            }
            disabled={batchIdsToCombine.length === 0 || !newLabel}
            title="Please add a new label and atleast one client upload."
          >
            Finish
          </Button>
          <Button colorClass={CAUTION} className="w-[100px]" onClick={() => closeModal()}>
            Cancel
          </Button>
        </div>
      </div>
    </div>
  );
};

const BATCH_TABLE_NUM_PETITIONS_PER_PAGE = 7;

// TODO: Rename batches to "Petition Groups"
export const ExistingPetitions = () => {
  const { user } = useAuth();
  const [pageNumber, setPageNumber] = useState(1);
  const { data } = useGetUserBatchesQuery({
    user: user.pk,
    offset: (pageNumber - 1) * BATCH_TABLE_NUM_PETITIONS_PER_PAGE,
    limit: BATCH_TABLE_NUM_PETITIONS_PER_PAGE,
  });
  const [downloadDocumentBatch, setDownloadDocumentBatch] = useState(null);

  useEffect(() => {
    if (calculateNumberOfPages(data?.count ?? 0, BATCH_TABLE_NUM_PETITIONS_PER_PAGE) < pageNumber) {
      setPageNumber(1);
    }
  }, [data?.count, pageNumber]);

  return (
    <div className="flex flex-col">
      <ModalButton title="Combine Petitions" colorClass={POSITIVE} className="w-[150px] h-[32px] mb-5">
        <CombineBatchModal rowData={data?.results} />
      </ModalButton>
      <h3 className="mb-2">Recent Petitions</h3>
      <p>Petitions you have recently worked on will show up here </p>
      <div className="w-full">
        <div className="tw-flex items-end justify-end pb-2">
          <LegacyPageSelection
            currentPage={pageNumber}
            numPages={calculateNumberOfPages(data?.count ?? 0, BATCH_TABLE_NUM_PETITIONS_PER_PAGE)}
            onPageSelect={(pageNum) => setPageNumber(pageNum)}
          />
        </div>
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
                    Summary
                  </Button>
                  <Button
                    onClick={() => {
                      manualAxiosRequest({
                        url: `/batch/${batch.pk}/generate_spreadsheet/`,
                        responseType: 'arraybuffer',
                        method: 'post',
                      }).then((recordsSummary) => {
                        const docBlob = new Blob([recordsSummary.data], {
                          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        });
                        downloadFile(docBlob, `${batch.label}.xlsx`);
                      });
                    }}
                  >
                    Spreadsheet
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
