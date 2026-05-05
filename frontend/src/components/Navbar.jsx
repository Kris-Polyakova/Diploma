import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../features/auth/authSlice";

export default function Navbar() {
  const isAuth = useSelector((state) => state.auth.isAuth);
  const dispatch = useDispatch();
  const user = useSelector((state) => state.auth.user);

  function handleLogout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    dispatch(logout());
  }

  return (
    <nav>
      {!isAuth ? (
        <>
          <Link to="/login">Вход</Link>
          <Link to="/register">Регистрация</Link>
        </>
      ) : (
        <>
          <Link to="/storage">Хранилище</Link>
          {user.is_admin ? 
          <Link to='/admin/users'>Пользователи</Link> 
          : null}

          <button className="btns exitBtn" onClick={handleLogout}>Выход</button>
        </>
      )}
    </nav>
  );
}