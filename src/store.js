import { configureStore } from '@reduxjs/toolkit';
import { api } from './service/api';
import authReducer from './slices/auth';

const store = configureStore({
  reducer: {
    auth: authReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(api.middleware),
});

export default store;
