import { useSelector } from "react-redux"; 
import { Navigate } from "react-router-dom"; 

export default function AdminRoute({ children }) { 
  const { user, isLoading } = useSelector((state) => state.auth);

  if (isLoading) return null;

  if (!user || !user.is_admin) {
    return <Navigate to="/storage" />;
  }
  
  return children; 
}