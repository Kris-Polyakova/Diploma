import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import StoragePage from "./pages/StoragePage";
import AdminUsersPage from "./pages/AdminUsersPage";
import AdminRoute from "./components/AdminRoute";

import { useDispatch } from "react-redux";
import api from "./api/axios";
import { useEffect } from "react";
import { setUser, setLoading } from "./features/auth/authSlice";

function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    const token = localStorage.getItem("access");
  
    if (token) {
      loadUser();
    } else {
      dispatch(setLoading(false));
    }
  }, []);
  
  async function loadUser() {
    try {
      const response = await api.get("/api/auth/me/");
  
      dispatch(setUser(response.data));
  
    } catch (error) {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
    } finally {
      dispatch(setLoading(false));
    }
  }

  return (
    <BrowserRouter>
        <Navbar />
        <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route 
              path="/storage" 
              element={<ProtectedRoute>
                <StoragePage />
              </ProtectedRoute>
              }
            />
            <Route
              path="/admin/users"
              element={<AdminRoute>
                  <AdminUsersPage />
                </AdminRoute>
              }
            />
        </Routes>
    </BrowserRouter>
  );
}

export default App;