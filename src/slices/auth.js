import { createSlice } from '@reduxjs/toolkit';
import { api } from '../service/api';

const initialState = {
  user: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loggedIn(state, action) {
      state.user = action.payload;
    },
    loggedOut(state) {
      state.user = null;
    },
  },
  extraReducers: (builder) => {
    builder.addMatcher(api.endpoints.login.matchFulfilled, (state, { payload }) => {
      state.user = payload.user;
    });
    builder.addMatcher(api.endpoints.logout.matchFulfilled, (state) => {
      state.user = null;
    });
  },
});

export const { loggedIn, loggedOut } = authSlice.actions;
export default authSlice.reducer;
