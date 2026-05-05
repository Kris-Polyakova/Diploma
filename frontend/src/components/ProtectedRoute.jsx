import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const { isAuth, isLoading } = useSelector((state) => state.auth);

  if (isLoading) {
    return <p>Загрузка...</p>;
  }

  if (!isAuth) {
    return <Navigate to="/login" />;
  }

  return children;
}