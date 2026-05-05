import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  user: null,
  isAuth: false,
  isLoading: true,
};

const authSlice = createSlice({
  name: "auth",
  initialState,

  reducers: {
    loginSuccess(state, action) {
      state.user = action.payload;
      state.isAuth = true;
    },

    logout(state) {
      state.user = null;
      state.isAuth = false;
    },

    restoreAuth(state) {
      state.isAuth = true;
    },

    setUser(state, action) {
      state.user = action.payload;
      state.isAuth = true;
    },

    setLoading(state, action) {
      state.isLoading = action.payload;
    },
  },
});

export const { loginSuccess, logout, setUser, setLoading } = authSlice.actions;

export default authSlice.reducer;