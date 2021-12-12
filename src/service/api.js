import { createApi } from '@reduxjs/toolkit/query/react';
import { axiosBaseQuery } from './axios';

export const api = createApi({
  // TODO: use baseUrl here instead of in axios.js
  baseQuery: axiosBaseQuery(),
  tagTypes: ['User'],
  endpoints: (builder) => ({
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
      query: (args) => {
        let url = '';
        if (args?.id) {
          url = `users/${args.id}/`;
        } else {
          const params = [];
          if (args?.limit) {
            params.push(`limit=${args.limit}`);
          }
          if (args?.offset) {
            params.push(`offset=${args.offset}`);
          }
          url = `users/${params.length > 0 ? '?' + params.join('&') : ''}`;
        }
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
  }),
});

export const {
  useCreateBatchMutation,
  useLazyCheckLoginQuery,
  useGetBatchQuery,
  useLoginMutation,
  useLogoutMutation,
  useCreateUserMutation,
  useModifyUserMutation,
  useUsersQuery,
} = api;
