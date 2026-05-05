import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router";
import { loginSuccess } from "../features/auth/authSlice"
import api from "../api/axios";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const response = await api.post("/api/auth/login/", {
        username,
        password,
      });

      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);

      dispatch(loginSuccess(response.data.user));
      navigate("/storage");

    } catch (error) {
      console.log("Ошибка входа");

      if (error.response) {
        console.log(error.response.data);
      }
    }
  }

  return (
    <div className="page">
      <h1>Вход</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <input
            className="inputs"
            type="text"
            placeholder="Логин"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div>
          <input
            className="inputs"
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button className="btns" type="submit">Войти</button>
      </form>
    </div>
  );
}