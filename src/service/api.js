import { createApi } from '@reduxjs/toolkit/query/react';
import { axiosBaseQuery } from './axios';

export const api = createApi({
  // TODO: use baseUrl here instead of in axios.js
  baseQuery: axiosBaseQuery(),
  tagTypes: ['AgencyList', 'Petition', 'User'],
  endpoints: (builder) => ({
    agencies: builder.query({
      query: ({ queryString }) => ({
        url: `contact/?category=agency&${queryString}`,
        method: 'get',
      }),
      providesTags: ['AgencyList'],
    }),
    searchAgencies: builder.query({
      query: ({ search }) => ({
        url: `contact/?category=agency&search=${search}`,
        method: 'get',
      }),
    }),
    createAgency: builder.mutation({
      query: ({ data }) => ({ url: `contact/`, method: 'post', data }),
      invalidatesTags: ['AgencyList', 'ContactFilterOptions'],
    }),
    deleteAgency: builder.mutation({
      query: ({ id }) => ({ url: `contact/${id}/`, method: 'delete' }),
      invalidatesTags: ['AgencyList', 'ContactFilterOptions'],
    }),
    updateAgency: builder.mutation({
      query: ({ id, data }) => ({ url: `contact/${id}/`, method: 'put', data }),
      invalidatesTags: ['AgencyList', 'ContactFilterOptions'],
    }),
    getContactFilterOptions: builder.query({
      query: ({ params }) => ({ url: 'contact/get_filter_options/', method: 'get', params }),
      providesTags: (result) => (result ? ['ContactFilterOptions'] : []),
    }),
    checkLogin: builder.query({
      query: () => ({ url: 'token/', method: 'get' }),
    }),
    createBatch: builder.mutation({
      query: ({ data }) => ({ url: 'batch/', method: 'post', timeout: 30 * 1000, data }),
    }),
    getBatch: builder.query({
      query: ({ id }) => ({ url: `batch/${id}/`, method: 'get' }),
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
  useCreateAgencyMutation,
  useDeleteAgencyMutation,
  useUpdateAgencyMutation,
  useAssignAgenciesToDocumentsMutation,
  useLazyGetContactFilterOptionsQuery,
  useCreateBatchMutation,
  useLazyCheckLoginQuery,
  useGetBatchQuery,
  useLoginMutation,
  useLogoutMutation,
  usePetitionQuery,
  useRecalculatePetitionsMutation,
  useCreateUserMutation,
  useModifyUserMutation,
  useUsersQuery,
} = api;
