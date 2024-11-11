import { createApi } from '@reduxjs/toolkit/query/react';
import { axiosBaseQuery } from './axios';

export const api = createApi({
  // TODO: use baseUrl here instead of in axios.js
  baseQuery: axiosBaseQuery(),
  tagTypes: ['ContactList', 'Batch', 'Petition', 'User'],
  endpoints: (builder) => ({
    agencies: builder.query({
      query: ({ queryString }) => ({
        url: `agency/?${queryString}`,
        method: 'get',
      }),
      providesTags: [{ type: 'ContactList', id: 'agency' }],
    }),
    createAgency: builder.mutation({
      query: ({ data }) => ({ url: `agency/`, method: 'post', data }),
      invalidatesTags: (result) =>
        result
          ? [
              { type: 'ContactList', id: 'agency' },
              { type: 'ContactFilterOptions', id: 'agency' },
            ]
          : [],
    }),
    updateAgency: builder.mutation({
      query: ({ id, data }) => ({ url: `agency/${id}/`, method: 'put', data }),
      invalidatesTags: (result) =>
        result
          ? [
              { type: 'ContactList', id: 'agency' },
              { type: 'ContactFilterOptions', id: 'agency' },
            ]
          : [],
    }),
    searchAttornies: builder.query({
      query: ({ search }) => ({
        url: `contact/?category=attorney&search=${search}`,
        method: 'get',
      }),
    }),
    searchAgencies: builder.query({
      query: ({ search }) => ({
        url: `agency/?search=${search}`,
        method: 'get',
      }),
    }),
    createContact: builder.mutation({
      query: ({ data }) => ({ url: `contact/`, method: 'post', data }),
      invalidatesTags: (result) =>
        result
          ? [
              { type: 'ContactList', id: result.category },
              { type: 'ContactFilterOptions', id: result.category },
            ]
          : [],
    }),
    updateContact: builder.mutation({
      query: ({ id, data }) => ({ url: `contact/${id}/`, method: 'put', data }),
      invalidatesTags: (result) =>
        result
          ? [
              { type: 'ContactList', id: result.category },
              { type: 'ContactFilterOptions', id: result.category },
            ]
          : [],
    }),
    createClient: builder.mutation({
      query: ({ data }) => ({ url: `client/`, method: 'post', data }),
    }),
    updateClient: builder.mutation({
      query: ({ id, data }) => ({ url: `client/${id}/`, method: 'put', data }),
      invalidatesTags: (result) => {
        if (!result) {
          return [];
        }
        const tags = [
          { type: 'ContactList', id: result.category },
          { type: 'ContactFilterOptions', id: result.category },
        ];
        console.log(result);
        result?.batches?.forEach((batchId) => tags.push({ type: 'Batch', id: batchId }));
        return tags;
      },
    }),
    deleteAgency: builder.mutation({
      query: ({ id }) => ({ url: `agency/${id}/`, method: 'delete' }),
      invalidatesTags: [
        { type: 'ContactList', id: 'agency' },
        { type: 'ContactFilterOptions', id: 'agency' },
      ],
    }),
    previewImportAgencies: builder.mutation({
      query: ({ data }) => ({ url: `agency/preview_import_agencies/`, method: 'put', data }),
    }),
    importAgencies: builder.mutation({
      query: ({ data }) => ({ url: `agency/import_agencies/`, method: 'put', data }),
      invalidatesTags: [{ type: 'ContactList', id: 'agency' }],
    }),
    searchClients: builder.query({
      query: ({ search }) => ({
        url: `client/?search=${search}`,
        method: 'get',
      }),
    }),
    getContactFilterOptions: builder.query({
      query: ({ params }) => ({ url: 'contact/get_filter_options/', method: 'get', params }),
      providesTags: (result, _error, { params: { category } }) =>
        result ? [{ type: 'ContactFilterOptions', id: category }] : [],
    }),
    checkLogin: builder.query({
      query: () => ({ url: 'token/', method: 'get' }),
    }),
    createBatch: builder.mutation({
      query: ({ data }) => ({ url: 'batch/', method: 'post', timeout: 30 * 1000, data }),
      invalidatesTags: (result) => (result ? [{ type: 'Batch' }] : []),
    }),
    createBatchFromRecordSpreadsheet: builder.mutation({
      query: ({ data }) => ({ url: `batch/import_spreadsheet/`, method: 'post', timeout: 30 * 1000, data }),
      invalidatesTags: (result) => (result ? [{ type: 'Batch' }] : []),
    }),
    deleteBatch: builder.mutation({
      query: ({ id }) => ({ url: `batch/${id}/`, method: 'delete' }),
      invalidatesTags: ['Batch'],
    }),
    updateBatch: builder.mutation({
      query: ({ id, data }) => ({ url: `batch/${id}/`, method: 'put', data }),
      invalidatesTags: (result, _err, { id }) => {
        const tags = [{ type: 'Batch', id }];
        result?.petitions?.forEach(({ pk }) => tags.push({ type: 'Petition', id: pk }));
        return tags;
      },
    }),
    getBatch: builder.query({
      query: ({ id }) => ({ url: `batch/${id}/`, method: 'get', timeout: 30 * 1000 }),
      providesTags: (result, _err, { id }) => {
        const tags = [{ type: 'Batch', id }];
        // TODO: Add petitions from this result to redux store
        if (result?.petitions) {
          tags.concat(result.petitions.map(({ pk }) => [{ type: 'Petition', id: pk }]));
        }
        return tags;
      },
    }),
    getUserBatches: builder.query({
      query: ({ user, limit, offset }) => ({ url: `batch/`, method: 'get', params: { user, limit, offset } }),
      providesTags: ['Batch'],
    }),
    combineBatches: builder.mutation({
      query: (data) => ({ url: 'batch/combine_batches/', method: 'post', data }),
      invalidatesTags: ['Batch'],
    }),
    login: builder.mutation({
      query: (data) => ({ url: 'token/', method: 'post', data }),
    }),
    logout: builder.mutation({
      query: () => ({ url: 'token/', method: 'delete' }),
    }),
    users: builder.query({
      query: ({ queryString, id }) => {
        let url = 'users/';
        if (id) {
          url = `${url}/${id}/`;
        }
        url = `${url}?${queryString}`;
        return { url, method: 'get' };
      },
      providesTags: ['User'],
    }),
    createUser: builder.mutation({
      query: (params) => ({ url: `users/`, method: 'post', data: { ...params } }),
      invalidatesTags: ['User'],
    }),
    modifyUser: builder.mutation({
      query: ({ id, data, method = 'put' }) => ({ url: `users/${id}/`, method, data }),
      invalidatesTags: ['User'],
    }),
    petition: builder.query({
      query: ({ petitionId }) => ({ url: `/petitions/${petitionId}/`, method: 'GET' }),
      providesTags: (_result, _err, { petitionId }) => [{ type: 'Petition', id: petitionId }],
    }),
    recalculatePetitions: builder.mutation({
      query: ({ petitionId, offenseRecordIds }) => ({
        url: `/petitions/${petitionId}/recalculate_petitions/`,
        data: { offense_record_ids: offenseRecordIds },
        method: 'POST',
      }),
      invalidatesTags: (result, _err, { petitionId }) => [
        { type: 'Batch', id: result?.batch },
        { type: 'Petition', id: petitionId },
      ],
    }),
    assignAgenciesToDocuments: builder.mutation({
      query: ({ petitionId, agencies }) => ({
        url: `/petitions/${petitionId}/assign_agencies_to_documents/`,
        method: 'post',
        data: { agencies },
      }),
      invalidatesTags: (result, _err, { petitionId }) => [
        { type: 'Batch', id: result?.batch },
        { type: 'Petition', id: petitionId },
      ],
    }),
    assignClientToBatch: builder.mutation({
      query: ({ batchId, data }) => ({
        url: `/batch/${batchId}/assign_client_to_batch/`,
        method: 'post',
        data: data,
      }),
      invalidatesTags: (result) => {
        if (!result) {
          return [];
        }
        const tags = [
          { type: 'ContactList', id: result.category },
          { type: 'ContactFilterOptions', id: result.category },
          { type: 'Batch', id: result.batch_id },
        ];
        return tags;
      },
    }),
  }),
});

export const {
  useAgenciesQuery,
  useCreateAgencyMutation,
  useUpdateAgencyMutation,
  useLazyAgenciesQuery,
  useLazySearchAgenciesQuery,
  useLazySearchAttorniesQuery,
  useLazySearchClientsQuery,
  useCreateContactMutation,
  useUpdateContactMutation,
  useCreateClientMutation,
  useUpdateClientMutation,
  useDeleteAgencyMutation,
  useImportAgenciesMutation,
  usePreviewImportAgenciesMutation,
  useAssignAgenciesToDocumentsMutation,
  useLazyGetContactFilterOptionsQuery,
  useCreateBatchMutation,
  useCreateBatchFromRecordSpreadsheetMutation,
  useDeleteBatchMutation,
  useCombineBatchesMutation,
  useLazyCheckLoginQuery,
  useGetBatchQuery,
  useGetUserBatchesQuery,
  useUpdateBatchMutation,
  useLoginMutation,
  useLogoutMutation,
  usePetitionQuery,
  useRecalculatePetitionsMutation,
  useCreateUserMutation,
  useModifyUserMutation,
  useUsersQuery,
  useAssignClientToBatchMutation,
} = api;
