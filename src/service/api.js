import { createApi } from '@reduxjs/toolkit/query/react';
import { axiosBaseQuery } from './axios';

export const api = createApi({
  // TODO: use baseUrl here instead of in axios.js
  baseQuery: axiosBaseQuery(),
  tagTypes: ['ContactList', 'Batch', 'Petition', 'User'],
  endpoints: (builder) => ({
    agencies: builder.query({
      query: ({ queryString }) => ({
        url: `contact/?category=agency&${queryString}`,
        method: 'get',
      }),
      providesTags: [{ type: 'ContactList', id: 'agency' }],
    }),
    searchAttornies: builder.query({
      query: ({ search }) => ({
        url: `contact/?category=attorney&search=${search}`,
        method: 'get',
      }),
    }),
    searchAgencies: builder.query({
      query: ({ search }) => ({
        url: `contact/?category=agency&search=${search}`,
        method: 'get',
      }),
    }),
    createContact: builder.mutation({
      query: ({ data }) => ({ url: `contact/`, method: 'post', data }),
      invalidatesTags: (_result, _err, { data: { category } }) => [
        { type: 'ContactList', id: category },
        { type: 'ContactFilterOptions', id: category },
      ],
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
    deleteAgency: builder.mutation({
      query: ({ id }) => ({ url: `contact/${id}/`, method: 'delete' }),
      invalidatesTags: [
        { type: 'ContactList', id: 'agency' },
        { type: 'ContactFilterOptions', id: 'agency' },
      ],
    }),
    searchClients: builder.query({
      query: ({ search }) => ({
        url: `contact/?category=client&search=${search}`,
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
    }),
    updateBatch: builder.mutation({
      query: ({ id, data }) => ({ url: `batch/${id}/`, method: 'put', data }),
      invalidatesTags: (_result, _err, { id }) => [{ type: 'Batch', id }],
    }),
    getBatch: builder.query({
      query: ({ id }) => ({ url: `batch/${id}/`, method: 'get' }),
      providesTags: (_result, _err, { id }) => {
        const tags = [{ type: 'Batch', id }];
        // TODO: Add petitions from this result to redux store
        /* if (result?.petitions) {
          tags.concat(result.petitions.map(({ pk }) => [{ type: 'Petition', id: pk }]));
        } */
        return tags;
      },
    }),
    getUserBatches: builder.query({
      query: ({ user }) => ({ url: `batch/`, method: 'get', params: { user, limit: 10 } }),
      providesTags: (result) =>
        result ? result.results.map(({ pk }) => [{ type: 'Batch', id: pk }]) : [],
    }),
    login: builder.mutation({
      query: (data) => ({ url: 'token/', method: 'post', data }),
    }),
    logout: builder.mutation({
      query: () => ({ url: 'token/', method: 'delete' }),
    }),
    users: builder.query({
      query: ({ params, id }) => {
        let url = 'users/';
        if (id) {
          url = `${url}/${id}/`;
        }
        return { url, method: 'get', params };
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
      invalidatesTags: (_result, _err, { petitionId }) => [{ type: 'Petition', id: petitionId }],
    }),
    assignAgenciesToDocuments: builder.mutation({
      query: ({ petitionId, agencies }) => ({
        url: `/petitions/${petitionId}/assign_agencies_to_documents/`,
        method: 'post',
        data: { agencies },
      }),
      invalidatesTags: (_result, _err, { petitionId }) => [{ type: 'Petition', id: petitionId }],
    }),
  }),
});

export const {
  useAgenciesQuery,
  useLazyAgenciesQuery,
  useLazySearchAgenciesQuery,
  useLazySearchAttorniesQuery,
  useLazySearchClientsQuery,
  useCreateContactMutation,
  useUpdateContactMutation,
  useDeleteAgencyMutation,
  useAssignAgenciesToDocumentsMutation,
  useLazyGetContactFilterOptionsQuery,
  useCreateBatchMutation,
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
} = api;
